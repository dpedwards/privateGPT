#!/usr/bin/env python3

import os
import argparse
import time
from dotenv import load_dotenv
from langchain.chains import RetrievalQA
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.vectorstores import Chroma
from langchain.llms import GPT4All, LlamaCpp
import chromadb
from constants import CHROMA_SETTINGS


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
        try:
            return GPT4All(model=config["model"], backend='gptj', **common_params)
        except Exception as e:
            print(f"Error initializing GPT4All: {e}")
            raise
    else:
        raise Exception(f"Model type {model_type} is not supported. Please choose one of the following: LlamaCpp, GPT4All")


def main():
    config = load_configuration()

    args = parse_arguments()
    embeddings = HuggingFaceEmbeddings(model_name=config["embeddings_model_name"])
    chroma_client = chromadb.PersistentClient(settings=CHROMA_SETTINGS, path=config["persist_directory"])
    db = Chroma(persist_directory=config["persist_directory"], embedding_function=embeddings, client_settings=CHROMA_SETTINGS, client=chroma_client)
    retriever = db.as_retriever(search_kwargs={"k": config["target_source_chunks"]})
    callbacks = [] if args.mute_stream else [StreamingStdOutCallbackHandler()]
    llm = initialize_llm(config["model_type"], callbacks, config)
    qa = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=retriever, return_source_documents=not args.hide_source)

    while True:
        query = input("\nEnter a query: ")
        if query == "exit":
            break
        if query.strip() == "":
            continue

        start = time.time()
        res = qa(query)
        answer, docs = res['result'], [] if args.hide_source else res['source_documents']
        end = time.time()

        print("\n\n> Question:")
        print(query)
        print(f"\n> Answer (took {round(end - start, 2)} s.):")
        print(answer)

        for document in docs:
            print("\n> " + document.metadata["source"] + ":")
            print(document.page_content)


def parse_arguments():
    parser = argparse.ArgumentParser(description='private-gpt: Ask questions to your documents without an internet connection, using the power of LLMs.')
    parser.add_argument("--hide-source", "-S", action='store_true', help='Use this flag to disable printing of source documents used for answers.')
    parser.add_argument("--mute-stream", "-M", action='store_true', help='Use this flag to disable the streaming StdOut callback for LLMs.')
    return parser.parse_args()


if __name__ == "__main__":
    main()
