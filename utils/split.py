from . import MODEL_DEFAULT
from langchain_text_splitters import CharacterTextSplitter, RecursiveCharacterTextSplitter
from langchain_experimental.text_splitter import SemanticChunker
import tiktoken
import pandas as pd

def count_tokens(text:str):
    encoding = tiktoken.encoding_for_model(MODEL_DEFAULT)
    return len(encoding.encode(text))

def count_word_tokens(documents:list):

    for doc in documents:
        page_content = doc.page_content
        word_tokens = page_content.split(' ')
    
    return len(word_tokens)

def count_subword_tokens(documents:list):

    for doc in documents:
        page_content = doc.page_content
        subword_tokens = count_tokens(page_content)
    
    return subword_tokens

def viz_subword_token(documents:list):

    subword_token_per_page = []

    for doc in documents:
        page_content = doc.page_content
        subword_token_per_page.append(count_tokens(page_content))

    return pd.Series(subword_token_per_page)
                     
def recursive_split(documents:list):

    text_splitter = RecursiveCharacterTextSplitter(
    separators=["\n\n", "\n", " ", ""],
    chunk_size=500,
    chunk_overlap=50,
    length_function=count_tokens
    )

    splitted_documents = text_splitter.split_documents(documents)

    return splitted_documents