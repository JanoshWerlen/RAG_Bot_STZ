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

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

chroma_db = None
chroma_db_PR = None
chroma_db_KAR = None
llm = None


response_file_path = "responses.txt"
pdf_folderpath = "data"


def initialise_AI():

    global pdf_folderpath
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
            if "PR" in file:
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
    chunks_all = text_splitter.split_documents(all_documents)

    print(f"Alle {len(chunks_all)}")
    print(f"KAR {len(chunks_KAR)}")
    print(f"PR {len(chunks_PR)}")

    # Initialize the OpenAI chat model
    print("initialise_llm")
    llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0.8)

    # Check for or create databases
    chroma_db = check_for_db(chunks_all, "chroma_db")
    chroma_db_PR = check_for_db(chunks_PR, "chroma_db_PR")
    chroma_db_KAR = check_for_db(chunks_KAR, "chroma_db_KAR")


def create_timestamp():
    current_timestamp = datetime.timestamp(datetime.now())
    dt_object = datetime.fromtimestamp(current_timestamp)
    formatted_date_time = dt_object.strftime("%d/%m/%Y %H:%M")

    return formatted_date_time


def create_log(timestamp, response):
    from python_code.chat import reduce_history

    # reduced_history = reduce_history(response)

    try:
        with open(response_file_path, "a", encoding="utf-8") as response_file:
            response_file.write(
                f"//{timestamp} \n + {response['query']}\n + {response['result']}\n")
    except Exception as e:
        print(f"An error occurred while writing to the file: {e}")

    print("Response appended to", response_file_path)


def clear_log():
    with open(response_file_path, "w", encoding="utf-8") as response_file:
        # Schreibe nichts in die Datei, um sie zu leeren
        pass

    print("Log-Datei geleert:", response_file_path)


def get_response(query: str, categorie):

    global chroma_db
    global chroma_db_PR
    global chroma_db_KAR
    global llm

    if categorie == "Alle":
        print("Gewählte Ketegorie ALLE")
        chain = RetrievalQA.from_chain_type(
            llm=llm, chain_type="stuff", retriever=chroma_db.as_retriever())
        response = chain.invoke(query)
        # print(response["result"])

        formatted_date_time = create_timestamp()

        create_log(formatted_date_time, response)

        return response["result"]

    elif categorie == "PR":
        print("Gewählte Ketegorie PR")
        chain = RetrievalQA.from_chain_type(
            llm=llm, chain_type="stuff", retriever=chroma_db_PR.as_retriever())
        response = chain.invoke(query)
        # print(response["result"])

        formatted_date_time = create_timestamp()

        create_log(formatted_date_time, response)

        return response["result"]

    elif categorie == "KAR":
        print("Gewählte Ketegorie KAR")
        chain = RetrievalQA.from_chain_type(
            llm=llm, chain_type="stuff", retriever=chroma_db_KAR.as_retriever())
        response = chain.invoke(query)
        # print(response["result"])

        formatted_date_time = create_timestamp()

        create_log(formatted_date_time, response)

        return response["result"]


def get_chroma_db(embeddings, name: str):
    print(f"Loading Chroma ({name})")
    chroma_db = Chroma(persist_directory=name, embedding_function=embeddings)
    return chroma_db


def create_chroma_db(chunks, embeddings, name: str):
    print(f"Creating new Chroma ({name}) with {len(chunks)}")

    chroma_db = Chroma.from_documents(
        chunks, embeddings, persist_directory=name)
    return chroma_db


def check_for_db(chunks, name: str):
    embeddings = OpenAIEmbeddings()
    global chroma_db
    global chroma_db_PR
    global chroma_db_KAR

    if os.path.exists(name):
        print(f"{name} exists")
        if name == "chroma_db":
            chroma_db = get_chroma_db(embeddings, name)
        elif name == "chroma_db_PR":
            chroma_db_PR = get_chroma_db(embeddings, name)
        elif name == "chroma_db_KAR":
            chroma_db_KAR = get_chroma_db(embeddings, name)
    else:
        if name == "chroma_db":
            chroma_db = create_chroma_db(chunks, embeddings, name)
        elif name == "chroma_db_PR":
            chroma_db_PR = create_chroma_db(chunks, embeddings, name)
        elif name == "chroma_db_KAR":
            chroma_db_KAR = create_chroma_db(chunks, embeddings, name)
        print(f"Created {name}")

    if name == "chroma_db":
        return chroma_db
    elif name == "chroma_db_PR":
        return chroma_db_PR
    elif name == "chroma_db_KAR":
        return chroma_db_KAR
