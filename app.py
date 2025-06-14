import streamlit as st
import fitz  # PyMuPDF
import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

# Validate API key
if not api_key:
    st.error("❌ GOOGLE_API_KEY not found in environment. Please set it in .env or Streamlit secrets.")
    st.stop()

genai.configure(api_key=api_key)

# Load Gemini model
try:
    model = genai.GenerativeModel("gemini-2.0-flash")
except Exception as e:
    st.error(f"❌ Failed to load Gemini model: {e}")
    st.stop()

# PDF loader function
def load_pdf_text(pdf_path):
    try:
        doc = fitz.open(pdf_path)
        return "\n".join([page.get_text() for page in doc])
    except Exception as e:
        st.error(f"❌ Could not load PDF: {e}")
        return None

pdf_text = load_pdf_text("my_report.pdf")

# Streamlit UI
st.set_page_config(layout="wide")
st.title("📊 AI Chatbot for Capstone Project")

col1, col2 = st.columns(2)

# LEFT: Tableau dashboard (via link)
with col1:
    st.subheader("📈 View Tableau Dashboard")
    st.markdown(
        "[🔗 Click to open the dashboard](https://public.tableau.com/views/AI-DrivenStockoutRiskPredictionforSmarterInventoryManagement/AI-drivenstockoutriskoptimizationforsmarterinventorymanagement?:language=en-US&publish=yes&:sid=&:redirect=auth&:display_count=n&:origin=viz_share_link)",
        unsafe_allow_html=True
    )

# RIGHT: Chatbot
with col2:
    st.subheader("💬 Ask Your Questions")
    if pdf_text:
        user_question = st.text_input("Ask about the project report:")
        if user_question:
            try:
                response = model.generate_content([f"Use this report to answer: {user_question}", pdf_text])
                st.success(response.text.strip())
            except Exception as e:
                st.error(f"⚠️ Error from Gemini: {e}")
    else:
        st.warning("⚠️ PDF not loaded.")

# Sidebar resources
st.sidebar.title("📂 Project Resources")

try:
    with open("my_report.pdf", "rb") as f:
        st.sidebar.download_button("📄 Download Report", f, "Capstone_Report.pdf")
except:
    st.sidebar.warning("PDF not found.")

try:
    with open("my_data.csv", "rb") as f:
        st.sidebar.download_button("🧾 Download Dataset", f, "Retail_Data.csv")
except:
    st.sidebar.warning("Dataset not found.")

try:
    with open("my_code.ipynb", "rb") as f:
        st.sidebar.download_button("🐍 Download Code", f, "Capstone_Code.ipynb")
except:
    st.sidebar.warning("Code not found.")

st.sidebar.markdown("🔗 [📦 View Dataset on Kaggle](https://www.kaggle.com/datasets/anirudhchauhan/retail-store-inventory-forecasting-dataset/data)")
