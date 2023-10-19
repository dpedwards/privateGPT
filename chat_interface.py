# chat_interface.py
import streamlit as st
from datetime import datetime
from main import initialize_system, ask_question
import subprocess
import sys
from ingest import LOADER_MAPPING
import os

def initialize_interface():
    # Extract allowed file extensions
    allowed_file_types = [ext.lstrip('.') for ext in LOADER_MAPPING.keys()]

    # Initialize the system
    system = initialize_system()

    # Initialize session state chat history if it doesn't exist
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    st.title("Private ChatGPT Interface")

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

    return hide_source, mute_stream, system

def process_input(user_input, hide_source, mute_stream, system):
    # If input provided and Send button clicked
    if user_input:
        answer, docs, duration = ask_question(system, user_input, hide_source, mute_stream)

        # Current timestamp
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # Add question, answer, and timestamp to session state's chat history
        st.session_state.chat_history.append((timestamp, user_input, answer))

        # Display the recent answer (not in accordion for immediate visibility)
        st.write(f"Answer (took {duration:.2f} s.): {answer}")

        if not hide_source:
            st.write("Source Documents:")
            for document in docs:
                st.write(document.metadata["source"])
                st.write(document.page_content)
