import os
from typing import List
from langchain_community.vectorstores import FAISS
from langchain.schema import Document


def build_faiss_from_texts(texts: List[str], embeddings, persist_directory: str = None) -> FAISS:
    docs = [Document(page_content=t) for t in texts]
    store = FAISS.from_documents(docs, embeddings)

    if persist_directory:
        os.makedirs(persist_directory, exist_ok=True)
        store.save_local(persist_directory)

    return store


def load_faiss(persist_directory: str, embeddings) -> FAISS:
    if not os.path.exists(persist_directory):
        raise FileNotFoundError(f"{persist_directory} does not exist")

    return FAISS.load_local(
        persist_directory,
        embeddings,
        allow_dangerous_deserialization=True
    )
