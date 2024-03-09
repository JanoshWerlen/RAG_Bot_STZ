import openai
import os
from dotenv import load_dotenv
from langchain.document_loaders import PyPDFLoader
from langchain.chains import RetrievalQA
from langchain_openai import ChatOpenAI
from langchain_openai import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma
from datetime import datetime

from bots_code.bots import create_chroma_db

chroma_db = None
chroma_db_PR = None
chroma_db_KAR = None
llm = None


response_file_path = "responses.txt"
pdf_folderpath = "data"

def initialise_AI():
    global chroma_db
    global chroma_db_PR
    global chroma_db_KAR
    global llm

    print("initialise_text_splitter")

    documents_PR = []
    documents_KAR = []

    for file in os.listdir(pdf_folderpath):
        if file.endswith('.pdf'):
            pdf_path = os.path.join(pdf_folderpath, file)
            loader = PyPDFLoader(pdf_path)
            if "Personalrecht" in file:
                documents_PR.extend(loader.load())
            elif "KAR" in file:
                documents_KAR.extend(loader.load())

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000, chunk_overlap=100)

    print(f"PR documents: {len(documents_PR)}")
    print(f"KAR documents: {len(documents_KAR)}")

    # Split documents
    chunks_PR = text_splitter.split_documents(documents_PR)
    chunks_KAR = text_splitter.split_documents(documents_KAR)

    # Combine all documents for the general database
    all_documents = documents_PR + documents_KAR
    all_chunks = text_splitter.split_documents(all_documents)

    # Load environment variables from .env file
    load_dotenv()

    # Access the API key using the variable name defined in the .env file
    openai.api_key = os.getenv("OPENAI_API_KEY")

    # Initialize the OpenAI chat model
    print("initialise_llm")
    llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0.8)

    # Check for or create databases
    if name == "chroma_db":
            chroma_db = create_chroma_db(all_chunks, embeddings, name)
        elif name == "chroma_db_PR":
            chroma_db_PR = create_chroma_db(all_chunks, embeddings, name)
        elif name == "chroma_db_KAR":
            chroma_db_KAR = create_chroma_db(all_chunks, embeddings, name)
        print(f"Created {name}")
            
