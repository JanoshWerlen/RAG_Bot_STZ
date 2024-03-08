import openai
import os
from dotenv import load_dotenv
from langchain.document_loaders import PyPDFLoader
from langchain.chains import RetrievalQA
from langchain_openai import ChatOpenAI
from langchain_openai import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma

chroma_db = None
llm = None


response_file_path = "responses.txt"

def initialise_AI():
    global chroma_db
    global llm


    print("initialise_text_splitter")
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    loader = PyPDFLoader("data/Personalrecht.pdf")
    chunks = loader.load_and_split(text_splitter)
 
    # Load environment variables from .env file
    load_dotenv()

    # Access the API key using the variable name defined in the .env file
    openai.api_key = os.getenv("OPENAI_API_KEY")

    # Initialize the OpenAI chat model
    print("initialise_llm")
    llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0.8)
    
    embeddings = OpenAIEmbeddings()
    
    if os.path.exists("chroma_db"):
        print("Loading Chroma")
        chroma_db =Chroma(persist_directory="chroma_db", embedding_function= embeddings )
    else: 
        print("Creat new Chroma")
        chroma_db = Chroma.from_documents(chunks, embeddings, persist_directory="chroma_db")
            
        return chroma_db, llm

def get_response(query:str):

    global chroma_db
    global llm

    chain = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=chroma_db.as_retriever())
    response = chain.invoke(query)
    print(response["result"])
    
    
    with open(response_file_path, "a", encoding="utf-8") as response_file:
        response_file.write("// \n"+response["query"] +"\n" +response["result"] +"//"+ "\n")

    print("Response appended to", response_file_path)

    return response["result"]
