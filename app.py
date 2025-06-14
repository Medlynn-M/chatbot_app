import streamlit as st
import fitz  # PyMuPDF
import os
import google.generativeai as genai

# --- CONFIGURE API KEY ---
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])  # Store key in Streamlit secrets

# --- PDF LOADER FUNCTION ---
def load_pdf_text(pdf_path):
    text = ""
    try:
        doc = fitz.open(pdf_path)
        for page in doc:
            text += page.get_text()
        return text
    except Exception as e:
        st.error(f"❌ Failed to load PDF: {e}")
        return ""

# --- LOAD PDF REPORT ---
pdf_text = load_pdf_text("my_report.pdf")

# --- Streamlit Page Setup ---
st.set_page_config(layout="wide")
st.title("📊 AI Chatbot for Stockout Risk Optimization Project")

# --- Layout: Tableau Dashboard + Chatbot ---
col1, col2 = st.columns(2)

with col1:
    st.subheader("📈 Tableau Dashboard")
    st.markdown("""
        <iframe src="https://public.tableau.com/views/AI-DrivenStockoutRiskPredictionforSmarterInventoryManagement/AI-drivenstockoutriskoptimizationforsmarterinventorymanagement?:language=en-US&:display_count=n&:origin=viz_share_link"
        width="100%" height="600" style="border:none;"></iframe>
    """, unsafe_allow_html=True)

with col2:
    st.subheader("🤖 Ask Questions About the Report")
    user_input = st.text_input("Ask your question:")
    
    if user_input and pdf_text:
        try:
            model = genai.GenerativeModel("gemini-pro")
            prompt = f"""You are an assistant reading a project report. Use the below content to answer questions:

            --- Start of Report Content ---
            {pdf_text[:8000]}  # Limiting to 8k chars to stay within Gemini limits
            --- End of Report Content ---

            Question: {user_input}
            Answer:"""
            response = model.generate_content(prompt)
            st.success(response.text)
        except Exception as e:
            st.error(f"⚠️ Gemini Error: {e}")

# --- Sidebar Resources ---
st.sidebar.title("📂 Project Files")

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
