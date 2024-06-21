# Set up and run this Streamlit App

import streamlit as st
from logic import rag_response


# region <--------- Streamlit App Configuration --------->
st.set_page_config(
    layout="centered",
    page_title="My Streamlit App"
)
# endregion <--------- Streamlit App Configuration --------->

st.title("Streamlit App")

form = st.form(key="form")
form.subheader("Prompt")

user_prompt = form.text_area("Enter your prompt here", height=200)

if form.form_submit_button("Submit"):

    # response = llm.get_completion(user_prompt)
    response = rag_response.respond(query=user_prompt)
    similar_search = rag_response.similarity_search(query=user_prompt)
    st.text(f"User prompt: {user_prompt}")
    st.write(response)
    st.write(similar_search)