from langchain_community.document_loaders import Docx2txtLoader
from langchain_community.document_loaders import TextLoader
from langchain_community.document_loaders import UnstructuredPDFLoader
from langchain_text_splitters import CharacterTextSplitter, RecursiveCharacterTextSplitter
from langchain_experimental.text_splitter import SemanticChunker
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
import tiktoken
import os
import config

model_default = config.MODEL_DEFAULT
persist_directory = config.PERSIST_DIRECTORY
embeddings_model = config.EMBEDDINGS_MODEL

# Load
file_paths = ["./data/DRAFT 1_Maternity Leave Information.docx",
            #   "./data/local transport policy FAQ.pdf"
              ]

collection_names = ['maternity', 
            #   'transport'
              ]

def count_tokens(text):
    encoding = tiktoken.encoding_for_model(model_default)
    return len(encoding.encode(text))

def create_chroma_db(file_paths, collection_names):

  for file, name in zip(file_paths, collection_names):
      
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
      embeddings_model = OpenAIEmbeddings(model=embeddings_model)
      vectorstore = Chroma.from_documents(splitted_documents, 
                                          embeddings_model,
                                          persist_directory=persist_directory,
                                          collection_name=name
                                          )
      
def clean_up():
  try:
      vectorstore.delete_collection()
  except:
      pass
  print('Vectorstore deleted')

def main():
   
  if not os.path.isdir(persist_directory):
    create_chroma_db(file_paths, collection_names)
    print('Chromadb created')

  print('ETL completed')

if __name__ == "__main__":
   main()