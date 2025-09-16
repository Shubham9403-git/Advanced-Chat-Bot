from src.pdf_loader import extract_text_from_pdf
from src.text_processing import chunk_text
from src.vectorstore import build_faiss_from_texts
from src.llm import get_embeddings_provider, get_chat_llm
from langchain.chains import RetrievalQA
import os

def create_index_from_pdf(pdf_path: str, persist_dir: str = None, chunk_size=1000, chunk_overlap=200):
    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"{pdf_path} not found.")
    
    raw = extract_text_from_pdf(pdf_path)
    chunks = chunk_text(raw, chunk_size, chunk_overlap)
    embeddings = get_embeddings_provider()
    return build_faiss_from_texts(chunks, embeddings, persist_directory=persist_dir)

def build_qa_chain_from_store(store, llm=None, k=3):
    if llm is None:
        llm = get_chat_llm()
    retriever = store.as_retriever(search_kwargs={"k": k})
    return RetrievalQA.from_chain_type(llm=llm, retriever=retriever, return_source_documents=True)

def ask_from_data(user_question: str, pdf_path: str, persist_dir="faiss_index"):
    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"{pdf_path} not found.")
    
    store = create_index_from_pdf(pdf_path, persist_dir)
    qa = build_qa_chain_from_store(store)
    return qa(user_question)
