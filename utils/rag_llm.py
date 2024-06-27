from. import MODEL_DEFAULT, PERSIST_DIRECTORY, EMBEDDINGS_MODEL
from langchain.chains import RetrievalQA
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma

all_policies_collection = Chroma(persist_directory=PERSIST_DIRECTORY,
                                embedding_function=EMBEDDINGS_MODEL,
                                collection_name="all_policies"
                                )

retriever = all_policies_collection.as_retriever(search_type="mmr", 
                                                search_kwargs={"k": 2, "fetch_k":3})

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
        ChatOpenAI(model=MODEL_DEFAULT),
        retriever = retriever,
        return_source_documents=True,
        chain_type_kwargs={"prompt": QA_CHAIN_PROMPT}
    )

    # Output
    response = qa_chain.invoke(query)

    return response