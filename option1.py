from email_auth import authenticate_gmail
from email_utils import fetch_recent_emails, fetch_emails_from_sender, get_or_create_label, move_emails_to_label
from filters import create_filter_for_sender

def option1():
    service = authenticate_gmail()
    emails = fetch_recent_emails(service)

    if not emails:
        print("No emails found.")
        return

    print("\nSelect a sender by entering the corresponding number:\n")
    senders = {idx + 1: email for idx, email in enumerate(emails)}
    for idx, email in enumerate(emails):
        print(f"{idx + 1}. Sender: {email['sender']}, Subject: {email['subject']}")

    try:
        choice = int(input("\nEnter the number: "))
        if choice not in senders:
            print("Invalid choice.")
            return

        selected_email = senders[choice]
        sender_email = selected_email['sender']
        message_ids = fetch_emails_from_sender(service, sender_email)

        if not message_ids:
            print(f"No emails found from {sender_email}.")
            return

        label_id = get_or_create_label(service, "EmailTracker/Unsubscribe")
        move_emails_to_label(service, message_ids, label_id)
        create_filter_for_sender(service, sender_email, label_id)
        print(f"Emails moved, and future emails from {sender_email} will be filtered.")

    except ValueError:
        print("Please enter a valid number.")

