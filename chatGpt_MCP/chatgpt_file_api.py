#!/usr/bin/env python3
"""
ChatGPT File Reader API
A web API that allows ChatGPT to read local files through HTTP requests
Since ChatGPT can't use MCP, we create a web API it can call instead
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
from pathlib import Path
from typing import Optional
import uvicorn

# Create FastAPI app
app = FastAPI(
    title="ChatGPT File Reader API",
    description="API for ChatGPT to read local files",
    version="1.0.0"
)

# Request model
class FileReadRequest(BaseModel):
    filepath: str
    encoding: Optional[str] = "utf-8"

# Response model  
class FileReadResponse(BaseModel):
    success: bool
    content: Optional[str] = None
    error: Optional[str] = None
    file_info: Optional[dict] = None

# Security: Define allowed directories
ALLOWED_DIRECTORIES = [
    "/Users/bharathmr/Documents/AI-Coding",
    "/Users/bharathmr/Projects"
]

def is_path_allowed(filepath: str) -> bool:
    """Check if file path is within allowed directories"""
    try:
        abs_path = Path(filepath).resolve()
        return any(str(abs_path).startswith(allowed_dir) for allowed_dir in ALLOWED_DIRECTORIES)
    except:
        return False

@app.get("/")
async def root():
    """API health check endpoint"""
    return {"message": "ChatGPT File Reader API is running", "status": "healthy"}

@app.get("/allowed-directories")
async def get_allowed_directories():
    """Get list of directories ChatGPT can read from"""
    return {"allowed_directories": ALLOWED_DIRECTORIES}

@app.post("/read-file", response_model=FileReadResponse)
async def read_file(request: FileReadRequest):
    """
    Read a local file and return its contents
    ChatGPT can call this endpoint to access local files
    """
    try:
        # Security check
        if not is_path_allowed(request.filepath):
            raise HTTPException(
                status_code=403, 
                detail="Access denied: File outside allowed directories"
            )
        
        # Convert to Path object
        file_path = Path(request.filepath)
        
        # Check if file exists
        if not file_path.exists():
            raise HTTPException(
                status_code=404,
                detail=f"File not found: {request.filepath}"
            )
        
        # Check if it's actually a file (not a directory)
        if not file_path.is_file():
            raise HTTPException(
                status_code=400,
                detail=f"Path is not a file: {request.filepath}"
            )
        
        # Read file content
        try:
            with open(file_path, 'r', encoding=request.encoding) as f:
                content = f.read()
        except UnicodeDecodeError:
            # Try with different encoding for binary files
            with open(file_path, 'r', encoding='latin-1') as f:
                content = f.read()
        
        # Get file info
        stat = file_path.stat()
        file_info = {
            "name": file_path.name,
            "size": stat.st_size,
            "extension": file_path.suffix,
            "absolute_path": str(file_path.resolve())
        }
        
        return FileReadResponse(
            success=True,
            content=content,
            file_info=file_info
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")

@app.get("/list-files")
async def list_files(directory: str = "/Users/bharathmr/Documents/AI-Coding"):
    """
    List files in a directory
    Helps ChatGPT discover available files
    """
    try:
        # Security check
        if not is_path_allowed(directory):
            raise HTTPException(
                status_code=403,
                detail="Access denied: Directory outside allowed paths"
            )
        
        dir_path = Path(directory)
        
        if not dir_path.exists():
            raise HTTPException(
                status_code=404,
                detail=f"Directory not found: {directory}"
            )
        
        if not dir_path.is_dir():
            raise HTTPException(
                status_code=400,
                detail=f"Path is not a directory: {directory}"
            )
        
        # List files
        files = []
        for item in dir_path.iterdir():
            if item.is_file():
                stat = item.stat()
                files.append({
                    "name": item.name,
                    "path": str(item),
                    "size": stat.st_size,
                    "extension": item.suffix
                })
        
        return {
            "directory": directory,
            "files": files,
            "count": len(files)
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")

@app.get("/file-info")
async def get_file_info(filepath: str):
    """Get information about a file without reading its content"""
    try:
        if not is_path_allowed(filepath):
            raise HTTPException(
                status_code=403,
                detail="Access denied: File outside allowed directories"
            )
        
        file_path = Path(filepath)
        
        if not file_path.exists():
            raise HTTPException(
                status_code=404,
                detail=f"File not found: {filepath}"
            )
        
        stat = file_path.stat()
        
        return {
            "name": file_path.name,
            "path": str(file_path.resolve()),
            "size": stat.st_size,
            "extension": file_path.suffix,
            "is_file": file_path.is_file(),
            "is_directory": file_path.is_dir(),
            "readable": os.access(file_path, os.R_OK)
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")

if __name__ == "__main__":
    print("🚀 Starting ChatGPT File Reader API...")
    print("📡 ChatGPT can now access your local files via HTTP!")
    print("📍 API will be available at: http://localhost:8001")
    print("📚 API docs at: http://localhost:8001/docs")
    
    uvicorn.run(
        app, 
        host="127.0.0.1", 
        port=8001,
        reload=False
    )