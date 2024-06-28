import os
import itertools
from utils import PERSIST_DIRECTORY
from utils.load import load_file
from utils.split import recursive_split
from utils.store import create_vectorstore


file_names = [
    "DRAFT 1_Maternity Leave Information.docx",
    "Local Transport Policy Draft.docx",
    "Overseas Travel Policy.docx"
]

file_paths = [
    "./data/DRAFT 1_Maternity Leave Information.docx",
    "./data/Local Transport Policy Draft.docx",
    "./data/Overseas Travel Policy.docx"
]

documents = []

collection_names = [
    "maternity",
    "local_transport",
    "overseas_travel"
]

full_collection_name = "all_policies"
all_split_documents = []

if not os.path.isdir(PERSIST_DIRECTORY):

    for file_name, file_path in zip(file_names, file_paths):
        document = load_file(file_name, file_path)
        document_content = document[0].page_content
        documents.append(document)

    for document, collection_name in zip(documents, collection_names):

        splitted_documents = recursive_split(document)
        collection = create_vectorstore(splitted_documents, collection_name)
        print(f'{collection_name} vectorstore created')
        all_split_documents.append(splitted_documents)

    full_split_documents = list(itertools.chain.from_iterable(all_split_documents))
    full_collection = create_vectorstore(full_split_documents, full_collection_name)
    print(f'{full_collection_name} vectorstore created')

def load_policies():

    success = 'Policies Loaded'
    print(success)
    return success


