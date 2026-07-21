import streamlit as st
from rag import search_and_response, init_db

@st.cache_resource
def setup():
    init_db()

setup()

st.title("Chess RAG")
q = st.text_input("Question")

if q:
    st.write(search_and_response(q))

