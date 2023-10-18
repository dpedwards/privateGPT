import streamlit as st
from datetime import datetime
from main import initialize_system, ask_question
import json
import base64
import subprocess
import sys
from ingest import LOADER_MAPPING
import os
import psycopg2

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

# Using Streamlit's form functionality for the query input
with st.form(key='query_form'):
    user_input = st.text_input("Enter a query:", "")
    submit_button = st.form_submit_button(label='Send')

# Place the clear button outside the form
clear_button = st.button(label='Clear')

# If Clear button clicked
if clear_button:
    user_input = ""
    st.write("Query cleared!")

# If input provided and Send button clicked
if user_input and submit_button:
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

# Export chat history as a JSON file
if st.button("Export Chat History"):
    chat_json = json.dumps(st.session_state.chat_history)
    b64 = base64.b64encode(chat_json.encode()).decode()  # some strings <-> bytes conversions necessary here
    href = f'<a href="data:text/json;base64,{b64}" download="chat_history.json">Download Chat History as JSON</a>'
    st.markdown(href, unsafe_allow_html=True)

# Display chat history in an accordion-style timeline
st.subheader("Chat History")
for idx, (ts, q, a) in enumerate(st.session_state.chat_history[:]):
    with st.expander(f"{ts} - Q{idx + 1}: {q}"):
        st.write(f"Answer: {a}")
        if st.button(f"Delete Q{idx + 1}", key=f"delete_{idx}"):
            st.session_state.chat_history.remove((ts, q, a))
