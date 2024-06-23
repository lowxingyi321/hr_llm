from langchain.chains import RetrievalQA
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
import config
from dotenv import load_dotenv

load_dotenv('.env')

model_default = config.MODEL_DEFAULT
persist_directory = config.PERSIST_DIRECTORY
embeddings_model = config.EMBEDDINGS_MODEL

embeddings_model = OpenAIEmbeddings(model=embeddings_model)

loaded_vectorstore = Chroma(persist_directory=persist_directory,
                            embedding_function=embeddings_model,
                            collection_name="maternity"
                            )

retriever = loaded_vectorstore.as_retriever()

def similarity_search(query):
    
    retriever = loaded_vectorstore.as_retriever()
    response = retriever.invoke(query)

    return response

def respond(query):

    # Build custom prompt
    template = """Use the following pieces of context to answer the question at the end. If you don't know the answer, just say that you don't know, don't try to make up an answer.
    Use three sentences maximum. Keep the answer as concise as possible. Always say "thanks for asking!" at the end of the answer.
    {context}
    Question: {question}
    Helpful Answer:"""
    QA_CHAIN_PROMPT = PromptTemplate.from_template(template)

    # Retrieval
    qa_chain = RetrievalQA.from_chain_type(
        ChatOpenAI(model=model_default),
        retriever = retriever,
        return_source_documents=True,
        chain_type_kwargs={"prompt": QA_CHAIN_PROMPT}
    )

    # Output
    response = qa_chain.invoke(query)

    return response