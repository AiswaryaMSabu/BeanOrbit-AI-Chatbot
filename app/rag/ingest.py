import os
from langchain_community.document_loaders import PyPDFLoader, CSVLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings

# ----------------------------
# Paths (absolute, safe)
# ----------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))              # .../BeanOrbit/app/rag
PROJECT_ROOT = os.path.abspath(os.path.join(BASE_DIR, "../.."))    # .../BeanOrbit
DOCUMENTS_DIR = os.path.join(PROJECT_ROOT, "documents")            # .../BeanOrbit/documents
FAISS_DIR = os.path.join(BASE_DIR, "faiss_index")                  # .../BeanOrbit/app/rag/faiss_index

# ----------------------------
# Load documents
# ----------------------------
docs = []

if not os.path.exists(DOCUMENTS_DIR):
    raise FileNotFoundError(f"Documents folder not found at: {DOCUMENTS_DIR}")

for file in os.listdir(DOCUMENTS_DIR):
    file_path = os.path.join(DOCUMENTS_DIR, file)

    if file.lower().endswith(".pdf"):
        loader = PyPDFLoader(file_path)
        docs.extend(loader.load())

    elif file.lower().endswith(".csv"):
        loader = CSVLoader(file_path)
        docs.extend(loader.load())

    elif file.lower().endswith(".txt"):
        loader = TextLoader(file_path, encoding="utf-8")
        docs.extend(loader.load())

print(f"Loaded {len(docs)} documents from {DOCUMENTS_DIR}")

if len(docs) == 0:
    raise Exception("No documents found. Add at least 2 PDFs + 1 CSV in /documents")

# ----------------------------
# Split documents into chunks
# ----------------------------
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=80
)
split_docs = text_splitter.split_documents(docs)
print(f"Split into {len(split_docs)} chunks")

# ----------------------------
# Embeddings (MUST MATCH retriever.py)
# ----------------------------
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# ----------------------------
# Create and save FAISS index
# ----------------------------
if os.path.exists(FAISS_DIR):
    # Clean old index to avoid mismatch issues
    for f in os.listdir(FAISS_DIR):
        os.remove(os.path.join(FAISS_DIR, f))
else:
    os.makedirs(FAISS_DIR, exist_ok=True)

vectorstore = FAISS.from_documents(split_docs, embeddings)
vectorstore.save_local(FAISS_DIR)

print(f"FAISS index saved successfully at: {FAISS_DIR}")
