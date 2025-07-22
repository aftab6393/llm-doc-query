# 🧠 LLM-powered Document Intelligence System

### Team SuperNova | HackRx 6.0 | G.L. Bajaj Institute of Technology and Management, Greater Noida
Leader Name: Aftab Ansari
---

## 🚀 Overview

This project is built for HackRx 6.0 under the problem statement:

> **"Build a system that uses Large Language Models (LLMs) to process natural language queries and retrieve relevant information from large unstructured documents such as policy documents, contracts, and emails."**

Our solution enables **semantic search** over uploaded documents using state-of-the-art **LLMs + FAISS vector search**, and provides **explainable decision outputs** with structured reasoning.

---

## 🏁 Key Features

- ✅ **Natural Language Query Support**
- 🔍 **Semantic Understanding via LLM (SentenceTransformer)**
- 📂 **Supports PDF, DOCX, and Email (EML) documents**
- 📎 **Clause-level Justification from documents**
- 🧠 **Approves/Rejects queries based on retrieved context**
- 🧾 **Structured JSON Output (Decision, Amount, Reason, ParsedQuery)**

---

## 📦 Tech Stack

| Component        | Technology                         |
|------------------|-------------------------------------|
| Frontend UI      | [Streamlit](https://streamlit.io)   |
| NLP Embeddings   | `sentence-transformers` (MiniLM)    |
| Search Engine    | `FAISS` Vector Indexing             |
| File Parsing     | `PyMuPDF`, `python-docx`, `.eml`    |
| Deployment       | Localhost / Streamlit Sharing       |
| Language         | Python 3.9+                         |

---

## 🧰 Folder Structure

```bash
llm-doc-query/
│
├── app.py                     # Streamlit frontend
├── llm_query_system.py        # Backend logic for processing queries
├── requirements.txt           # All dependencies
├── README.md                  # Project description
├── test_files/                # Sample PDFs or DOCX files (optional)
└── venv/                      # Virtual environment (not included in repo)
