from config import load_config
from db import init_db, is_email_processed, save_processed_email
from gmail_client import fetch_unread_emails
from notifier import notify_email
from rules import classify_email


def main():
    config = load_config()

    max_results = config["gmail"]["max_results"]
    notifications_enabled = config["notifications"]["enabled"]
    notifiable_priorities = set(config["notifications"]["priorities"])

    init_db()

    emails = fetch_unread_emails(max_results=max_results)

    if not emails:
        print("No unread emails found.")
        return

    new_emails = [
        email for email in emails
        if not is_email_processed(email["id"])
    ]

    if not new_emails:
        print("No new unread emails to process.")
        return

    classified_emails = [classify_email(email) for email in new_emails]

    classified_emails.sort(
        key=lambda email: email["score"],
        reverse=True,
    )

    print(f"Found {len(classified_emails)} new unread email(s):\n")

    for index, email in enumerate(classified_emails, start=1):
        print(f"{index}. [{email['priority']}] {email['subject']}")
        print(f"   Score: {email['score']}")
        print(f"   From: {email['from']}")
        print(f"   Date: {email['date']}")
        print(f"   Snippet: {email['snippet']}")

        if email["reasons"]:
            print("   Reasons:")
            for reason in email["reasons"]:
                print(f"   - {reason}")

        if notifications_enabled and email["priority"] in notifiable_priorities:
            notify_email(email)

        save_processed_email(email)

        print("-" * 80)


if __name__ == "__main__":
    main()