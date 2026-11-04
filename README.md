# LLM Contextual Chatbot

An AI-powered contextual chatbot built using **Google Gemini, FastAPI, and Streamlit**. The application supports multi-turn conversations, maintains conversation history, manages context windows, and provides a simple interactive chat interface.

## Project Overview

This project demonstrates the development of a contextual chatbot using a Large Language Model (LLM) through a real API.

Unlike a basic question-answering chatbot, this application maintains separate conversation histories and uses previous messages to generate context-aware responses.

## Objectives

- Integrate a real LLM API using Google Gemini.
- Implement multi-turn conversational functionality.
- Maintain separate histories for different conversations.
- Manage context windows by limiting the number of messages sent to the LLM.
- Configure chatbot personality and behaviour using a system prompt.
- Implement API error handling and request timeouts.
- Develop an interactive frontend using Streamlit.
- Build a REST API backend using FastAPI.

## Technologies Used

| Technology | Purpose |
|---|---|
| Python | Core programming language |
| Google Gemini API | LLM response generation |
| FastAPI | Backend REST API |
| Streamlit | Interactive chatbot frontend |
| Pydantic | Request data validation |
| UUID | Unique conversation identification |
| python-dotenv | Environment variable management |
| Requests | HTTP communication |
| Git and GitHub | Version control |

## System Architecture

The application follows a frontend-backend architecture.

1. **Streamlit Frontend:** Accepts user messages and displays chatbot responses.
2. **FastAPI Backend:** Processes requests, manages conversation IDs, and maintains conversation history.
3. **Context Manager:** Selects recent messages based on a configurable history limit.
4. **Google Gemini API:** Generates responses using conversation context and system instructions.

### Architecture Flow

```text
        User
         |
         v
  Streamlit Frontend
         |
         | HTTP / JSON
         v
   FastAPI Backend
         |
         v
 Conversation Manager
         |
         v
  Context Window Manager
         |
         v
   Google Gemini API
         |
         v
   Generated Response
         |
         v
  Streamlit Frontend
```

## Project Structure

```text
llm-contextual-chatbot/
│
├── main.py
├── frontend.py
├── test_api.py
├── requirements.txt
├── .gitignore
└── README.md
```

## Features

### 1. LLM API Integration
Uses the Google Gemini API to generate intelligent responses.

### 2. Multi-turn Conversations
Maintains conversational context across multiple user messages.

### 3. Conversation Isolation
Each conversation receives a unique UUID. Starting a new conversation creates a separate history.

### 4. Context Window Management
Uses a sliding-window approach to send only the most recent messages to Gemini, reducing unnecessary context and token usage.

### 5. System Prompt
Defines the chatbot's personality, response style, and behaviour.

### 6. Error Handling
Handles API errors, rate limits, timeouts, and backend connection failures.

### 7. Interactive Frontend
Provides a Streamlit chat interface with message history and a new-conversation option.

### 8. Secure API Key Management
Loads the Gemini API key from environment variables rather than hardcoding credentials.

## Installation and Setup

### Prerequisites

- Python 3.10 or later
- Git
- Google Gemini API key

### Step 1: Clone the Repository

```bash
git clone https://github.com/ShajeeaMinnath/llm-contextual-chatbot.git
cd llm-contextual-chatbot
```

### Step 2: Create a Virtual Environment

```bash
python -m venv venv
```

Activate it on Windows:

```powershell
.\venv\Scripts\Activate.ps1
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Configure the API Key

Create a file named `.env` in the project root directory.

Add your Gemini API key:

```env
GEMINI_API_KEY=your_gemini_api_key
```

Obtain an API key from [Google AI Studio](https://aistudio.google.com/apikey).

**Important:** Never upload your `.env` file or expose your API key publicly.

### Step 5: Start the FastAPI Backend

Open the first terminal and run:

```bash
uvicorn main:app --reload
```

Backend URL:

```text
http://127.0.0.1:8000
```

API documentation:

```text
http://127.0.0.1:8000/docs
```

### Step 6: Start the Streamlit Frontend

Open a second terminal, activate the virtual environment, and run:

```bash
streamlit run frontend.py
```

Frontend URL:

```text
http://localhost:8501
```

The chatbot is now ready to use.

## Testing

The application was tested with the following scenarios:

| Test Case | Expected Result | Status |
|---|---|---|
| Basic chatbot interaction | Generates a response | Passed |
| Multi-turn conversation | Retains previous context | Passed |
| Conversation continuity | Recalls previously provided information | Passed |
| Conversation isolation | Does not share context