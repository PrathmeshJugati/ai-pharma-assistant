# app/main.py

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from core.agent import PharmaAgent
import logging


# ----------------------------
# Logging Configuration
# ----------------------------

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# ----------------------------
# Initialize FastAPI App
# ----------------------------

app = FastAPI(
    title="AI Pharma Assistant",
    description="Domain-grounded pharmaceutical intelligence system",
    version="1.0.0"
)

# ----------------------------
# CORS Configuration
# ----------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ----------------------------
# Initialize Agent (Singleton)
# ----------------------------

agent = PharmaAgent()


# ----------------------------
# Request & Response Models
# ----------------------------

class QueryRequest(BaseModel):
    query: str
    session_id: str = "default"

class QueryResponse(BaseModel):
    response: str


# ----------------------------
# Health Check Endpoint
# ----------------------------

@app.get("/")
def health_check():
    return {
        "status": "running",
        "service": "AI Pharma Assistant"
    }


# ----------------------------
# Main Query Endpoint
# ----------------------------

@app.post("/ask", response_model=QueryResponse)
def ask(request: QueryRequest):

    try:
        logger.info(f"Received query: {request.query} on session: {request.session_id}")

        result = agent.pharma_assistant(request.query, request.session_id)

        return {"response": result}

    except Exception as e:
        logger.error(f"Error processing query: {str(e)}")

        raise HTTPException(
            status_code=500,
            detail="Internal Server Error"
        )