from. import MODEL_DEFAULT, PERSIST_DIRECTORY, EMBEDDINGS_MODEL
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings

def create_vectorstore(splitted_documents, collection_name):
    embeddings_model = OpenAIEmbeddings(model=EMBEDDINGS_MODEL)
    collection = Chroma.from_documents(splitted_documents, 
                                        embeddings_model,
                                        persist_directory=PERSIST_DIRECTORY,
                                        collection_name=collection_name
                                        )
    return collection