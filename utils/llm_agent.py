from. import MODEL_DEFAULT, PERSIST_DIRECTORY, EMBEDDINGS_MODEL
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain_community.vectorstores import Chroma
from langchain.tools.retriever import create_retriever_tool
from langchain.agents import ( 
    AgentExecutor,
    create_tool_calling_agent,
    create_react_agent,
    create_openai_tools_agent
)

def respond(query):

    # Build custom prompt
    template = """Use the following pieces of context to answer the question at the end. If you don't know the answer, just say that you don't know, don't try to make up an answer.
    Use three sentences maximum. Keep the answer as concise as possible. Always say "thanks for asking!" at the end of the answer.
    {context}
    Question: {question}
    Helpful Answer:"""

    CUSTOM_PROMPT = PromptTemplate.from_template(template)

    maternity_collection = Chroma(persist_directory=PERSIST_DIRECTORY,
                                embedding_function=EMBEDDINGS_MODEL,
                                collection_name="maternity"
                                )
    maternity_retriever = maternity_collection.as_retriever(search_type="mmr", 
                                                            search_kwargs={"k": 2, "fetch_k":3})


    local_transport_collection = Chroma(persist_directory=PERSIST_DIRECTORY,
                                embedding_function=EMBEDDINGS_MODEL,
                                collection_name="local_transport"
                                )
    local_transport_retriever = local_transport_collection.as_retriever(search_type="mmr", 
                                                            search_kwargs={"k": 2, "fetch_k":3})


    overseas_travel_collection = Chroma(persist_directory=PERSIST_DIRECTORY,
                                embedding_function=EMBEDDINGS_MODEL,
                                collection_name="overseas_travel"
                                )
    overseas_travel_retriever = overseas_travel_collection.as_retriever(search_type="mmr", 
                                                            search_kwargs={"k": 2, "fetch_k":3})


    tool_maternity_retriever = create_retriever_tool(
        retriever=maternity_retriever,
        name="maternity_retriever",
        description="Search for information related to maternity leave policy",
    )

    tool_local_transport_retriever = create_retriever_tool(
        retriever=local_transport_retriever,
        name="local_transport_retriever",
        description="Search for information related to local transport policy",
    )

    tool_overseas_travel_retriever = create_retriever_tool(
        retriever=overseas_travel_retriever,
        name="overseas_travel_retriever",
        description="Search for information related to local transport policy",
    )

    # Define the tools which the agent will have access to
    tools = [tool_maternity_retriever, tool_local_transport_retriever,
            tool_overseas_travel_retriever]

    # Define the LLM that "powers" the agent (i.e., the brain)
    llm = ChatOpenAI(model='gpt-3.5-turbo')
    agent_w_info_tools = create_tool_calling_agent(llm, tools, prompt=CUSTOM_PROMPT)
    agent_w_info_executor = AgentExecutor(agent=agent_w_info_tools, tools=tools, verbose=False,
                                max_iterations=10, max_execution_time=None)

    response = agent_w_info_executor.invoke(query)

    return response['output']