import streamlit as st
import requests
import os
from dotenv import load_dotenv

load_dotenv()
backend_port = os.getenv("PORT_BACKEND", "8600")
BACKEND_URL = f"http://localhost:{backend_port}"

st.set_page_config(page_title="AI Document Assistant", page_icon="📄", layout="wide")

# Custom CSS for Premium Look
st.markdown("""
    <style>
    .main {
        background-color: #f8f9fa;
    }
    .stChatFloatingInputContainer {
        bottom: 20px;
    }
    .sidebar .sidebar-content {
        background-color: #ffffff;
    }
    .citation {
        font-size: 0.8rem;
        color: #6c757d;
        margin-top: 5px;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("📄 AI Document Assistant")
st.markdown("---")

# Sidebar for Document Management
with st.sidebar:
    st.header("📁 Knowledge Base")
    
    # File Upload
    uploaded_file = st.file_uploader("Upload PDF", type=["pdf"])
    if uploaded_file is not None:
        if st.button("Add to Knowledge Base"):
            with st.spinner("Processing document..."):
                files = {"file": uploaded_file.getvalue()}
                response = requests.post(f"{BACKEND_URL}/upload", files={"file": (uploaded_file.name, uploaded_file.getvalue())})
                if response.status_code == 200:
                    st.success(f"Added {uploaded_file.name}")
                    st.rerun()
                else:
                    st.error("Upload failed.")

    st.markdown("---")
    st.subheader("Managed Documents")
    
    # List Documents
    try:
        docs_response = requests.get(f"{BACKEND_URL}/documents")
        if docs_response.status_code == 200:
            docs = docs_response.json()
            st.write(f"Total: {len(docs)} / 1000")
            
            for doc in docs:
                col1, col2 = st.columns([0.8, 0.2])
                col1.write(f"📄 {doc['filename']}")
                if col2.button("🗑️", key=doc['id']):
                    del_resp = requests.delete(f"{BACKEND_URL}/documents/{doc['id']}")
                    if del_resp.status_code == 200:
                        st.success("Deleted")
                        st.rerun()
                    else:
                        st.error("Delete failed")
        else:
            st.error("Failed to fetch documents")
    except Exception as e:
        st.error("🔴 Backend disconnected")
        st.info("Please restart the application.")

# Chat Interface
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if "citations" in message and message["citations"]:
            st.markdown("**Sources:**")
            for cite in message["citations"]:
                st.markdown(f"- {cite['filename']} (p. {cite['page']})", help="Citation source")

# Chat Input
if prompt := st.chat_input("Ask me anything about your documents..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        with st.spinner("Thinking..."):
            try:
                response = requests.post(f"{BACKEND_URL}/chat", json={"query": prompt})
                if response.status_code == 200:
                    data = response.json()
                    answer = data["answer"]
                    citations = data["citations"]
                    
                    # Deduplicate citations for display
                    unique_citations = []
                    seen = set()
                    for c in citations:
                        cit_key = f"{c['filename']}_{c['page']}"
                        if cit_key not in seen:
                            unique_citations.append(c)
                            seen.add(cit_key)
                    
                    message_placeholder.markdown(answer)
                    if unique_citations:
                        st.markdown("**Sources:**")
                        for cite in unique_citations:
                            st.markdown(f"- {cite['filename']} (p. {cite['page']})")
                    
                    st.session_state.messages.append({
                        "role": "assistant", 
                        "content": answer, 
                        "citations": unique_citations
                    })
                else:
                    st.error("AI response failed.")
            except Exception as e:
                st.error(f"Error: {e}")
