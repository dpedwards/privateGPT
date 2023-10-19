#!/usr/bin/env python3

import os
import time
from dotenv import load_dotenv
from langchain.chains import RetrievalQA
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.vectorstores import Chroma
from langchain.llms import GPT4All, LlamaCpp
import chromadb
from constants import CHROMA_SETTINGS
import psycopg2


def load_configuration():
    if not load_dotenv():
        print("Could not load .env file or it is empty. Please check if it exists and is readable.")
        exit(1)
    
    return {
        "embeddings_model_name": os.environ.get("EMBEDDINGS_MODEL_NAME"),
        "persist_directory": os.environ.get('PERSIST_DIRECTORY'),
        "model_type": os.environ.get('MODEL_TYPE'),
        "model": os.environ.get('MODEL_PATH'),
        "model_n_ctx": os.environ.get('MODEL_N_CTX'),
        "model_n_batch": int(os.environ.get('MODEL_N_BATCH', 8)),
        "target_source_chunks": int(os.environ.get('TARGET_SOURCE_CHUNKS', 4))
    }


def initialize_llm(model_type, callbacks, config):
    common_params = {
        "max_tokens": config["model_n_ctx"],
        "n_batch": config["model_n_batch"],
        "callbacks": callbacks,
        "verbose": False
    }

    if model_type == "LlamaCpp":
        return LlamaCpp(model_path=config["model"], **common_params)
    elif model_type == "GPT4All":
        return GPT4All(model=config["model"], backend='gptj', **common_params)
    else:
        raise Exception(f"Model type {model_type} is not supported. Please choose one of the following: LlamaCpp, GPT4All")


def initialize_system():
    try:
        config = load_configuration()

        embeddings = HuggingFaceEmbeddings(model_name=config["embeddings_model_name"])
        chroma_client = chromadb.PersistentClient(settings=CHROMA_SETTINGS, path=config["persist_directory"])
        db = Chroma(persist_directory=config["persist_directory"], embedding_function=embeddings, client_settings=CHROMA_SETTINGS, client=chroma_client)

        retriever = db.as_retriever(search_kwargs={"k": config["target_source_chunks"]})
        callbacks = [StreamingStdOutCallbackHandler()]
        llm = initialize_llm(config["model_type"], callbacks, config)

        qa = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=retriever)
        
        system = {
            'llm': llm,
            'qa': qa,
            'retriever': retriever
        }

        print(system)  # To see the returned structure
        return system

    except Exception as e:
        print(f"Error during system initialization: {e}")
        return {}


YOUR_CONNECTION_STRING = "YOUR_DB_CONNECTION_STRING"  # TODO: Add your actual connection string here

def get_nearest_neighbors(connection, embedding_vector, top_n=10):
    query = """
    SELECT document, embedding
    FROM documents_table
    ORDER BY embedding <-> %s
    LIMIT %s;
    """
    cursor = connection.cursor()
    cursor.execute(query, (embedding_vector, top_n))
    results = cursor.fetchall()
    return results

def ask_question(system, query, hide_source=False, mute_stream=False):
    if not isinstance(system, dict) or 'qa' not in system:
        print("Error: Invalid system provided.")
        return None, [], 0

    start = time.time()
    res = system['qa'](query)
    
    # Log the keys in the returned result to understand its structure
    print(f"Keys in returned result: {res.keys()}")

    # Use .get() to avoid KeyError
    answer = res.get('result', "No answer found.")
    docs = [] if hide_source else res.get('source_documents', [])

    # Check if the answer contains an SQL statement
    if "SELECT" in answer and "FROM" in answer:
        # Fetch similar vectors based on the SQL statement (placeholder logic, adapt as needed)
        connection = psycopg2.connect(YOUR_CONNECTION_STRING)
        similar_vectors = get_nearest_neighbors(connection, answer)  # Assuming the SQL statement can be used as an embedding_vector (modify as needed)
        connection.close()
        answer += f"\n\nEquivalent Vectors: {similar_vectors}"

    end = time.time()
    duration = end - start
    return answer, docs, duration


