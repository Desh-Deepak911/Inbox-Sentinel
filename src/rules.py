URGENT_KEYWORDS = [
    "urgent",
    "asap",
    "deadline",
    "interview",
    "offer",
    "action required",
    "follow up",
    "final reminder",
]

IMPORTANT_SENDERS = [
    "recruiter",
    "careers",
    "hr",
    "hiring",
]


def classify_email(email):
    score = 0
    reasons = []

    subject = email.get("subject", "").lower()
    snippet = email.get("snippet", "").lower()
    sender = email.get("from", "").lower()

    text = f"{subject} {snippet}"

    for keyword in URGENT_KEYWORDS:
        if keyword in text:
            score += 3
            reasons.append(f'Contains keyword "{keyword}"')

    for sender_keyword in IMPORTANT_SENDERS:
        if sender_keyword in sender:
            score += 4
            reasons.append(f'Sender looks important: "{sender_keyword}"')

    if score >= 6:
        priority = "HIGH"
    elif score >= 3:
        priority = "MEDIUM"
    else:
        priority = "LOW"

    return {
        **email,
        "priority": priority,
        "score": score,
        "reasons": reasons,
    }