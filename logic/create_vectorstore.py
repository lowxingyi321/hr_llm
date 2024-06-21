import pandas as pd
from datasets import Dataset
from langchain.prompts import PromptTemplate
from langchain_community.document_loaders import Docx2txtLoader
from langchain_community.document_loaders import TextLoader
from langchain_community.document_loaders import UnstructuredPDFLoader
from langchain_text_splitters import CharacterTextSplitter, RecursiveCharacterTextSplitter
from langchain_experimental.text_splitter import SemanticChunker
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain.chains import RetrievalQA
from langchain_openai import ChatOpenAI
import tiktoken


def count_tokens(text):
    encoding = tiktoken.encoding_for_model(model_default)
    return len(encoding.encode(text))

# Constants
model_default = "gpt-4o"
persist_directory = "../chroma_db"

# Load
file_paths = ["./data/DRAFT 1_Maternity Leave Information.docx",
            #   "./data/local transport policy FAQ.pdf"
              ]

categories = ['mat', 
            #   'tra'
              ]
documents = []

#cleanup
try:
    vectorstore.delete_collection()
except:
    pass
   

for file, category in zip(file_paths, categories):
    
    if file.endswith(".docx"):
      loader = Docx2txtLoader(file)

    if file.endswith(".pdf"):
      loader = UnstructuredPDFLoader(file)
    
    doc = loader.load() #loader returns a list with 1 document element
    doc[0].metadata['filename'] = doc[0].metadata['source']

    # Split and chunk
    text_splitter = RecursiveCharacterTextSplitter(
        separators=["\n\n", "\n", " ", ""],
        chunk_size=500,
        chunk_overlap=50,
        length_function=count_tokens
    )

    splitted_documents = text_splitter.split_documents(doc)

    # Convert to embedding and storage
    embeddings_model = OpenAIEmbeddings(model='text-embedding-3-small')
    vectorstore = Chroma.from_documents(splitted_documents, 
                                        embeddings_model,
                                        persist_directory=persist_directory,
                                        # collection_name=category
                                        )
    print(category)

print('complete')