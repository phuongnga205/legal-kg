import os
from dotenv import load_dotenv

# Load biến môi trường từ file .env
load_dotenv()

# Neo4j config
NEO4J_URI = os.getenv("NEO4J_URI", "bolt://localhost:7687")
NEO4J_USER = os.getenv("NEO4J_USER", "neo4j")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD", "neo4j")

# API debug
API_DEBUG = os.getenv("API_DEBUG", "false").lower() == "true"

# CORS origins (cho phép frontend gọi API)
CORS_ORIGINS = os.getenv("CORS_ORIGINS", "http://localhost:5173").split(",")
