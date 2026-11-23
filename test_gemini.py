from app.services.ai_service import generate_ai_response


prompt = """
You are an AI job-search assistant.

Explain in three bullet points how AI can help
a junior Python developer find suitable jobs.
"""

answer = generate_ai_response(prompt)

print("\nGemini response:\n")
print(answer)