import streamlit as st
import tempfile
from utils.load import load_file
from utils.split import (
    count_word_tokens,
    count_subword_tokens,
    recursive_split,
    viz_subword_token
)
from utility import check_password

### Config
st.set_page_config(page_title="Bot Reading", page_icon="📖")

st.markdown("# Learn how I read")
###

if not check_password():  
    st.stop()

uploaded_file = st.file_uploader("Choose a file", accept_multiple_files=False)

if uploaded_file is not None:

    # Get the file name
    file_name = uploaded_file.name
    st.write(f"Uploaded file: {file_name}")

    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        temp_file.write(uploaded_file.getvalue())
        temp_file_path = temp_file.name

    document = load_file(file_name, temp_file_path)
    document_content = document[0].page_content
    word_count = count_word_tokens(document)
    subword_count = count_subword_tokens(document)

    splitted_documents = recursive_split(document)

    st.markdown("## Your Document")
    st.write(document_content)
    
    st.markdown(f"### Has {word_count} words and {subword_count} subword tokens.")
                
    st.markdown(f"### This is further split into {len(splitted_documents)} smaller documents:")

    splitted_documents_chart = viz_subword_token(splitted_documents)

    st.bar_chart(splitted_documents_chart)
    
    st.markdown(f"### With this chart showing the number of tokens in each document.")
