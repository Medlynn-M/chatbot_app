import streamlit as st
import os
from dotenv import load_dotenv
from langchain_openai import OpenAI
from langchain.document_loaders import PyPDFLoader
from langchain.chains.question_answering import load_qa_chain

# Load API key: from .env locally or st.secrets on Streamlit Cloud
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

if not api_key and "OPENAI_API_KEY" in st.secrets:
    api_key = st.secrets["OPENAI_API_KEY"]

if not api_key:
    st.error("❌ OPENAI_API_KEY not found. Please check your .env file (for local) or Streamlit Secrets (for deployment).")
    st.stop()

# Load your report PDF
try:
    loader = PyPDFLoader("my_report.pdf")
    documents = loader.load()
except Exception as e:
    st.error(f"❌ Failed to load PDF: {e}")
    st.stop()

# Initialize OpenAI and LangChain
llm = OpenAI(temperature=0.2, openai_api_key=api_key)
chain = load_qa_chain(llm, chain_type="stuff")

# Streamlit Layout
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

# RIGHT: Chatbot Q&A
with col2:
    st.subheader("💬 Ask Questions from the PDF Report")
    question = st.text_input("Ask your question:")
    if question:
        try:
            answer = chain.run(input_documents=documents, question=question)
            st.success(answer)
        except Exception as e:
            st.error(f"⚠️ Error: {e}")

# SIDEBAR: Resources
st.sidebar.title("📂 Project Resources")

try:
    with open("my_report.pdf", "rb") as f:
        st.sidebar.download_button("📄 Download Report", f, file_name="my_report.pdf")
except:
    st.sidebar.warning("⚠️ PDF not found")

try:
    with open("my_data.xlsx", "rb") as f:
        st.sidebar.download_button("📊 Download Dataset", f, file_name="my_data.xlsx")
except:
    st.sidebar.warning("⚠️ Dataset not found")

try:
    with open("your_code.py", "rb") as f:
        st.sidebar.download_button("🐍 Download Code", f, file_name="your_code.py")
except:
    st.sidebar.warning("⚠️ Code file not found")

st.sidebar.markdown("🔗 [📦 View Dataset on Kaggle](https://www.kaggle.com/datasets/anirudhchauhan/retail-store-inventory-forecasting-dataset/data)")
