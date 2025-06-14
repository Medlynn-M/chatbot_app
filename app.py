import streamlit as st
import fitz  # PyMuPDF
import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load API key
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
if not api_key and "GEMINI_API_KEY" in st.secrets:
    api_key = st.secrets["GEMINI_API_KEY"]

if not api_key:
    st.error("❌ GEMINI_API_KEY not found. Please set it in .env or Streamlit Secrets.")
    st.stop()

# Configure Gemini
try:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("models/text-bison-001")
except Exception as e:
    st.error(f"⚠️ Gemini configuration error: {e}")
    st.stop()

# Load the PDF content
def load_pdf_text(pdf_path):
    text = ""
    try:
        doc = fitz.open(pdf_path)
        for page in doc:
            text += page.get_text()
        return text
    except Exception as e:
        st.error(f"❌ Failed to load PDF: {e}")
        return None

pdf_text = load_pdf_text("my_report.pdf")

# Layout setup
st.set_page_config(layout="wide")
st.title("📊 AI-Driven Stockout Risk Optimization Chatbot")

col1, col2 = st.columns(2)

# LEFT: Tableau Embed
with col1:
    st.subheader("📈 Interactive Tableau Dashboard")
    st.markdown("""
        <iframe src="https://public.tableau.com/views/AI-DrivenStockoutRiskPredictionforSmarterInventoryManagement/AI-drivenstockoutriskoptimizationforsmarterinventorymanagement?:language=en-US&:display_count=n&:origin=viz_share_link"
        width="100%" height="600" style="border:none;"></iframe>
    """, unsafe_allow_html=True)

# RIGHT: Q&A
with col2:
    st.subheader("💬 Ask Questions from the PDF Report")
    if pdf_text:
        question = st.text_input("Ask your question:")
        if question:
            try:
                response = model.generate_content(["Context:\n" + pdf_text + "\n\nQuestion:" + question])
                st.success(response.text.strip())
            except Exception as e:
                st.error(f"⚠️ Gemini Error: {e}")
    else:
        st.error("PDF not loaded. Cannot answer questions.")

# SIDEBAR RESOURCES
st.sidebar.title("📂 Project Resources")

try:
    with open("my_report.pdf", "rb") as f:
        st.sidebar.download_button("📄 Download Report", f, file_name="my_report.pdf")
except:
    st.sidebar.warning("⚠️ PDF not found")

try:
    with open("my_data.csv", "rb") as f:
        st.sidebar.download_button("🧾 Download Dataset", f, file_name="my_data.csv")
except:
    st.sidebar.warning("⚠️ Dataset not found")

try:
    with open("my_code.ipynb", "rb") as f:
        st.sidebar.download_button("🐍 Download Code", f, file_name="my_code.ipynb")
except:
    st.sidebar.warning("⚠️ Code file not found")

st.sidebar.markdown("🔗 [📦 View Dataset on Kaggle](https://www.kaggle.com/datasets/anirudhchauhan/retail-store-inventory-forecasting-dataset/data)")
