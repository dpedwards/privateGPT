from fastapi import APIRouter, Request
from starlette.responses import StreamingResponse
from langchain.llms import LlamaCpp
from langchain.utilities import SQLDatabase
from langchain.chains import create_sql_query_chain
from langchain.callbacks.manager import CallbackManager
from langchain_experimental.sql import SQLDatabaseChain
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from pydantic import BaseModel
from langchain.agents import create_sql_agent
from langchain.agents.agent_toolkits import SQLDatabaseToolkit
from langchain.agents.agent_types import AgentType
from langchain.sql_database import SQLDatabase
from langchain.llms import LlamaCpp  # Import LlamaCpp

# Define the API router
sql_router = APIRouter(tags=["SQL"])

class SQLRequestBody(BaseModel):
    query: str

# Initialize the Langchain SQL database
db = SQLDatabase.from_uri("sqlite:////Users/dpedwards/Documents/MyRepositores/privateGPT/local_data/sql/Chinook.db")

# Create the LLM instance
llm_model_path = "/Users/dpedwards/Documents/MyRepositores/privateGPT/models/mistral-7b-instruct-v0.2.Q4_K_M.gguf"
llm = LlamaCpp(
    model_path=llm_model_path,  # Specify model_path explicitly
    temperature=0.0,
    n_ctx=10000,
    n_gpu_layers=15,
    n_threads=3,
    n_batch=512,
    f16_kv=True,
    verbose=True,
    repeat_penalty=1.8
)

# Create the SQL query chain
chain = create_sql_query_chain(llm, db)

@sql_router.post("/sql")
async def sql_query(request: Request, body: SQLRequestBody) -> StreamingResponse:
    """
    Execute a SQL query using the provided LLM and toolkit.
    """
    # Get the user's SQL query
    user_query = body.query
    
    try:
        # Invoke the SQL query chain
        response = chain.invoke({"question": user_query})
        
        async def generate():
            yield str(response)
        
        # Return the response as a StreamingResponse with async generator
        return StreamingResponse(content=generate(), media_type="text/plain", status_code=200)
    except Exception as e:
        return StreamingResponse(content=str(e), media_type="text/plain", status_code=500)



