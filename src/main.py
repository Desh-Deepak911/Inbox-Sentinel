from gmail_client import get_gmail_service


def main():
    service = get_gmail_service()
    profile = service.users().getProfile(userId="me").execute()

    print("Inbox Sentinel connected successfully.")
    print(f"Email: {profile.get('emailAddress')}")


if __name__ == "__main__":
    main()