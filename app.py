import streamlit as st
import fitz  # PyMuPDF
import google.generativeai as genai
import os

# Set up Gemini API key
api_key = st.secrets["GEMINI_API_KEY"] if "GEMINI_API_KEY" in st.secrets else os.getenv("GEMINI_API_KEY")

if not api_key:
    st.error("❌ Gemini API key not found. Add it in Streamlit secrets or .env file.")
    st.stop()

genai.configure(api_key=api_key)
model = genai.GenerativeModel("models/gemini-2.0-flash")

# Load the PDF content
def load_pdf_text(pdf_path):
    try:
        doc = fitz.open(pdf_path)
        return "\n".join(page.get_text() for page in doc)
    except Exception as e:
        st.error(f"❌ Failed to load PDF: {e}")
        return None

pdf_text = load_pdf_text("my_report.pdf")

# UI setup
st.set_page_config(layout="wide")
st.title("📊 AI-Driven Stockout Risk Optimization Chatbot")

col1, col2 = st.columns(2)

with col1:
    st.subheader("📈 Tableau Dashboard")
    st.markdown("""
        The Tableau dashboard cannot be embedded directly here.  
        👉 [Click to view the dashboard in a new tab](https://public.tableau.com/views/AI-DrivenStockoutRiskPredictionforSmarterInventoryManagement/AI-drivenstockoutriskoptimizationforsmarterinventorymanagement?:language=en-US&publish=yes)
    """, unsafe_allow_html=True)

with col2:
    st.subheader("💬 Ask Questions")
    if pdf_text:
        question = st.text_input("Ask your question:")
        if question:
            try:
                response = model.generate_content(f"Answer the question based on the report:\n\n{pdf_text}\n\nQuestion: {question}")
                st.success(response.text)
            except Exception as e:
                st.error(f"⚠️ Gemini Error: {e}")
    else:
        st.warning("PDF content not available.")

# Sidebar Downloads
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
