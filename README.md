# PRIVATE-GPT
### Version 0.0.1

### 

[![LICENSE](https://img.shields.io/badge/license-Apache-lightgrey.svg)]()
[![Python 3](https://img.shields.io/badge/python-yellow.svg)](https://www.python.org/downloads/)
[![LangChain](https://img.shields.io/badge/langchain-lightgreen.svg)](https://python.langchain.com/docs/get_started/introduction)
[![GPT4ALL](https://img.shields.io/badge/gpt4all-white.svg)](https://github.com/nomic-ai/gpt4all)
[![llama.cpp](https://img.shields.io/badge/llamacpp-brown.svg)](https://github.com/abetlen/llama-cpp-python)

## Requirements

* minimum python==3.10.+

## Virtual Environment

### 1. Install venv (if not already installed):
```
pip install virtualenv
```
### 2. Create a virtual environment:
```
python3 -m venv myenv
```
### 3. Activate the virtual environment:
Once the virtual environment is created, you need to activate it:
- Windows:
```
source myenv/bin/activate
```
- macOS and Linux:
```
myenv\Scripts\activate
```

### 4. Deactivate the virtual environment:
When you're done working in the virtual environment and want to return to the global Python environment, simply run:
```
deactivate
```

## Auto installation

For this purpose you use following commands:

```
pip install --upgrade pip
pip install -r requirements.txt
```

## Manual installation

```
pip install --upgrade pip

pip install langchain
pip install gpt4all
pip install chromadb
pip install llama-cpp-python
pip install urllib3
pip install PyMuPDF
pip install python-dotenv
pip install unstructured
pip install extract-msg
pip install tabulate
pip install pandoc
pip install pypandoc
pip install tqdm
pip install sentence_transformers
```


## Download the llm
Store the [ggml-gpt4all-j-v1.3-groovy.bin](https://gpt4all.io/models/ggml-gpt4all-j-v1.3-groovy.bin) model in the `llm` folder.

## Setup env

Rename the 'env' file to '.env' and store all credentials to the following fields:

MODEL_TYPE: supports LlamaCpp or GPT4All
PERSIST_DIRECTORY: is the folder you want your vectorstore in
MODEL_PATH: Path to your GPT4All or LlamaCpp supported LLM

MODEL_N_CTX: Maximum token limit for the LLM model

MODEL_N_BATCH: Number of tokens in the prompt that are fed into the model at a time. Optimal value differs a lot depending on the model (8 works well for GPT4All, and 1024 is better for LlamaCpp)

EMBEDDINGS_MODEL_NAME: SentenceTransformers embeddings model name (see https://www.sbert.net/docs/pretrained_models.html)

TARGET_SOURCE_CHUNKS: The amount of chunks (sources) that will be used to answer a question

## Run the application
1. Store files/documents into `source_documents` folder

  <img width="450" src="images/02.png">

2. Create chunks for vector db from own data files/documents
  ```
  python3 ingest.py
   ```
  <img width="450" src="images/01.png">

3. Chat with llm
  ```
  python3 main.py
  ```

  <img width="450" src="images/03.png">

  <img width="450" src="images/04.png">

  <img width="450" src="images/05.png">



## Contact
core8@gmx.net
