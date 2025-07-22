import streamlit as st
import os
import tempfile
from llm_query_system import process_query

st.set_page_config(page_title="📄 Smart Document Query System", layout="centered")

st.markdown("""
    <h1 style='text-align: center; color: #4CAF50;'>📄 LLM-powered Document Intelligence System</h1>
    <p style='text-align: center;'>Query large policy or contract documents using natural language</p>
""", unsafe_allow_html=True)

st.sidebar.markdown("### 📁 Upload Documents")

uploaded_files = st.sidebar.file_uploader(
    "Upload PDFs, Word, or EML files",
    type=["pdf", "docx", "eml"],
    accept_multiple_files=True,
    help="Supported formats: .pdf, .docx, .eml"
)

# === File Handling ===
if uploaded_files:
    docs_dir = tempfile.mkdtemp()
    for f in uploaded_files:
        with open(os.path.join(docs_dir, f.name), "wb") as out:
            out.write(f.read())
    st.sidebar.success(f"✅ {len(uploaded_files)} file(s) uploaded.")
else:
    docs_dir = "data"
    st.sidebar.info("📂 No uploads yet. Using documents from 'data/' folder.")

# === Query Section ===
st.markdown("---")
st.subheader("🔍 Enter Your Query")
query = st.text_input("e.g., 46-year-old male, knee surgery in Pune, 3-month-old policy")

# === Analyze Button with Custom Style ===
st.markdown("""
    <style>
    div.stButton > button:first-child {
        background-color: #4CAF50;
        color: white;
        border-radius: 8px;
        height: 3em;
        width: 100%;
        font-size: 16px;
    }
    </style>
""", unsafe_allow_html=True)

if st.button("🧠 Analyze Query", key="analyze_button"):
    if query:
        with st.spinner("🔎 Analyzing the query..."):
            result = process_query(query, docs_dir)
        st.success("✅ Analysis Complete!")

        # === Show Results in a Container ===
        with st.expander("📋 View Result"):
            st.markdown(f"""
                <div style="background-color:#f9f9f9;padding:15px;border-radius:10px;">
                <b>🧾 Decision:</b> <span style="color:{'green' if result['Decision']=='Approved' else 'red'};">{result['Decision']}</span><br>
                <b>💰 Amount:</b> {result['Amount']}<br>
                <b>📌 Justification:</b> <br><code>{result['Justification'][:1500]}</code><br>
                <b>🔎 Parsed Query:</b> {result['ParsedQuery']}
                </div>
            """, unsafe_allow_html=True)
    else:
        st.warning("⚠️ Please enter a query.")
