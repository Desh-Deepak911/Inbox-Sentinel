import json

from inbox_sentinel.ai.email_classifier import client

def should_generate_reply_draft(email):
    priority = email.get("priority")
    suggested_action = (email.get("suggested_action") or "").lower()

    if priority not in {"HIGH", "MEDIUM"}:
        return False

    reply_signals = [
        "reply",
        "respond",
        "send",
        "share",
        "confirm",
        "provide",
        "follow up",
    ]

    return any(signal in suggested_action for signal in reply_signals)


def create_reply_draft_request(email):
    if not should_generate_reply_draft(email):
        return None

    return {
        "email_id": email.get("id"),
        "thread_id": email.get("thread_id"),
        "sender": email.get("from"),
        "subject": email.get("subject"),
        "priority": email.get("priority"),
        "reason": email.get("ai_reason"),
        "suggested_action": email.get("suggested_action"),
        "status": "pending",
    }

def generate_reply_body(email, model="gemini-2.5-flash"):
    prompt = f"""
You are helping the user draft a professional email reply.

Write a concise, polite reply.

Do not invent facts.
If information is missing, use a placeholder like [your availability] or [required document].

Original email:
From: {email.get("from")}
Subject: {email.get("subject")}
Snippet: {email.get("snippet")}

Suggested action:
{email.get("suggested_action")}

Return ONLY JSON:
{{
  "reply_body": "email body here"
}}
"""

    response = client.models.generate_content(
        model=model,
        contents=prompt,
    )

    try:
        return json.loads(response.text).get("reply_body")
    except Exception:
        return None