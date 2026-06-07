from gmail_client import fetch_unread_emails


def main():
    emails = fetch_unread_emails(max_results=10)

    if not emails:
        print("No unread emails found.")
        return

    print(f"Found {len(emails)} unread email(s):\n")

    for index, email in enumerate(emails, start=1):
        print(f"{index}. {email['subject']}")
        print(f"   From: {email['from']}")
        print(f"   Date: {email['date']}")
        print(f"   Snippet: {email['snippet']}")
        print("-" * 80)


if __name__ == "__main__":
    main()