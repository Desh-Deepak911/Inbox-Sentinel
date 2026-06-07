from inbox_sentinel.config.loader import load_config


def classify_email(email):
    config = load_config()

    urgent_keywords = config["priority"]["urgent_keywords"]
    important_senders = config["priority"]["important_senders"]

    score = 0
    reasons = []

    subject = email.get("subject", "").lower()
    snippet = email.get("snippet", "").lower()
    sender = email.get("from", "").lower()

    text = f"{subject} {snippet}"

    for keyword in urgent_keywords:
        if keyword.lower() in text:
            score += 3
            reasons.append(f'Contains keyword "{keyword}"')

    for sender_keyword in important_senders:
        if sender_keyword.lower() in sender:
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