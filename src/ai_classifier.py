import json
import os

from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

def classify_email_with_ai(email, model="gemini-2.5-flash"):
    prompt = f"""
Classify this email.

Sender: {email.get('from')}
Subject: {email.get('subject')}
Snippet: {email.get('snippet')}

Return ONLY JSON:

{{
    "priority": "HIGH|MEDIUM|LOW",
    "reason": "...",
    "suggested_action": "...",
    "confidence": 0.0
}}
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
    )

    try:
        return json.loads(response.text)
    except Exception:
        return {
            "priority": email["priority"],
            "reason": "Unable to parse AI response",
            "suggested_action": "Review manually",
            "confidence": 0.0,
        }