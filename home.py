import streamlit as st
from utils.archive import rag_llm

# region <--------- Streamlit App Configuration --------->
st.set_page_config(
    layout="centered",
    page_title="Main",
    page_icon = "🤖"
)

# Name 🤖_HR_Policy_Bot

# endregion <--------- Streamlit App Configuration --------->

st.title("HR Policy Bot")

# Ensure session state variables are initialized
if "response" not in st.session_state:
    st.session_state.response = None
if "submitted" not in st.session_state:
    st.session_state.submitted = False

def handle_submit():
    st.session_state.response = rag_llm.respond(query=user_prompt)
    st.session_state.submitted = True

# Form submission
with st.form(key="my_form"):
    user_prompt = st.text_area("Enter your question here", 
                                value="What is maternity leave eligibility?",
                                height=200)
    submit_button = st.form_submit_button(label="Submit", on_click=handle_submit)

# Check if form has been submitted 
if st.session_state.submitted:
    st.write(st.session_state.response['result'])

    # Checkbox to show sources
    show_sources = st.checkbox('Show me sources')

    # Display sources if checkbox is checked
    if show_sources:
        st.write(st.session_state.response)



# Wrong code - learn why

# """
#  The way your code is structured causes the form to be re-evaluated and 
#  potentially overwrites st.session_state.response on each rerun, 
#  which might not persist the desired state.

# To ensure that the response is persisted correctly and to handle the 
# checkbox interaction properly, you need to manage the state more explicitly. 
# Here's a modified version of your code:

# 1. Use a session state flag to track the form submission.
# 2. Separate the response generation from the checkbox interaction.
# """

# if "response" not in st.session_state:
#     st.session_state.response = set()

# with st.form(key="my_form"):
#     st.subheader("Ask me about HR Policies")
#     user_prompt = st.text_area("Enter your question here", 
#                                 value="What is maternity leave eligibility?",
#                                 height=200)



#     if st.form_submit_button("Submit") or st.session_state.response != None:
        
#         #need to persist the true value for submit button
#         st.session_state.response = rag_llm.respond(query=user_prompt)
#         st.write(st.session_state.response['result'])

#         if st.checkbox('Show me sources'):
#             st.write(st.session_state.response)

