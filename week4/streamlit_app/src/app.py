import os
import requests
import streamlit as st

RETRIEVAL_URL = os.getenv("RETRIEVAL_URL", "http://haystack-api:8000/query")

st.set_page_config(page_title="RAG Demo", layout="wide")
st.title("RAG Query")

query = st.text_input("Enter your question:")

if st.button("Ask") and query.strip():
    with st.spinner("Querying..."):
        resp = requests.post(RETRIEVAL_URL, json={"query": query}, timeout=120)

    if resp.status_code != 200:
        st.error(f"Error: {resp.status_code} - {resp.text}")
    else:
        data = resp.json()
        st.subheader("Answer")
        st.write(data.get("answer", ""))

        docs = data.get("documents", [])
        if docs:
            st.subheader("Retrieved Documents")
            for i, d in enumerate(docs, 1):
                with st.expander(f"Document {i}"):
                    st.write(d.get("content", ""))
                    st.caption(d.get("meta", {}))