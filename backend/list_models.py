import os
from google import genai
from dotenv import load_dotenv

# Load from .env
load_dotenv(os.path.join(os.path.dirname(__file__), "..", ".env"))

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    print("Error: GEMINI_API_KEY not found in .env file")
    exit(1)

client = genai.Client(api_key=api_key)

try:
    print("Listing available models that support generateContent:")
    for m in client.models.list():
        actions = getattr(m, 'supported_actions', []) or []
        if any(act.lower() in ['generatecontent', 'generate_content'] for act in actions):
            print(f"- {m.name} (displayName: {getattr(m, 'display_name', m.name)})")
except Exception as e:
    print(f"Error fetching models: {e}")

