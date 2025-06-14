import streamlit as st
from transformers import pipeline
import fitz  # PyMuPDF for reading PDFs

# Load Hugging Face token from secrets (for deployment)
hf_token = st.secrets["HUGGINGFACE_TOKEN"]

# Hugging Face Q&A pipeline (DistilBERT)
qa = pipeline("question-answering",
              model="distilbert-base-cased-distilled-squad",
              tokenizer="distilbert-base-cased-distilled-squad",
              use_auth_token=hf_token)

# Load and extract text from PDF
def extract_text_from_pdf(pdf_path):
    text = ""
    try:
        doc = fitz.open(pdf_path)
        for page in doc:
            text += page.get_text()
    except Exception as e:
        st.error(f"❌ Error loading PDF: {e}")
    return text

# Extract context
pdf_text = extract_text_from_pdf("my_report.pdf")

# UI layout
st.set_page_config(layout="wide")
st.title("📊 AI Chatbot + Tableau Dashboard (Free Hugging Face Version)")

col1, col2 = st.columns(2)

# LEFT: Dashboard
with col1:
    st.subheader("📈 Interactive Tableau Dashboard")
    st.markdown("""
<iframe src="https://public.tableau.com/views/AI-DrivenStockoutRiskPredictionforSmarterInventoryManagement/AI-drivenstockoutriskoptimizationforsmarterinventorymanagement?:language=en-US&:display_count=n&:origin=viz_share_link"
width="100%" height="600" style="border:none;"></iframe>
""", unsafe_allow_html=True)

# RIGHT: Chatbot
with col2:
    st.subheader("🤖 Ask About the Project")
    user_question = st.text_input("Ask your question here:")
    if user_question:
        try:
            result = qa(question=user_question, context=pdf_text)
            st.success(result["answer"])
        except Exception as e:
            st.error(f"⚠️ Hugging Face error: {e}")

# Sidebar Resources
st.sidebar.title("📂 Project Resources")

try:
    with open("my_report.pdf", "rb") as f:
        st.sidebar.download_button("📄 Download Report", f, file_name="my_report.pdf")
except:
    st.sidebar.warning("⚠️ Report not found")

try:
    with open("my_data.csv", "rb") as f:
        st.sidebar.download_button("📊 Download Dataset", f, file_name="my_data.csv")
except:
    st.sidebar.warning("⚠️ Dataset missing")

try:
    with open("my_code.ipynb", "rb") as f:
        st.sidebar.download_button("🐍 Download Code", f, file_name="my_code.ipynb")
except:
    st.sidebar.warning("⚠️ Code file missing")

st.sidebar.markdown("🔗 [📦 View Dataset on Kaggle](https://www.kaggle.com/datasets/anirudhchauhan/retail-store-inventory-forecasting-dataset/data)")
