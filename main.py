
import os
import uuid

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from google import genai
from google.genai import types, errors
import httpx


# Load environment variables
load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY is missing!")


# Initialize Gemini client with a 30-second timeout
client = genai.Client(
    api_key=api_key,
    http_options=types.HttpOptions(timeout=30000)
)


# Application configuration
app = FastAPI(
    title="LLM Contextual Chatbot",
    description="A chatbot powered by Google Gemini",
    version="1.0.0"
)


# Conversation storage
conversations = {}

MAX_HISTORY_MESSAGES = 10


# Chatbot personality
SYSTEM_PROMPT = """
You are a friendly, professional, and helpful AI assistant.

Follow these instructions:

1. Give clear and accurate answers.
2. Keep answers concise for simple questions.
3. Provide detailed explanations for technical questions.
4. Use simple language whenever possible.
5. Include examples when they help understanding.
6. Avoid unnecessary repetition.
7. Maintain a polite and encouraging tone.
8. Remember relevant information from the conversation
   when answering follow-up questions.
"""


# Request model
class ChatRequest(BaseModel):
    message: str
    conversation_id: str | None = None


# Home endpoint
@app.get("/")
def home():
    return {
        "message": "Welcome to the LLM Contextual Chatbot API!"
    }


# Chat endpoint
@app.post("/chat")
def chat(request: ChatRequest):

    try:

        # Create a new conversation if needed
        if request.conversation_id is None:

            conversation_id = str(uuid.uuid4())
            conversations[conversation_id] = []

        else:

            conversation_id = request.conversation_id

            if conversation_id not in conversations:
                raise HTTPException(
                    status_code=404,
                    detail="Conversation not found"
                )

        # Retrieve conversation history
        history = conversations[conversation_id]

        # Add current message temporarily
        messages_for_model = history + [
            {
                "role": "user",
                "content": request.message
            }
        ]

        # Keep only recent messages
        recent_messages = messages_for_model[-MAX_HISTORY_MESSAGES:]

        # Avoid starting with an isolated model response
        if recent_messages and recent_messages[0]["role"] == "model":
            recent_messages = recent_messages[1:]

        # Convert messages to Gemini format
        chat_history = []

        for message in recent_messages:
            chat_history.append({
                "role": message["role"],
                "parts": [{"text": message["content"]}]
            })

        print("Total stored messages:", len(history))
        print("Messages sent to Gemini:", len(recent_messages))

        # Generate Gemini response
        response = client.models.generate_content(
            model="gemini-3.5-flash-lite",
            contents=chat_history,
            config={
                "system_instruction": SYSTEM_PROMPT
            }
        )

        bot_response = response.text

        if not bot_response:
            raise HTTPException(
                status_code=502,
                detail="Gemini returned an empty response."
            )

        # Store successful interaction
        history.append({
            "role": "user",
            "content": request.message
        })

        history.append({
            "role": "model",
            "content": bot_response
        })

        return {
            "conversation_id": conversation_id,
            "user_message": request.message,
            "bot_response": bot_response
        }

    except HTTPException:
        raise

    except httpx.TimeoutException:
        raise HTTPException(
            status_code=504,
            detail="The request timed out. Please try again."
        )

    except errors.APIError as e:

        # Display actual error in VS Code terminal
        print("Gemini API Error:", repr(e))
        print("Error type:", type(e).__name__)
        print("Status code:", getattr(e, "code", None))

        status_code = getattr(e, "code", None)

        if status_code == 429:
            raise HTTPException(
                status_code=429,
                detail="API rate limit reached. Please try again later."
            )

        elif status_code in (401, 403):
            raise HTTPException(
                status_code=502,
                detail="Gemini API authentication failed. Check the API configuration."
            )

        else:
            raise HTTPException(
                status_code=502,
                detail="Gemini service is temporarily unavailable."
            )

    except Exception as e:

        # Temporary debugging information
        print("Unexpected error:", repr(e))

        raise HTTPException(
            status_code=502,
            detail="An unexpected error occurred. Please try again."
        )
