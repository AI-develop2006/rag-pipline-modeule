import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables from the root folder if present
load_dotenv(os.path.join(os.path.dirname(__file__), "..", ".env"))

app = FastAPI(title="RAG FastAPI Backend")

# Configure CORS for local Next.js client testing
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    message: str

def load_knowledge_base() -> str:
    """Reads the local knowledge base text file."""
    kb_path = os.path.join(os.path.dirname(__file__), "knowledge_base.txt")
    if not os.path.exists(kb_path):
        raise FileNotFoundError(f"Knowledge base file not found at {kb_path}")
    with open(kb_path, "r", encoding="utf-8") as file:
        return file.read()

@app.post("/api/chat")
async def chat_endpoint(request: ChatRequest):
    """
    Accepts user message, reads knowledge base, prompts Gemini 1.5 Flash
    under strict system instructions, and returns the generated response.
    """
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key or api_key == "your_gemini_api_key_here":
        raise HTTPException(
            status_code=500,
            detail="GEMINI_API_KEY is not configured. Please set a valid API key in the .env file."
        )

    # Configure the Gemini client
    genai.configure(api_key=api_key)

    try:
        context = load_knowledge_base()
    except FileNotFoundError as e:
        raise HTTPException(status_code=500, detail=str(e))

    # Define system instruction strictly limiting the model's responses to knowledge base contents
    system_instruction = (
        "You are a strict, deterministic retrieval-augmented generation assistant. "
        "Your sole task is to answer user queries using only the information provided below "
        "inside the <knowledge_base> XML tag.\n\n"
        f"<knowledge_base>\n{context}\n</knowledge_base>\n\n"
        "CRITICAL RULES:\n"
        "1. Base your answer solely on the content inside the <knowledge_base> XML tags.\n"
        "2. Do not use any outside knowledge, assumptions, extrapolation, or web-based queries.\n"
        "3. If the answer cannot be found in the provided <knowledge_base> context, or if there is not "
        "enough information to answer the question, you must respond with exactly this text and nothing else: "
        "\"I am sorry, but I cannot find that information in the knowledge base.\"\n"
        "4. Do not prefix, suffix, explain, or modify the fallback statement. Respond exactly with that string."
    )

    try:
        # Use gemini-1.5-flash
        model = genai.GenerativeModel(
            model_name="gemini-1.5-flash",
            system_instruction=system_instruction
        )
        
        # Request content generation
        response = model.generate_content(request.message)
        
        # Extract text safely
        answer = response.text.strip() if response.text else "I am sorry, but I cannot find that information in the knowledge base."
        return {"response": answer}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Gemini API Error: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    # Read port from env or default to 8000
    port = int(os.getenv("PORT", "8000"))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)
