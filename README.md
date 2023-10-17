# PRIVATE-GPT
### Version 0.0.1

### 

[![LICENSE](https://img.shields.io/badge/license-Apache-lightgrey.svg)]()
[![Python 3](https://img.shields.io/badge/python-yellow.svg)](https://www.python.org/downloads/)
[![python-dotenv](https://img.shields.io/badge/python-dotenv-lightblue.svg)](https://pypi.org/project/python-dotenv/)

## Requirements

* minimum python==3.10.+

## Virtual Environment

### 1. Install venv (if not already installed):
```
pip install virtualenv
```
### 2. Create a virtual environment:
```
python -m venv myenv
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

### ISSUES DURING INSTALLATION (WINDOWS)
```
Collecting dotenv
  Using cached dotenv-0.0.5.tar.gz (2.4 kB)
  Preparing metadata (setup.py) ... error
  error: subprocess-exited-with-error
  
  × python setup.py egg_info did not run successfully.
  │ exit code: 1
  ╰─> [70 lines of output]
      /Users/<user>/Desktop/private-gpt/myenv/lib/python3.11/site-packages/setuptools/installer.py:27: SetuptoolsDeprecationWarning: setuptools.installer is deprecated. Requirements should be satisfied by a PEP 517 installer.
```

The error message suggests that there's a problem with building the `dotenv` package using `setup.py`. The specific line mentioning `setuptools.installer is deprecated` indicates that the package might not be up-to-date with the current best practices and standards related to packaging.

Here are some steps you can take to resolve this:

1. **Update `pip` and `setuptools`**:
   Ensuring you have the latest versions can sometimes resolve compatibility issues.
   ```bash
   pip install --upgrade pip setuptools
  ```

2. **Use a Different Package**:
   If you're trying to use `dotenv` for loading environment variables, the more popular package is `python-dotenv`. Perhaps you meant to install this one:
   ```bash
   pip install python-dotenv
   ```

3. **Install Without PEP 517**:
   As a workaround, you can try to install the package without PEP 517:
   ```bash
   pip install dotenv --no-use-pep517
   ```

4. **Manual Installation**:
   As a last resort, you can manually download the package from the PyPI repository, unpack it, and install using `setup.py` directly:
   ```bash
   wget https://files.pythonhosted.org/packages/source/d/dotenv/dotenv-0.0.5.tar.gz
   tar xzf dotenv-0.0.5.tar.gz
   cd dotenv-0.0.5
   python setup.py install
   ```

5. **Python Version Compatibility**:
   Notice that you're using Python 3.11 (as per the path). Some packages may not yet be compatible with the latest versions of Python. If possible, consider creating a virtual environment with an older version of Python (e.g., 3.9 or 3.10) and trying the installation there.

In general, given the error, I would recommend going with the second option and trying to install `python-dotenv` unless you have a specific reason to use the `dotenv` package.

## Download the llm
[ggml-gpt4all-j-v1.3-groovy.bin](https://gpt4all.io/models/ggml-gpt4all-j-v1.3-groovy.bin)

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
1. Store files/ducuments into source_documents
2. Create chunks from own data files/documents
  ```
  python3 ingest.py
   ```
4. Chat with llm
  ```
  python3.main.py
  ```

## Contact
core8@gmx.net
