# 📘 AI PDF Chatbot

An interactive chatbot built with **Streamlit**, **LangChain**, **FAISS**, and **Google Gemini API**.  
Upload any PDF and chat with it — the app extracts the text, creates vector embeddings, and answers your questions using Gemini + retrieval.

---

## 🚀 Features
- Upload **any PDF** via sidebar
- PDF text is chunked & indexed in **FAISS**
- Ask natural questions about the content
- Answers generated with **Google Gemini (via LangChain)**
- Chat history stored during the session
- Clean and modern **Streamlit UI**

---

## 📂 Project Structure
├── app.py # Main Streamlit app
├── config/
│ └── settings.py # Loads GOOGLE_API_KEY from .env
├── src/
│ ├── pipeline.py # Indexing, QA pipeline
│ ├── pdf_loader.py # PDF text extraction
│ ├── text_processing.py # Cleaning & chunking
│ ├── vectorstore.py # FAISS vector DB utilities
│ └── llm.py # LLM + embeddings providers
├── data/ # Uploaded PDFs will be stored here
├── faiss_index/ # Persisted FAISS vector store
├── requirements.txt
└── README.md
|___.env


---

## ⚙️ Installation

1. **Clone the repo**
   ```bash
   git clone https://github.com/Shubham9403-git/Advanced-Chat-Bot.git
   cd pdf-chatbot

2. **Create a virtual environment

python -m venv venv
source venv/bin/activate   # macOS/Linux
venv\Scripts\activate      # Windows


3. **Install dependencies

pip install -r requirements.txt


4. **Set up environment variables
Create a .env file in the project root:
GOOGLE_API_KEY=your_google_api_key_here


▶️ Running the App
Start the Streamlit app:
streamlit run app.py


📖 Usage

Upload a PDF from the sidebar
Wait for processing (text extraction + FAISS indexing)
Ask questions in the chat box
Get answers grounded in your document


🛠️ Tech Stack

Streamlit
 – Web UI
LangChain
 – Orchestration
FAISS
 – Vector database
Google Gemini
 – LLM & embeddings
PyPDF
 – PDF text extraction

 
⚠️ Notes

Requires a Google API key for Gemini models
Currently supports one PDF at a time
All uploaded PDFs are stored in the data/ folder

📌 Roadmap

 Support multiple PDFs in one session
 Add persistent chat history
 Add support for non-PDF formats (DOCX, TXT)
 Deploy to cloud (Streamlit Community Cloud, Hugging Face Spaces, etc.)

📜 License

MIT License © 2025

