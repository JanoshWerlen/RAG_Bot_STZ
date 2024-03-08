
import openai
import os
from dotenv import load_dotenv
from langchain.document_loaders import PyPDFLoader
from langchain.chains import RetrievalQA
from langchain_openai import ChatOpenAI
from langchain_openai import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma


text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
loader = PyPDFLoader("data/Personalrecht.pdf")
chunks = loader.load_and_split(text_splitter)


load_dotenv()

    # Access the API key using the variable name defined in the .env file
openai.api_key = os.getenv("OPENAI_API_KEY")

    # Initialize the OpenAI chat model
llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0.8)

embeddings = OpenAIEmbeddings()

print("updating...")   

chroma_db = Chroma.from_documents(
    documents=chunks,
    embedding=embeddings,
    persist_directory="chroma",
    collection_name="lc_chroma_demo")


print("finished")