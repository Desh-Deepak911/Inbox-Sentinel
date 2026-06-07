from inbox_sentinel.memory.sqlite_store import get_recent_priority_emails

def generate_digest(limit=20):
    emails = get_recent_priority_emails(limit)

    if not emails:
        return "No priority emails found."

    digest_lines = []

    digest_lines.append("=" * 80)
    digest_lines.append("INBOX SENTINEL DAILY DIGEST")
    digest_lines.append("=" * 80)
    digest_lines.append("")

    high_priority = [
        email
        for email in emails
        if email["priority"] == "HIGH"
    ]

    medium_priority = [
        email
        for email in emails
        if email["priority"] == "MEDIUM"
    ]

    digest_lines.append(
        f"HIGH PRIORITY EMAILS ({len(high_priority)})"
    )

    for index, email in enumerate(high_priority, start=1):
        digest_lines.append(
            f"\n{index}. {email['subject']}"
        )

        digest_lines.append(
            f"   From: {email['sender']}"
        )

        digest_lines.append(
            f"   Action: {email.get('suggested_action')}"
        )

        digest_lines.append(
            f"   Confidence: {email.get('confidence')}"
        )

    digest_lines.append("")
    digest_lines.append(
        f"MEDIUM PRIORITY EMAILS ({len(medium_priority)})"
    )

    for index, email in enumerate(medium_priority, start=1):
        digest_lines.append(
            f"\n{index}. {email['subject']}"
        )

        digest_lines.append(
            f"   From: {email['sender']}"
        )

        digest_lines.append(
            f"   Action: {email.get('suggested_action')}"
        )

    return "\n".join(digest_lines)