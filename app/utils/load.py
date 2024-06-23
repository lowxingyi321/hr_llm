from langchain_community.document_loaders import Docx2txtLoader
from langchain_community.document_loaders import TextLoader
from langchain_community.document_loaders import UnstructuredPDFLoader

def load_file(filename, file):

    if filename.endswith(".docx"):
        loader = Docx2txtLoader(file)

    if filename.endswith(".pdf"):
        loader = UnstructuredPDFLoader(file)

    if filename.endswith(".txt"):
        loader = TextLoader(file)

    doc = loader.load() #loader returns a list with 1 document element
    doc[0].metadata['filename'] = doc[0].metadata['source']

    return doc
