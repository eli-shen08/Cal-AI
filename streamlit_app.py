import streamlit as st
import requests
import time

# Page setup
st.set_page_config(page_title="RAG Query", layout="centered")

st.title("RAG Query System")
st.markdown(" Ask me about Act 1979 or Ph.D Reg 2025.")

# Hardcode your FastAPI URL here
# API_URL = "http://127.0.0.1:8000/"
API_URL = "http://localhost:5678/webhook/rag-query"
HEALTH_URL = "http://127.0.0.1:8000/health"

def is_ready():
    try:
        r = requests.get(HEALTH_URL, timeout=2)
        return r.json().get("vectordb_ready", False)
    except:
        return False
    


if not is_ready():
    with st.spinner("⏳ System initializing — loading documents and vector database..."):
        while not is_ready():
            time.sleep(2)
    st.rerun()

st.success("✅ System ready")

# User input
query = st.text_area("Enter your query:", height=100)

# Submit button
if st.button("🔍 Submit Query", type="primary"):
    if not query.strip():
        st.warning("⚠️Please enter a question first")
    else:
        with st.spinner("Waiting for response..."):
            try:
                # Call FastAPI RAG endpoint
                response = requests.post(API_URL, json={"query": query})

                if response.status_code == 200:
                    if not response.text:
                        st.error("❌ Empty response from n8n")
                    else:
                        data = response.json()
                        st.markdown("### 💬 Cal-AI :")
                        st.info(data["response"]["content"])  

                else:
                    st.error(f"❌ API error: {response.status_code} – {response.text}")

            except requests.exceptions.ConnectionError:
                st.error("❌ Cannot connect to FastAPI. Please start the server first.")
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")