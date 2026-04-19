import os
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from config.config import KB_PATH, FAISS_PATH

def load_kb():
    loader = PyPDFLoader(KB_PATH)
    documents = loader.load()

    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    docs = splitter.split_documents(documents)

    return [doc.page_content for doc in docs]

def create_or_load_db(kb_data):
    embeddings = HuggingFaceEmbeddings()

    if os.path.exists(FAISS_PATH):
        return FAISS.load_local(FAISS_PATH, embeddings, allow_dangerous_deserialization=True)

    db = FAISS.from_texts(kb_data, embeddings)
    db.save_local(FAISS_PATH)
    return db

def retrieve_context(db, query):
    docs = db.similarity_search(query, k=2)
    return " ".join([doc.page_content for doc in docs])
