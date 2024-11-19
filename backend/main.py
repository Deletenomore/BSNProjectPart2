# backend/main.py
import sys
import os

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict
from models.chatbot import process_prompt  # Import the chatbot processing function
from dotenv import load_dotenv

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Load environment variables
load_dotenv()

app = FastAPI()

# Configure CORS to allow requests from the frontend URL
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Adjust this to your frontend's URL
    # allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    #allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define a variable to store the last chatbot response
last_chatbot_response = {"response": ""}

# Create a Pydantic model for prompt data
class ChatbotPrompt(BaseModel):
    prompt: str

@app.post("/chatbot/")
async def chatbot_interaction(prompt: ChatbotPrompt):
    """
    Endpoint to interact with the AI chatbot.
    """
    global last_chatbot_response  # Use the global variable to store the response
    try:
        print(f"Received prompt: {prompt.prompt}")
        string_prompt = prompt.prompt  # Extract the 'prompt' field as a string
        if not isinstance(string_prompt, str):
            raise ValueError(f"Expected a string prompt. Got: {type(string_prompt)}")
        response = process_prompt(string_prompt)  # Pass the prompt to the AI processing function
        #print(f"Generated response: {response}")
        last_chatbot_response["response"] = response  # Store the response
        return {"response": response}
    except Exception as e:
        print(f"Error in /chatbot/ endpoint: {e}")
        raise HTTPException(status_code=500, detail=f"Chatbot interaction failed: {str(e)}")

@app.get("/results/")
async def fetch_results():
    """
    Endpoint to fetch the last chatbot response.
    """
    try:
        # Retrieve the last stored response
        if last_chatbot_response["response"]:
            return {"results": last_chatbot_response["response"]}
        else:
            return {"results": "No chatbot response available yet."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Fetching results failed: {str(e)}")
