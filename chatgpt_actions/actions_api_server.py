"""
ChatGPT Actions API Server
A FastAPI server designed specifically for ChatGPT Actions integration.
Provides OpenAPI-compliant endpoints that ChatGPT can call directly.
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
import requests
import uvicorn
from typing import Optional, List
import json
import os
from pathlib import Path

# Create FastAPI app with CORS for ChatGPT Actions
app = FastAPI(
    title="Local AI Actions API", 
    description="API for ChatGPT Actions to interact with local AI services and files",
    version="1.0.0",
    openapi_url=None  # Disable auto-generated OpenAPI
)

# Add CORS middleware for ChatGPT Actions
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://chat.openai.com", "https://chatgpt.com"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

# Pydantic models for API requests/responses
class AskRequest(BaseModel):
    message: str = Field(..., description="The question or prompt to send to the local AI", example="What is machine learning?")
    model: Optional[str] = Field("llama3.2:latest", description="The AI model to use")

class AskResponse(BaseModel):
    response: str = Field(..., description="The AI's response to your question")
    model_used: str = Field(..., description="The AI model that generated the response")
    success: bool = Field(..., description="Whether the request was successful")

class FileRequest(BaseModel):
    filepath: str = Field(..., description="Absolute path to the file to read", example="/Users/bharathmr/Documents/AI-Coding/README.md")

class FileResponse(BaseModel):
    content: str = Field(..., description="The content of the file")
    filename: str = Field(..., description="Name of the file")
    size: int = Field(..., description="Size of file in bytes")
    success: bool = Field(..., description="Whether the file was read successfully")

class StatusResponse(BaseModel):
    status: str = Field(..., description="Service status")
    ollama_available: bool = Field(..., description="Whether Ollama AI is running")
    models_available: List[str] = Field(..., description="List of available AI models")

@app.get("/", response_model=dict, summary="Service Information")
async def root():
    """
    Get basic information about this AI service.
    """
    return {
        "service": "Local AI Assistant API",
        "description": "ChatGPT Actions can use this API to interact with your local AI",
        "version": "1.0.0",
        "endpoints": ["/ask", "/read-file", "/status"],
        "documentation": "http://localhost:8080/docs"
    }

@app.post("/ask", response_model=AskResponse, summary="Ask Local AI")
async def ask_local_ai(request: AskRequest):
    """
    Send a question to your local Ollama AI model.
    
    This endpoint allows ChatGPT to ask questions to your local AI model,
    creating a bridge between ChatGPT and your local AI infrastructure.
    """
    try:
        # Prepare request to local Ollama
        ollama_payload = {
            "model": request.model,
            "prompt": request.message,
            "stream": False
        }
        
        # Send request to local Ollama service
        response = requests.post(
            "http://localhost:11434/api/generate", 
            json=ollama_payload,
            timeout=30
        )
        
        if response.status_code == 200:
            ollama_response = response.json()
            return AskResponse(
                response=ollama_response["response"],
                model_used=request.model,
                success=True
            )
        else:
            raise HTTPException(
                status_code=500, 
                detail=f"Ollama service error: {response.status_code}"
            )
            
    except requests.exceptions.RequestException as e:
        raise HTTPException(
            status_code=503, 
            detail=f"Cannot connect to local AI service: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Unexpected error: {str(e)}"
        )

@app.post("/read-file", response_model=FileResponse, summary="Read Local File")
async def read_local_file(request: FileRequest):
    """
    Read the contents of a local file on your computer.
    
    This allows ChatGPT to access and analyze files on your local system
    through the Actions interface. Files must be within allowed directories.
    """
    try:
        file_path = Path(request.filepath)
        
        # Security: Only allow files within the AI-Coding project
        allowed_base = Path(os.environ.get("AI_CODING_BASE_DIR", "/Users/bharathmr/Documents/AI-Coding"))
        try:
            # Check if file is within allowed directory
            file_path.resolve().relative_to(allowed_base.resolve())
        except ValueError:
            raise HTTPException(
                status_code=403,
                detail="File access denied: Only files within AI-Coding project are allowed"
            )
        
        # Check if file exists
        if not file_path.exists():
            raise HTTPException(
                status_code=404,
                detail=f"File not found: {request.filepath}"
            )
        
        # Check if it's actually a file
        if not file_path.is_file():
            raise HTTPException(
                status_code=400,
                detail=f"Path is not a file: {request.filepath}"
            )
        
        # Read file content
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        return FileResponse(
            content=content,
            filename=file_path.name,
            size=len(content.encode('utf-8')),
            success=True
        )
        
    except UnicodeDecodeError:
        raise HTTPException(
            status_code=400,
            detail="File is not a text file or has unsupported encoding"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error reading file: {str(e)}"
        )

@app.get("/status", response_model=StatusResponse, summary="Service Status")
async def get_service_status():
    """
    Check the status of the local AI service and available models.
    
    This endpoint helps ChatGPT understand what AI capabilities are
    available on your local system.
    """
    try:
        # Check if Ollama is running
        ollama_response = requests.get("http://localhost:11434/api/tags", timeout=5)
        
        if ollama_response.status_code == 200:
            models_data = ollama_response.json()
            available_models = [model["name"] for model in models_data.get("models", [])]
            
            return StatusResponse(
                status="healthy",
                ollama_available=True,
                models_available=available_models
            )
        else:
            return StatusResponse(
                status="ollama_error",
                ollama_available=False,
                models_available=[]
            )
            
    except requests.exceptions.RequestException:
        return StatusResponse(
            status="ollama_unavailable",
            ollama_available=False,
            models_available=[]
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error checking service status: {str(e)}"
        )

@app.get("/openapi.json")
async def custom_openapi():
    """Serve our custom OpenAPI schema with proper HTTPS URLs and schema validation"""
    try:
        # Load our custom OpenAPI schema
        current_dir = Path(__file__).parent
        openapi_path = current_dir / "openapi.json"
        
        with open(openapi_path, 'r') as f:
            openapi_schema = json.load(f)
        
        return JSONResponse(content=openapi_schema)
    except Exception as e:
        # Fallback to auto-generated schema if custom one fails
        return app.openapi()

if __name__ == "__main__":
    print("🚀 Starting ChatGPT Actions API Server...")
    print("📡 ChatGPT Actions can now connect to your local AI!")
    print("📍 Server will be available at: http://localhost:8081")
    print("📚 API documentation at: http://localhost:8081/docs")
    print("🔧 Configure ChatGPT Actions with: http://localhost:8081/openapi.json")
    
    uvicorn.run(
        app, 
        host="127.0.0.1", 
        port=8081,
        reload=False
    )