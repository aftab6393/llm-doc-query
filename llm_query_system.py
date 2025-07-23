def process_query(query: str, doc_dir: str):
    from sentence_transformers import SentenceTransformer
    import faiss
    import os
    import fitz  # PyMuPDF
    import docx
    import re
    import numpy as np

    # === Document Loader with error handling ===
    def load_documents(path):
        texts = []
        for file in os.listdir(path):
            full_path = os.path.join(path, file)
            try:
                if file.endswith(".pdf"):
                    try:
                        with fitz.open(full_path) as doc:
                            text = " ".join([page.get_text() for page in doc])
                            texts.append((file, text))
                    except Exception as e:
                        print(f"❌ Skipping PDF '{file}' due to MuPDF error: {e}")
                elif file.endswith(".docx"):
                    try:
                        doc = docx.Document(full_path)
                        text = " ".join([p.text for p in doc.paragraphs])
                        texts.append((file, text))
                    except Exception as e:
                        print(f"❌ Skipping DOCX '{file}' due to error: {e}")
                elif file.endswith(".eml"):
                    try:
                        with open(full_path, "r", encoding="utf8", errors="ignore") as f:
                            texts.append((file, f.read()))
                    except Exception as e:
                        print(f"❌ Skipping EML '{file}' due to error: {e}")
            except Exception as e:
                print(f"⚠️ General error while reading '{file}': {e}")
        return texts

    # === Text chunking ===
    def chunk_text(text, chunk_size=500):
        words = text.split()
        return [" ".join(words[i:i + chunk_size]) for i in range(0, len(words), chunk_size)]

    # === Embedding ===
    def embed_chunks(chunks):
        return model.encode(chunks, convert_to_numpy=True)

    # === Semantic Search ===
    def search(query, index, chunks):
        q_embed = model.encode([query])
        D, I = index.search(q_embed, k=3)
        return [chunks[i] for i in I[0]]

    # === Query Parser ===
    def parse_query(query):
        age_match = re.search(r"(\d+)[ -]?(?:year|yo)?[ -]?(?:old)?", query)
        duration_match = re.search(r"(\d+)[ -]?(month|day|year)", query)
        location = re.findall(r"in (\w+)", query)
        procedure = re.findall(r"(knee|heart|surgery|operation|replacement)", query, re.IGNORECASE)

        return {
            "age": age_match.group(1) if age_match else None,
            "location": location[0] if location else None,
            "procedure": procedure[0] if procedure else None,
            "duration": f"{duration_match.group(1)} {duration_match.group(2)}" if duration_match else None
        }

    # === Load Model ===
    model = SentenceTransformer('all-MiniLM-L6-v2')

    # === Load and prepare documents ===
    docs = load_documents(doc_dir)
    all_chunks, sources = [], []
    for name, text in docs:
        for chunk in chunk_text(text):
            all_chunks.append(chunk)
            sources.append(name)

    # === FAISS Index ===
    embeddings = embed_chunks(all_chunks)
    dim = embeddings.shape[1]
    index = faiss.IndexFlatL2(dim)
    index.add(embeddings)

    # === Run semantic search ===
    query_info = parse_query(query)
    retrieved_chunks = search(query, index, all_chunks)

    if retrieved_chunks:
        justification = max(
            retrieved_chunks,
            key=lambda x: x.lower().count(query_info["procedure"].lower()) if query_info["procedure"] else 0
        )
    else:
        justification = "Not found"

        # Improved approval check
    approval_keywords = ["covered", "eligible", "included", "reimbursed", "payable"]
    rejection_keywords = ["not covered", "excluded", "not payable", "excluded from policy"]

    is_approved = any(kw in justification.lower() for kw in approval_keywords) and not any(kw in justification.lower() for kw in rejection_keywords)

    # 🔍 DEBUG LINES
    print("🔍 Justification Chunk:", justification)
    print("✅ Approval Check:", is_approved)

    return {
        "Decision": "Approved" if is_approved else "Rejected",
        "Amount": "₹50,000" if is_approved else "₹0",
        "Justification": justification[:1000] + "..." if len(justification) > 1000 else justification,
        "ParsedQuery": query_info
    }

