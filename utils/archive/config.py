model_default = utils.config.MODEL_DEFAULT
persist_directory = utils.config.PERSIST_DIRECTORY
embeddings_model = utils.config.EMBEDDINGS_MODEL

embeddings_model = OpenAIEmbeddings(model=embeddings_model)

client = chromadb.PersistentClient(path="chroma_db")

loaded_vectorstore = Chroma(persist_directory=persist_directory,
                            embedding_function=embeddings_model,
                            collection_name="maternity"
                            )

retriever = loaded_vectorstore.as_retriever()