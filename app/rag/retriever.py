import os
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

# --- Paths (absolute + safe) ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))      # .../BeanOrbit/app/rag
FAISS_DIR = os.path.join(BASE_DIR, "faiss_index")          # .../BeanOrbit/app/rag/faiss_index

# --- Embeddings (MUST MATCH ingest.py) ---
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# --- Load FAISS index ---
if not os.path.exists(FAISS_DIR):
    raise Exception(f"FAISS index folder not found: {FAISS_DIR}. Run: python3 app/rag/ingest.py")

vectorstore = FAISS.load_local(
    FAISS_DIR,
    embeddings,
    allow_dangerous_deserialization=True
)

def retrieve_docs(query: str, k: int = 3):
    """
    Return top-k relevant document chunks from FAISS.
    """
    return vectorstore.similarity_search(query, k=k)
