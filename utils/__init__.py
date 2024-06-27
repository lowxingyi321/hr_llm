from dotenv import load_dotenv

load_dotenv('.env')

MODEL_DEFAULT = "gpt-4o"
PERSIST_DIRECTORY = "./data/chroma_db"
EMBEDDINGS_MODEL ='text-embedding-3-small'