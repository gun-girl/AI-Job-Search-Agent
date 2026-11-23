import os

from dotenv import load_dotenv
from google import genai
from google.genai import types


# Load environment variables
load_dotenv()


def get_gemini_client():
    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        raise ValueError(
            "GEMINI_API_KEY is missing. Check your .env file."
        )

    return genai.Client(api_key=api_key)


def get_gemini_model():
    return os.getenv(
        "GEMINI_MODEL",
        "gemini-3.5-flash-lite"
    )


def generate_ai_response(prompt: str) -> str:
    client = get_gemini_client()

    response = client.models.generate_content(
        model=get_gemini_model(),
        contents=prompt
    )

    if not response.text:
        raise ValueError("Gemini returned an empty response.")

    return response.text


def generate_ai_json_response(prompt: str) -> str:
    client = get_gemini_client()

    response = client.models.generate_content(
        model=get_gemini_model(),
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json"
        )
    )

    if not response.text:
        raise ValueError("Gemini returned an empty response.")

    return response.text