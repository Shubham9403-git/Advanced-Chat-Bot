import asyncio
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from config.settings import GOOGLE_API_KEY
from langchain_community.embeddings import HuggingFaceEmbeddings


def get_chat_llm(model="gemini-1.5-flash", temperature=0.3):
    try:
        asyncio.get_running_loop()
    except RuntimeError:
        asyncio.set_event_loop(asyncio.new_event_loop())

    return ChatGoogleGenerativeAI(
        model=model,
        temperature=temperature,
        google_api_key=GOOGLE_API_KEY,
    )


#def get_embeddings_provider(model="models/embedding-001"):
    """Return Google Gemini embeddings provider"""
    return GoogleGenerativeAIEmbeddings(
        model=model,
        google_api_key=GOOGLE_API_KEY,
    )


def get_embeddings_provider():
    return HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")


