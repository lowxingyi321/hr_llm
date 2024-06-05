from helper_functions import llm
from langchain_community.document_loaders import Docx2txtLoader
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import CharacterTextSplitter, RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain.chains import RetrievalQA
from langchain_openai import ChatOpenAI


# Load
loader = Docx2txtLoader("./data/DRAFT 1_Maternity Leave Information.docx")
docs = loader.load()

# Split and chunk
text_splitter = RecursiveCharacterTextSplitter(
    separators=["\n\n", "\n", " ", ""],
    chunk_size=500,
    chunk_overlap=50,
    length_function=count_tokens
)

splitted_documents = text_splitter.split_documents(docs)

# Storage
embeddings_model = OpenAIEmbeddings(model='text-embedding-3-small')
db = Chroma.from_documents(splitted_documents, embeddings_model, persist_directory="./chroma_db")

# Retrieval
qa_chain = RetrievalQA.from_chain_type(
    ChatOpenAI(model='gpt-3.5-turbo'),
    retriever=db.as_retriever(search_kwargs={"k": 2}),
    return_source_documents=True
)

# Output
response = qa_chain.invoke("Am I eligible for maternity leave if I am not a citizen?")
response