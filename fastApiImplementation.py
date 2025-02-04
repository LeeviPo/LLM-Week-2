# Installing the required libraries
!pip install fastapi uvicorn nest_asyncio python-multipart googletrans==4.0.0-rc1 requests

import nest_asyncio
import uuid
import threading
import uvicorn
from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel
from googletrans import Translator

# Apparently FastAPI needs an ASGI server (uvicorn) and it cannot be run in
# colab without async as colab is already an event loop?
nest_asyncio.apply()

# Generating an API token
API_TOKEN = str(uuid.uuid4())
print("Generated API token:", API_TOKEN)

# Creating a FastAPI app
app = FastAPI()

# Initializing the translator
translator = Translator()

class TranslationRequest(BaseModel):
    text: str

# Defining the translation endpoint
@app.post("/translate")
async def translate_text(request: TranslationRequest, authorization: str = Header(...)):
    # Checking the API token (passed in the Authorization header)
    if authorization != API_TOKEN:
        raise HTTPException(status_code=401, detail="Invalid API token")
    # Translate text from English to Finnish
    translated = translator.translate(request.text, src='en', dest='fi')
    return {"translated_text": translated.text}

# Running the Uvicorn server
def run_server():
    uvicorn.run(app, host="0.0.0.0", port=8000)

# Running the server in a background thread
server_thread = threading.Thread(target=run_server, daemon=True)
server_thread.start()

import requests

# Defining the API endpoint
url = "http://0.0.0.0:8000/translate"

# Setting the headers to include the generated API token
headers = {"Authorization": API_TOKEN}

# Preparing the request payload with text in English
payload = {"text": "Hello, how are you?"}

# Sending a POST request to the API
response = requests.post(url, json=payload, headers=headers)
print("API response:", response.json())
