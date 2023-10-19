import streamlit as st
from datetime import datetime
from main import initialize_system, ask_question
import json
import base64
import subprocess
import sys
from ingest import LOADER_MAPPING
import os

# Initialize session state for sidebar size if not set
if "sidebar_size" not in st.session_state:
    st.session_state.sidebar_size = "normal"


# Custom CSS for the smaller sidebar
small_sidebar_css = """
<style>
    .css-17eq0hr a, .css-17eq0hr span, .css-17eq0hr div {
        font-size: 0.8em !important;
    }
    div[data-baseweb="select"] > div {
        height: 24px !important;
    }
    .stButton>div>div>button {
        padding: 0.25em 1em !important;
        font-size: 0.75em !important;
    }
</style>
"""

# If sidebar size is set to "small", inject the custom CSS
if st.session_state.sidebar_size == "small":
    st.sidebar.markdown(small_sidebar_css, unsafe_allow_html=True)

# Extract allowed file extensions
allowed_file_types = [ext.lstrip('.') for ext in LOADER_MAPPING.keys()]

# Initialize the system
system = initialize_system()

# Initialize session state chat history if it doesn't exist
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

st.title("Private GPT Interface")

st.sidebar.header("Configuration")
hide_source = st.sidebar.checkbox("Hide Source Documents")
mute_stream = st.sidebar.checkbox("Mute Stream")

# File Uploader in Sidebar
uploaded_file = st.sidebar.file_uploader("Upload a file", type=allowed_file_types)
SOURCE_DOCUMENTS_PATH = "source_documents"

if uploaded_file:
    with open(os.path.join(SOURCE_DOCUMENTS_PATH, uploaded_file.name), "wb") as f:
        f.write(uploaded_file.getvalue())
    subprocess.run([sys.executable, "ingest.py"])

# Initialize 'last_action', 'user_input', and 'delete_queue' in session_state
st.session_state.setdefault('last_action', None)
st.session_state.setdefault('user_input', "")
st.session_state.setdefault('delete_queue', set())

with st.form(key='query_form'):
    st.session_state.user_input = st.text_input("Enter a query:", st.session_state.user_input)
    if st.form_submit_button(label='Send'):
        st.session_state.last_action = "send"

# Place the clear button outside the form
if st.button(label='Clear'):
    st.session_state.user_input = ""
    st.session_state.last_action = "clear"
    st.write("Query cleared!")

# Custom styles for the container
container_styles = """
<style>
    .answer-container {
        border: 1px solid #E6E6E6;
        border-radius: 5px;
        padding: 15px;
        margin: 10px 0;
    }
</style>
"""
st.markdown(container_styles, unsafe_allow_html=True)

# If input provided and Send button clicked
if st.session_state.user_input and st.session_state.last_action == "send":
    answer, docs, duration = ask_question(system, st.session_state.user_input, hide_source, mute_stream)
    
    # Reset last_action to prevent re-submit on refresh
    st.session_state.last_action = None 

    # Current timestamp
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # Add question, answer, and timestamp to session state's chat history
    st.session_state.chat_history.append((timestamp, st.session_state.user_input, answer))

    # Display the recent answer with a styled container
    with st.container():
        st.markdown(f'<div class="answer-container">Answer (took {duration:.2f} s.): {answer}</div>', unsafe_allow_html=True)

    if not hide_source:
        st.write("Source Documents:")
        for document in docs:
            st.write(document.metadata["source"])
            st.write(document.page_content)

# Handle deletion of chat history entries
for idx in list(st.session_state.delete_queue):
    entry_to_delete = st.session_state.chat_history[idx]
    st.session_state.chat_history.remove(entry_to_delete)
st.session_state.delete_queue = set()  # Clear the delete queue

# Export chat history as a JSON file
if st.sidebar.button("Export Chat History"):
    chat_json = json.dumps(st.session_state.chat_history)
    b64 = base64.b64encode(chat_json.encode()).decode()  
    href = f'<a href="data:text/json;base64,{b64}" download="chat_history.json">Download Chat History as JSON</a>'
    st.sidebar.markdown(href, unsafe_allow_html=True)

# Display chat history in the sidebar
st.sidebar.subheader("Chat History")
container = st.sidebar.container()
displayed_history = st.session_state.chat_history[-30:]

for idx, (ts, q, a) in enumerate(displayed_history):
    with container.expander(f"{ts} - Q{idx + 1}: {q}"):
        st.write(f"Answer: {a}")
        delete_key = f"delete_{ts}"  # Use timestamp as part of the key for uniqueness
        if st.button(f"Delete Q{idx + 1}", key=delete_key):
            entry_to_delete = (ts, q, a)
            st.session_state.chat_history.remove(entry_to_delete)
