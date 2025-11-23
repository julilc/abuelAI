from pymongo import MongoClient
from openai import OpenAI
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Environment variables (private)  
MONGODB_URI = os.getenv("MONGODB_URI")  

# MongoDB cluster configuration
mongo_client = MongoClient(MONGODB_URI)
agent_db = mongo_client["ai_agent_db"]
vector_collection = agent_db["embeddings"]
memory_collection = agent_db["chat_history"]

# Local LLM through Ollama (OpenAI API compatible)
openai_client = OpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama"   # any string is fine
)

# Chat model to use locally
OPENAI_MODEL = "llama3.1"
