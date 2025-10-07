#!/usr/bin/env python3
"""
File Upload Interface for ChatGPT
A simple web interface to upload files and get shareable content for ChatGPT
"""

from fastapi import FastAPI, UploadFile, File, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pathlib import Path
import os
import uvicorn
from typing import List

app = FastAPI(title="ChatGPT File Upload Interface")

# Create uploads directory
UPLOAD_DIR = Path("/Users/bharathmr/Documents/AI-Coding/MCP/uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

@app.get("/", response_class=HTMLResponse)
async def upload_page():
    """Simple HTML page for file uploads"""
    return """
<!DOCTYPE html>
<html>
<head>
    <title>ChatGPT File Upload</title>
    <style>
        body { 
            font-family: Arial, sans-serif; 
            max-width: 800px; 
            margin: 50px auto; 
            padding: 20px;
            background-color: #f5f5f5;
        }
        .container {
            background: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        h1 { color: #333; text-align: center; }
        .upload-area {
            border: 3px dashed #ddd;
            border-radius: 10px;
            padding: 30px;
            text-align: center;
            margin: 20px 0;
            background: #fafafa;
        }
        .upload-area:hover { border-color: #007bff; background: #f0f8ff; }
        input[type="file"] { 
            margin: 10px 0; 
            padding: 10px;
            border: 1px solid #ddd;
            border-radius: 5px;
            width: 100%;
        }
        button { 
            background: #007bff; 
            color: white; 
            border: none; 
            padding: 12px 24px; 
            border-radius: 5px;
            cursor: pointer;
            font-size: 16px;
            width: 100%;
            margin: 10px 0;
        }
        button:hover { background: #0056b3; }
        .result { 
            margin-top: 20px; 
            padding: 15px; 
            border-radius: 5px; 
            background: #d4edda;
            border: 1px solid #c3e6cb;
            display: none;
        }
        .error {
            background: #f8d7da;
            border-color: #f5c6cb;
            color: #721c24;
        }
        .file-content {
            background: #f8f9fa;
            padding: 15px;
            border-radius: 5px;
            border: 1px solid #e9ecef;
            font-family: 'Courier New', monospace;
            font-size: 14px;
            white-space: pre-wrap;
            max-height: 300px;
            overflow-y: auto;
            margin: 10px 0;
        }
        .instructions {
            background: #e3f2fd;
            padding: 20px;
            border-radius: 5px;
            margin: 20px 0;
            border-left: 4px solid #2196f3;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🤖 ChatGPT File Upload Interface</h1>
        
        <div class="instructions">
            <h3>📋 How to Use:</h3>
            <ol>
                <li><strong>Upload your file</strong> using the form below</li>
                <li><strong>Copy the content</strong> that appears after upload</li>
                <li><strong>Paste into ChatGPT</strong> with your questions</li>
                <li><strong>Ask ChatGPT</strong> to analyze the content</li>
            </ol>
        </div>

        <form id="uploadForm" enctype="multipart/form-data">
            <div class="upload-area">
                <h3>📁 Select File to Upload</h3>
                <input type="file" id="fileInput" name="file" required>
                <p>Supports: .txt, .py, .js, .json, .md, .csv, and more</p>
            </div>
            <button type="submit">🚀 Upload and Process File</button>
        </form>

        <div id="result" class="result">
            <h3>✅ File Processed Successfully!</h3>
            <p><strong>File:</strong> <span id="fileName"></span></p>
            <p><strong>Size:</strong> <span id="fileSize"></span> bytes</p>
            
            <h4>📋 Content to Copy for ChatGPT:</h4>
            <div id="fileContent" class="file-content"></div>
            <button onclick="copyToClipboard()" style="width: auto; padding: 8px 16px;">📋 Copy Content</button>
        </div>
    </div>

    <script>
        document.getElementById('uploadForm').addEventListener('submit', async (e) => {
            e.preventDefault();
            
            const formData = new FormData();
            const fileInput = document.getElementById('fileInput');
            const file = fileInput.files[0];
            
            if (!file) {
                alert('Please select a file');
                return;
            }
            
            formData.append('file', file);
            
            try {
                const response = await fetch('/upload', {
                    method: 'POST',
                    body: formData
                });
                
                const data = await response.json();
                
                if (data.success) {
                    document.getElementById('fileName').textContent = data.filename;
                    document.getElementById('fileSize').textContent = data.size;
                    document.getElementById('fileContent').textContent = 
                        `File: ${data.filename}\\n\\nContent:\\n${data.content}`;
                    
                    const resultDiv = document.getElementById('result');
                    resultDiv.style.display = 'block';
                    resultDiv.classList.remove('error');
                } else {
                    throw new Error(data.error || 'Upload failed');
                }
            } catch (error) {
                const resultDiv = document.getElementById('result');
                resultDiv.innerHTML = `<h3>❌ Error</h3><p>${error.message}</p>`;
                resultDiv.style.display = 'block';
                resultDiv.classList.add('error');
            }
        });
        
        function copyToClipboard() {
            const content = document.getElementById('fileContent').textContent;
            navigator.clipboard.writeText(content).then(() => {
                alert('✅ Content copied to clipboard!\\nNow paste it into ChatGPT.');
            }).catch(err => {
                console.error('Copy failed:', err);
                alert('❌ Copy failed. Please select and copy manually.');
            });
        }
    </script>
</body>
</html>
    """

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    """Upload and process file for ChatGPT"""
    try:
        # Check file size (limit to 10MB)
        content = await file.read()
        if len(content) > 10 * 1024 * 1024:  # 10MB limit
            raise HTTPException(status_code=413, detail="File too large (max 10MB)")
        
        # Save file
        file_path = UPLOAD_DIR / file.filename
        with open(file_path, 'wb') as f:
            f.write(content)
        
        # Try to read as text
        try:
            text_content = content.decode('utf-8')
        except UnicodeDecodeError:
            try:
                text_content = content.decode('latin-1')
            except:
                text_content = "Binary file - content not displayable as text"
        
        return {
            "success": True,
            "filename": file.filename,
            "size": len(content),
            "content": text_content,
            "saved_path": str(file_path)
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")

@app.get("/uploaded-files")
async def list_uploaded_files():
    """List all uploaded files"""
    try:
        files = []
        for file_path in UPLOAD_DIR.glob("*"):
            if file_path.is_file():
                stat = file_path.stat()
                files.append({
                    "name": file_path.name,
                    "size": stat.st_size,
                    "path": str(file_path)
                })
        
        return {"files": files, "count": len(files)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    print("🌐 Starting ChatGPT File Upload Interface...")
    print("📁 Upload files at: http://localhost:8002")
    print("💡 Upload files and copy content to share with ChatGPT!")
    
    uvicorn.run(
        app, 
        host="127.0.0.1", 
        port=8002,
        reload=False
    )