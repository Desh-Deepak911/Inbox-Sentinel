from apscheduler.schedulers.blocking import BlockingScheduler

from inbox_sentinel.ai.email_classifier import classify_email_with_ai
from inbox_sentinel.classifiers.rule_classifier import classify_email
from inbox_sentinel.config.loader import load_config
from inbox_sentinel.digest.generator import generate_digest
from inbox_sentinel.gmail.client import fetch_unread_emails
from inbox_sentinel.memory.sqlite_store import (
    init_db,
    is_email_processed,
    reminder_exists_for_email,
    save_processed_email,
    save_reminder,
)
from inbox_sentinel.notifications.notifier import notify_email
from inbox_sentinel.reminders.reminder_agent import create_reminder

PRIORITY_ORDER = {
    "LOW": 1,
    "MEDIUM": 2,
    "HIGH": 3,
}


def should_use_ai(email, config):
    if not config["ai"]["enabled"]:
        return False

    minimum_priority = config["ai"]["minimum_priority"]

    return PRIORITY_ORDER[email["priority"]] >= PRIORITY_ORDER[minimum_priority]

def process_inbox():
    config = load_config()

    max_results = config["gmail"]["max_results"]
    notifications_enabled = config["notifications"]["enabled"]
    notifiable_priorities = set(config["notifications"]["priorities"])
    ai_model = config["ai"]["model"]

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

    classified_emails = []

    for email in new_emails:
        rule_result = classify_email(email)

        if should_use_ai(rule_result, config):
            ai_result = classify_email_with_ai(rule_result, model=ai_model)

            rule_result["ai_priority"] = ai_result.get(
                "priority",
                rule_result["priority"],
            )
            rule_result["ai_reason"] = ai_result.get("reason", "")
            rule_result["suggested_action"] = ai_result.get("suggested_action", "")
            rule_result["confidence"] = ai_result.get("confidence", 0.0)
            rule_result["priority"] = rule_result["ai_priority"]

        classified_emails.append(rule_result)

    classified_emails.sort(
        key=lambda email: PRIORITY_ORDER[email["priority"]],
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
            print("   Rule Reasons:")
            for reason in email["reasons"]:
                print(f"   - {reason}")

        if email.get("ai_reason"):
            print(f"   AI Reason: {email['ai_reason']}")
            print(f"   Suggested Action: {email['suggested_action']}")
            print(f"   Confidence: {email['confidence']}")

        if notifications_enabled and email["priority"] in notifiable_priorities:
            notify_email(email)

        reminder = create_reminder(email)

        if reminder and not reminder_exists_for_email(email["id"]):
            save_reminder(reminder)

            print("   Reminder Created:")
            print(f"   - Remind At: {reminder['remind_at']}")
            print(f"   - Status: {reminder['status']}")

        save_processed_email(email)

        print("-" * 80)


def run_scheduler():
    config = load_config()
    interval_minutes = config["scheduler"]["interval_minutes"]

    scheduler = BlockingScheduler()

    scheduler.add_job(
        process_inbox,
        "interval",
        minutes=interval_minutes,
        next_run_time=None,
    )

    print(f"Inbox Sentinel is running every {interval_minutes} minutes.")
    print("Press Ctrl+C to stop.")

    process_inbox()
    scheduler.start()

def main():
    config = load_config()

    if config["scheduler"]["enabled"]:
        run_scheduler()
    else:
        process_inbox()
        print()
        print(generate_digest())


if __name__ == "__main__":
    main()