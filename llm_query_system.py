def process_query(query: str, doc_dir: str):
    from sentence_transformers import SentenceTransformer
    import faiss
    import os
    import fitz  # PyMuPDF
    import docx
    import re
    import numpy as np

    # Load PDF, Word, and Email documents from directory
    def load_documents(path):
        texts = []
        for file in os.listdir(path):
            full_path = os.path.join(path, file)
            if file.endswith(".pdf"):
                doc = fitz.open(full_path)
                text = " ".join([page.get_text() for page in doc])
                texts.append((file, text))
            elif file.endswith(".docx"):
                doc = docx.Document(full_path)
                text = " ".join([p.text for p in doc.paragraphs])
                texts.append((file, text))
            elif file.endswith(".eml"):
                with open(full_path, "r", encoding="utf8", errors="ignore") as f:
                    texts.append((file, f.read()))
        return texts

    # Split text into manageable chunks
    def chunk_text(text, chunk_size=500):
        words = text.split()
        return [" ".join(words[i:i+chunk_size]) for i in range(0, len(words), chunk_size)]

    # Create sentence embeddings
    def embed_chunks(chunks):
        embeddings = model.encode(chunks, convert_to_numpy=True)
        return embeddings

    # Search for top-k relevant chunks
    def search(query, index, chunks):
        q_embed = model.encode([query])
        D, I = index.search(q_embed, k=3)
        return [chunks[i] for i in I[0]]

    # Parse the user query for structured information
    def parse_query(query):
        age_match = re.search(r"(\d+)[ -]?(?:year|yo)?[ -]?(?:old)?", query)
        duration_match = re.search(r"(\d+)[ -]?(month|day|year)", query)
        location = re.findall(r"in (\w+)", query)
        procedure = re.findall(r"(knee|heart|surgery|operation|replacement)", query)

        return {
            "age": age_match.group(1) if age_match else None,
            "location": location[0] if location else None,
            "procedure": procedure[0] if procedure else None,
            "duration": f"{duration_match.group(1)} {duration_match.group(2)}" if duration_match else None
        }

    # Load Sentence Transformer
    model = SentenceTransformer('all-MiniLM-L6-v2')

    # Load and chunk all documents
    docs = load_documents(doc_dir)
    all_chunks, sources = [], []
    for name, text in docs:
        for chunk in chunk_text(text):
            all_chunks.append(chunk)
            sources.append(name)

    # Build FAISS index
    embeddings = embed_chunks(all_chunks)
    dim = embeddings.shape[1]
    index = faiss.IndexFlatL2(dim)
    index.add(embeddings)

    # Parse and search
    query_info = parse_query(query)
    retrieved = search(query, index, all_chunks)
    justification = retrieved[0] if retrieved else "Not found"
    approved = "covered" in justification.lower() or "eligible" in justification.lower()

    # Return structured result
    return {
        "Decision": "Approved" if approved else "Rejected",
        "Amount": "₹50,000" if approved else "₹0",
        "Justification": justification,
        "ParsedQuery": query_info
    }
