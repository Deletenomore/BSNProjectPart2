# backend/main.py
import sys
import os

from fastapi import FastAPI, UploadFile, File, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict
import os
from models.chatbot import handle_user_prompt  # Import the chatbot processing function
from dotenv import load_dotenv

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Load environment variables
load_dotenv()

app = FastAPI()

# Configure CORS to allow requests from the frontend URL
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Adjust this to your frontend's URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create a Pydantic model for prompt data
class ChatbotPrompt(BaseModel):
    prompt: str

# Define an upload directory
UPLOAD_DIR = "./uploaded_files"
os.makedirs(UPLOAD_DIR, exist_ok=True)  # Create the directory if it doesn't exist

@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    """
    Endpoint to handle file uploads.
    """
    try:
        file_location = os.path.join(UPLOAD_DIR, file.filename)
        with open(file_location, "wb") as file_object:
            file_object.write(await file.read())
        return {"message": "File uploaded successfully", "file_location": file_location}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"File upload failed: {str(e)}")

@app.post("/chatbot/")
async def chatbot_interaction(prompt: ChatbotPrompt):
    """
    Endpoint to interact with the AI chatbot.
    """
    try:
        response = handle_user_prompt(prompt.dict())  # Pass the prompt to the AI processing function
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Chatbot interaction failed: {str(e)}")

@app.get("/results/")
async def fetch_results():
    """
    Endpoint to fetch results based on previous queries or analysis.
    """
    try:
        results = "Here are your results based on the query..."  # Replace with actual data fetching logic
        return {"results": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Fetching results failed: {str(e)}")
