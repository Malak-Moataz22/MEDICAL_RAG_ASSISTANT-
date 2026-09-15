import streamlit as st
import requests
import os

API_BASE_URL = os.getenv("API_BASE_URL", "http://127.0.0.1:8000")

st.set_page_config(page_title="Medical RAG Assistant", page_icon="🧠", layout="centered")

st.title("🧠 Medical RAG Assistant")
st.write("Ask any question related to the medical documents, and the assistant will retrieve the answer for you.")

query = st.text_input("Enter your question here:")

if st.button("Generate Answer"):
    if query.strip():
        with st.spinner("Searching documents and generating response..."):
            try:
                response = requests.post(
                    f"{API_BASE_URL}/api/query",
                    json={"question": query}
                )
                if response.status_code == 200:
                    data = response.json()
                    st.success("### Answer:")
                    st.write(data.get("answer"))

                    st.info("### Sources:")
                    sources = data.get("sources", [])
                    for src in sources:
                        st.write(f"- {src}")
                else:
                    st.error(f"Error from server: {response.text}")
            except Exception as e:
                st.error(f"Could not connect to backend server. Error: {e}")
    else:
        st.warning("Please enter a valid question first.")