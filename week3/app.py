import streamlit as st
from retriever import retrieve

query = st.text_input("Ask a question")
mode = st.selectbox("Retrieval mode", ["hybrid", "embedding", "bm25"])

if st.button("Search"):
    st.write(retrieve(query, mode=mode))