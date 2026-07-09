import os
from dotenv import load_dotenv
from google import genai

load_dotenv()  # reads .env and loads GEMINI_API_KEY into the environment

api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    raise SystemExit("GEMINI_API_KEY not found -- check your .env file")

client = genai.Client(api_key=api_key)

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="Reply with exactly one word: hello"
)

print("Gemini replied:", response.text)