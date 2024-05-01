#Import Libraries
from langchain_community.document_loaders import WebBaseLoader
from langchain_text_splitters import CharacterTextSplitter
from langchain_chroma import Chroma
from langchain_openai import AzureOpenAIEmbeddings
import os
from dotenv import load_dotenv
load_dotenv()

#Specify URL's to chunk and embedd
loader = WebBaseLoader(["https://docs.smith.langchain.com/tracing/concepts", "https://docs.smith.langchain.com/cookbook"])
data = loader.load()

#Split documents into 1000 character chunks with no overlap
text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
docs = text_splitter.split_documents(data)

#Bring in Azure OpenAI Embeddings Config
embedding_function = AzureOpenAIEmbeddings(
    azure_deployment="embeddings",
    openai_api_version="2023-05-15",
    api_key=os.getenv("AZURE_OPENAI_API_KEY")
)

#Add documents to chromadb
Chroma.from_documents(docs, embedding_function, persist_directory="./chroma_db")