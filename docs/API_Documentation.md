# API Documentation

## Overview

The Local AI Chatbot Service provides a RESTful API for interacting with locally hosted AI models via Ollama. This API allows you to send questions and receive AI-generated responses programmatically.

## Base URL

```
http://localhost:8000
```

## Authentication

No authentication required - this is a local service.

## Endpoints

### POST /ask

Send a message to the AI model and receive a response.

**URL:** `/ask`
**Method:** `POST`
**Content-Type:** `application/json`

#### Request Format

```json
{
  "message": "string"
}
```

#### Parameters

| Parameter | Type   | Required | Description                    |
|-----------|--------|----------|--------------------------------|
| message   | string | Yes      | The question or prompt for AI  |

#### Response Format

**Success (200 OK):**
```json
{
  "response": "string"
}
```

**Error (500 Internal Server Error):**
```json
{
  "detail": "Error description"
}
```

#### Example Requests

**Basic Question:**
```bash
curl -X POST "http://localhost:8000/ask" \
     -H "Content-Type: application/json" \
     -d '{"message": "What is artificial intelligence?"}'
```

**Programming Question:**
```bash
curl -X POST "http://localhost:8000/ask" \
     -H "Content-Type: application/json" \
     -d '{"message": "How do I create a Python function?"}'
```

**Creative Request:**
```bash
curl -X POST "http://localhost:8000/ask" \
     -H "Content-Type: application/json" \
     -d '{"message": "Write a haiku about programming"}'
```

#### Example Responses

**Successful Response:**
```json
{
  "response": "Artificial intelligence (AI) refers to the simulation of human intelligence in machines that are programmed to think and learn like humans. It includes various technologies like machine learning, natural language processing, and computer vision."
}
```

**Error Response:**
```json
{
  "detail": "Connection to Ollama failed: Connection refused"
}
```

## Code Examples

### Python with requests

```python
import requests
import json

def ask_ai(question):
    url = "http://localhost:8000/ask"
    payload = {"message": question}
    
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        return response.json()["response"]
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return None

# Usage
answer = ask_ai("Explain quantum computing in simple terms")
print(answer)
```

### JavaScript (Node.js)

```javascript
const axios = require('axios');

async function askAI(question) {
    try {
        const response = await axios.post('http://localhost:8000/ask', {
            message: question
        });
        return response.data.response;
    } catch (error) {
        console.error('Error:', error.response?.data || error.message);
        return null;
    }
}

// Usage
askAI("What are the benefits of renewable energy?")
    .then(answer => console.log(answer));
```

### JavaScript (Browser/Fetch)

```javascript
async function askAI(question) {
    try {
        const response = await fetch('http://localhost:8000/ask', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ message: question })
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        return data.response;
    } catch (error) {
        console.error('Error:', error);
        return null;
    }
}

// Usage
askAI("How does blockchain technology work?")
    .then(answer => console.log(answer));
```

### cURL Examples

**Simple question:**
```bash
curl -X POST "http://localhost:8000/ask" \
     -H "Content-Type: application/json" \
     -d '{"message": "What is machine learning?"}'
```

**Multi-line question:**
```bash
curl -X POST "http://localhost:8000/ask" \
     -H "Content-Type: application/json" \
     -d '{
       "message": "Can you help me debug this Python code: print(Hello World)"
     }'
```

**Question with special characters:**
```bash
curl -X POST "http://localhost:8000/ask" \
     -H "Content-Type: application/json" \
     -d '{"message": "What does the symbol \"&\" mean in programming?"}'
```

## Interactive Documentation

The API provides interactive documentation via Swagger UI:

**URL:** `http://localhost:8000/docs`

This interface allows you to:
- View all available endpoints
- Test API calls directly in the browser
- See request/response schemas
- Download OpenAPI specification

Alternative documentation format:
**URL:** `http://localhost:8000/redoc`

## Rate Limits

Currently, there are no rate limits imposed by the API. However, response time depends on:
- Local machine performance
- AI model size and complexity
- Question complexity
- Ollama service load

## Error Codes

| Status Code | Description                                    |
|-------------|-----------------------------------------------|
| 200         | Success - AI response generated               |
| 422         | Validation Error - Invalid request format     |
| 500         | Internal Server Error - Ollama/AI model issue |

## Best Practices

### Request Optimization

1. **Be specific** in your questions for better responses
2. **Use clear language** - the AI responds better to well-formed questions
3. **Avoid extremely long prompts** - they may cause timeouts

### Error Handling

Always implement proper error handling in your applications:

```python
import requests

def robust_ai_request(question):
    try:
        response = requests.post(
            "http://localhost:8000/ask",
            json={"message": question},
            timeout=30  # 30 second timeout
        )
        response.raise_for_status()
        return response.json()["response"]
    
    except requests.exceptions.Timeout:
        return "Request timed out - try a shorter question"
    except requests.exceptions.ConnectionError:
        return "Cannot connect to AI service - is it running?"
    except requests.exceptions.HTTPError as e:
        return f"HTTP error occurred: {e}"
    except Exception as e:
        return f"Unexpected error: {e}"
```

### Performance Considerations

- **Cache responses** for identical questions
- **Use connection pooling** for multiple requests
- **Implement retries** for transient failures
- **Set appropriate timeouts** based on question complexity

## Monitoring and Logging

The service logs requests and responses. Check the console output or log files for:
- Request timing
- Error messages
- Model loading status
- Ollama connection status

---

For more information, visit the main [README.md](./README.md) file.