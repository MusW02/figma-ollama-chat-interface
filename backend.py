from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
# from fastapi.staticfiles import StaticFiles
# from fastapi.responses import FileResponse
import requests
import os
import json
from dotenv import load_dotenv
from pydantic import BaseModel

# Load environment variables
load_dotenv(override=True)

# Initialize FastAPI app
app = FastAPI(title="Figma-Ollama Chat Interface")

# Add CORS middleware to allow frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, restrict to your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Get environment variables
OLLAMA_API_KEY = os.environ.get('OLLAMA_API_KEY')
OLLAMA_MODEL = os.environ.get('OLLAMA_MODEL', 'deepseek-v3.1:671b-cloud')
FIGMA_ACCESS_TOKEN = os.environ.get('FIGMA_ACCESS_TOKEN')

# Pydantic models for request validation
class ChatMessage(BaseModel):
    message: str
    conversation_history: list = []

class FigmaRequest(BaseModel):
    file_id: str
    node_ids: str = None

# Ollama API function
def ask_ollama(prompt):
    """Send a prompt to Ollama and get a response"""
    if not OLLAMA_API_KEY:
        return "Error: Ollama API key not configured"
    
    try:
        headers = {
            "Authorization": f"Bearer {OLLAMA_API_KEY}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": OLLAMA_MODEL,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": 0.7,
                "top_p": 0.9,
                "top_k": 40,
            }
        }
        
        ollama_endpoint = os.environ.get('OLLAMA_ENDPOINT', 'https://ollama.com/api/generate')
        
        response = requests.post(
            ollama_endpoint,
            headers=headers,
            json=payload,
            timeout=60
        )
        response.raise_for_status()
        
        result = response.json()
        return result.get("response", "No response generated")
        
    except requests.RequestException as e:
        return f"Sorry, I couldn't get a response from the Ollama model: {e}"

# Figma API functions
def get_figma_file(file_id):
    """Fetch a Figma file by ID"""
    if not FIGMA_ACCESS_TOKEN:
        return {"error": "Figma access token not configured"}
    
    try:
        headers = {"X-FIGMA-TOKEN": FIGMA_ACCESS_TOKEN}
        response = requests.get(f"https://api.figma.com/v1/files/{file_id}?depth=1", headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        return {"error": f"Failed to fetch Figma file: {e}"}

# Figma API functions
# def get_figma_file(file_id):
#     """TEMPORARY MOCK: Bypasses the 429 error to test DeepSeek"""
    
#     return {
#         "name": "Mock Login Component",
#         "document": {
#             "id": "0:1",
#             "name": "Main Frame",
#             "type": "FRAME",
#             "children": [
#                 {
#                     "name": "Submit Button",
#                     "type": "RECTANGLE",
#                     "fills": [{"type": "SOLID", "color": {"r": 0.2, "g": 0.6, "b": 1.0}}],
#                     "cornerRadius": 8
#                 },
#                 {
#                     "name": "Button Text",
#                     "type": "TEXT",
#                     "characters": "Sign In",
#                     "style": {"fontFamily": "Inter", "fontWeight": 700, "fontSize": 16}
#                 }
#             ]
#         }
#     }
# API Routes
@app.post("/api/chat")
async def chat_with_llm(chat_message: ChatMessage):
    """Main chat endpoint that handles conversation with the LLM"""
    try:
        # Build the prompt with conversation history
        prompt = "Continue this conversation:\n"
        
        for msg in chat_message.conversation_history:
            role = "User" if msg.get("role") == "user" else "Assistant"
            prompt += f"{role}: {msg.get('content', '')}\n"
        
        prompt += f"User: {chat_message.message}\nAssistant:"
        
        # Get response from Ollama
        response = ask_ollama(prompt)
        
        return {
            "success": True,
            "response": response,
            "conversation_history": chat_message.conversation_history + [
                {"role": "user", "content": chat_message.message},
                {"role": "assistant", "content": response}
            ]
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/generate-from-figma")
async def generate_from_figma(figma_request: FigmaRequest):
    """Generate code from a Figma design"""
    try:
        # Get Figma file data
        figma_data = get_figma_file(figma_request.file_id)
        if "error" in figma_data:
            return {"success": False, "error": figma_data["error"]}
        
        # Prepare prompt for Ollama
        prompt = f"""
        Based on this Figma design information, generate clean HTML and CSS code.
        
        Figma File: {figma_data.get('name', 'Unknown')}
        Document Structure: {json.dumps(figma_data.get('document', {}), indent=2)}
        
        Please generate:
        1. Semantic HTML structure
        2. CSS styles (preferably using Flexbox/Grid)
        3. Responsive design considerations
        4. Clean, well-commented code
        
        Return the code in a single code block with appropriate language tags.
        """
        
        # Get code from Ollama
        response = ask_ollama(prompt)
        
        return {
            "success": True,
            "response": response
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "figma-ollama-chat"}

# # Serve frontend (we'll add this later)
# @app.get("/")
# async def serve_frontend():
#     return FileResponse("frontend/index.html")

# # Mount static files
# app.mount("/", StaticFiles(directory="frontend"), name="frontend")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
