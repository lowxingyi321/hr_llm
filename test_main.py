from utils import rag_llm
from create_collections import load_policies

load_policies()
response = rag_llm.respond("Do you work?")
print(response)

store_response = rag_llm.query_store("Tell me about local transport")
print(store_response)