import streamlit as st
import tempfile
from utils.load import load_file

### Config
st.set_page_config(page_title="Bot Reading", page_icon="📖")

st.markdown("# Learn how I read")
###

uploaded_file = st.file_uploader("Choose a file", accept_multiple_files=False)

if uploaded_file is not None:

    # Get the file name
    file_name = uploaded_file.name
    st.write(f"Uploaded file: {file_name}")

    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        temp_file.write(uploaded_file.getvalue())
        temp_file_path = temp_file.name

    document = load_file(file_name, temp_file_path)

    st.markdown("## Your Document")
    st.write(document[0].page_content)
