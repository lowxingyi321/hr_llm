import streamlit as st

st.set_page_config(
    page_title="About RAG",
    page_icon="🧐",
)

st.write("# Retrieval Augmented Generation (RAG) 🧐")

st.image('./img/rag.png', caption='Overview of Steps in RAG')

st.sidebar.success("Select a page above.")

st.markdown(
    """
    RAG is the process of retrieving relevant contextual information from a 
    data source and passing that information to a large language model
    alongside the user’s prompt. This information is used to improve the model’s output
    (generated text or images) by augmenting the model’s base knowledge. 

    **👈 Try out the HR Policy Bot from the sidebar** to see it in action!

    ### Want to learn more?
    - Check out the AI Champion Bootcamp
        [notes from Govtech](https://d27l3jncscxhbx.cloudfront.net/topic-4-from-embeddings-to-applications/4.-retrieval-augmented-generation-(rag).html)
    - Visit the 📖 Learning pages in the sidebar
    """
)