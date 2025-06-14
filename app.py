import streamlit as st
from transformers import pipeline
import fitz  # PyMuPDF

# ----------- PDF LOADER -------------
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

# ----------- QA MODEL -------------
def load_qa_pipeline():
    return pipeline(
        "question-answering",
        model="distilbert-base-cased-distilled-squad",
        tokenizer="distilbert-base-cased-distilled-squad"
    )

# Load PDF text
pdf_text = load_pdf_text("my_report.pdf")
qa = load_qa_pipeline()

# ----------- UI SETUP -------------
st.set_page_config(layout="wide")
st.title("📊 AI-Driven Stockout Risk Optimization Chatbot")

col1, col2 = st.columns(2)

# LEFT: Tableau Dashboard Embed
with col1:
    st.subheader("📈 Interactive Tableau Dashboard")
    st.markdown("""
        <iframe src="https://public.tableau.com/views/AI-DrivenStockoutRiskPredictionforSmarterInventoryManagement/AI-drivenstockoutriskoptimizationforsmarterinventorymanagement?:language=en-US&:display_count=n&:origin=viz_share_link"
        width="100%" height="600" style="border:none;"></iframe>
    """, unsafe_allow_html=True)

# RIGHT: Chatbot Interface
with col2:
    st.subheader("💬 Ask Questions from the PDF Report")
    if pdf_text:
        question = st.text_input("Ask your question:")
        if question:
            try:
                result = qa(question=question, context=pdf_text)
                st.success(result['answer'])
            except Exception as e:
                st.error(f"⚠️ Model error: {e}")
    else:
        st.warning("PDF could not be loaded.")

# ----------- SIDEBAR RESOURCES -------------
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
