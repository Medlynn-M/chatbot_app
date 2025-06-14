import streamlit as st
import fitz  # PyMuPDF
from transformers import pipeline

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

# Load the PDF
pdf_text = load_pdf_text("my_report.pdf")

# Initialize Hugging Face QA pipeline (no API key required)
@st.cache_resource
def load_qa_pipeline():
    return pipeline(
        "question-answering",
        model="deepset/roberta-base-squad2",
        tokenizer="deepset/roberta-base-squad2"
    )

qa_pipeline = load_qa_pipeline()

# Streamlit layout
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

# RIGHT: PDF-based chatbot
with col2:
    st.subheader("💬 Ask Questions from the PDF Report")
    if pdf_text:
        user_question = st.text_input("Ask your question:")
        if user_question:
            try:
                response = qa_pipeline(question=user_question, context=pdf_text)
                st.success(response["answer"])
            except Exception as e:
                st.error(f"⚠️ Model error: {e}")
    else:
        st.error("PDF not loaded. Cannot answer questions.")

# SIDEBAR: Downloads
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
    st.sidebar.warning("⚠️ Code not found")

st.sidebar.markdown("🔗 [📦 View Dataset on Kaggle](https://www.kaggle.com/datasets/anirudhchauhan/retail-store-inventory-forecasting-dataset/data)")
