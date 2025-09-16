import os
import asyncio
import streamlit as st
import traceback
from src.pipeline import create_index_from_pdf, build_qa_chain_from_store, ask_from_data
from config.settings import GOOGLE_API_KEY


try:
    asyncio.get_running_loop()
except RuntimeError:
    asyncio.set_event_loop(asyncio.new_event_loop())

st.set_page_config(page_title="AI PDF Chatbot", layout="wide")

st.markdown(
    """
    <style>
        .stApp {
            background-color: #f9fafb;
            font-family: "Segoe UI", sans-serif;
        }

        .stChatMessage {
            padding: 12px;
            border-radius: 12px;
            margin-bottom: 12px;
        }

        .stChatMessage.user {
            background-color: #dbeafe;
            border: 1px solid #93c5fd;
        }

        .stChatMessage.assistant {
            background-color: #f3f4f6;
            border: 1px solid #e5e7eb;
        }

        h1 {
            text-align: center;
            font-size: 2rem;
            color: #1f2937;
        }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("PDF Chatbot")
st.caption("Upload your PDF and start chatting below!")

with st.sidebar:
    st.header("📂 PDF Controls")

    if not GOOGLE_API_KEY or GOOGLE_API_KEY.strip() == "":
        st.error("GOOGLE_API_KEY missing. Add it in your `.env` file.")
        st.stop()

    uploaded_file = st.file_uploader("Upload a PDF", type=["pdf"])

    if st.button("Clear Chat History"):
        st.session_state.chat_history = []
        st.success("Chat history cleared!")

if uploaded_file:
    os.makedirs("data", exist_ok=True)
    pdf_path = os.path.join("data", uploaded_file.name)

    with open(pdf_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    st.sidebar.success(f"Uploaded: {uploaded_file.name}")

    if "store" not in st.session_state or st.session_state.get("last_file") != pdf_path:
        with st.spinner("Processing PDF... Please wait."):
            try:
                store = create_index_from_pdf(
                    pdf_path=pdf_path,
                    persist_dir="faiss_index",
                    chunk_size=1000,
                    chunk_overlap=200
                )
                st.session_state.store = store
                st.session_state.qa = build_qa_chain_from_store(store)
                st.session_state.last_file = pdf_path
            except Exception as e:
                st.error(f"⚠️ Failed to process PDF: {e}")
                st.stop()

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []


for role, msg in st.session_state.chat_history:
    with st.chat_message(role):
        st.markdown(msg)

if uploaded_file and (question := st.chat_input("Ask about your PDF...")):
    st.session_state.chat_history.append(("user", question))
    with st.chat_message("user"):
        st.markdown(question)

    with st.chat_message("assistant"):
        with st.spinner("⏳ Thinking..."):
            try:
                res = ask_from_data(
                    user_question=f"{question}\n\nFormat the answer naturally, "
                                  f"but use bullet points ONLY for key facts, lists, or important items. "
                                  f"Keep introductory/context sentences as normal text.",
                    pdf_path=st.session_state.last_file,
                    persist_dir="faiss_index"
                )
                answer = res.get("result") if isinstance(res, dict) else str(res)
            except Exception as e:
                answer = f"⚠️ Error: {str(e)}"
                print(traceback.format_exc())

        st.markdown(answer)
        st.session_state.chat_history.append(("assistant", answer))
