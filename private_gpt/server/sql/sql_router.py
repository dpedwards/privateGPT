import os
import dotenv
from fastapi import FastAPI, APIRouter, Request
from starlette.responses import JSONResponse
from pydantic import BaseModel
from transformers import AutoTokenizer
from langchain.llms import GPT4All
from langchain_community.llms import OpenAI
from langchain_community.utilities import SQLDatabase
from langchain_experimental.sql import SQLDatabaseChain
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler

# Load environment variables
dotenv.load_dotenv()

# Initialize FastAPI and the API router
app = FastAPI()
sql_router = APIRouter(tags=["SQL"])

# Define the SQLRequestBody class for handling requests
class SQLRequestBody(BaseModel):
    query: str

# Environment variables
use_local_llm = os.getenv("USE_LOCAL_LLM", "false").lower() == "true"
model_path = os.getenv("MODEL_PATH")

# Database setup
db_uri = "sqlite:////Users/dpedwards/Documents/Statista/Repositories/privateGPT/local_data/sql/Chinook.db"
db = SQLDatabase.from_uri(db_uri)

# Callbacks support token-wise streaming
callbacks = [StreamingStdOutCallbackHandler()]

# LLM setup
if use_local_llm and model_path:
    model_name = "gpt2-xl"  # You can choose a different LLM model
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    llm = GPT4All(model=model_path, backend=model_name, callbacks=callbacks, verbose=True) # Custom model
else:
    # Fallback to OpenAI model
    llm = OpenAI(temperature=0, verbose=True)

# SQL Agent setup with LLM and database
db_chain = SQLDatabaseChain.from_llm(llm, db, verbose=True)

# Define the endpoint for SQL queries
@sql_router.post("/sql")
async def sql_query(request: Request, body: SQLRequestBody) -> JSONResponse:
    user_query = body.query
    try:
        # Use the SQL agent executor to process the query
        response = db_chain.run(user_query)
    except Exception as e:
        response = f"An error occurred: {str(e)}"

    return JSONResponse(content=response, media_type="text/plain")

app.include_router(sql_router)
