
import os
from dotenv import load_dotenv
from google import genai

from main import SYSTEM_PROMPT

# Load environment variables
load_dotenv()

# Retrieve Gemini API key
api_key = os.getenv("GEMINI_API_KEY")

# Check whether the API key exists
if not api_key:
    raise ValueError("GEMINI_API_KEY is missing!")

# Create Gemini client
client = genai.Client(api_key=api_key)

try:
    # Send a request to Gemini
    response = client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents="Explain what artificial intelligence is in two sentences.",
        config={
         "system_instruction": SYSTEM_PROMPT
        }
    )

    # Display the generated response
    print("Chatbot:", response.text)

except Exception as e:
    print("An error occurred:", str(e))
