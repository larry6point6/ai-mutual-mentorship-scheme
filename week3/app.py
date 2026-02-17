import streamlit as st
from rag_pipeline import run_query

query = st.text_input("What is your query?")

if st.button("Run query"):
    st.write(run_query(query))