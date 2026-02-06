import os

from dotenv import load_dotenv
from google import genai

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    raise RuntimeError("API key not found")

client = genai.Client(api_key=api_key)

content = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="Why is Boot.dev such a great place to learn backend development? Use one paragraph maximum.",
)

print(f"Prompt tokens: {content.usage_metadata.prompt_token_count}")  # type: ignore
print(f"Response tokens: {content.usage_metadata.candidates_token_count}")  # type: ignore

print(content.text)
