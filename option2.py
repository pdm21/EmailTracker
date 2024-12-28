from utils.email_auth import authenticate_gmail
from utils.email_fetch import fetch_recent_emails, fetch_emails_from_sender
from utils.label_utils import get_or_create_label
from utils.email_move import move_emails_to_label
from utils.filters import create_filter_for_sender

def option2():
    service = authenticate_gmail()
    emails = fetch_recent_emails(service)

    if not emails:
        print("No emails found.")
        return

    print("\nSelect senders to create a new folder and filter future emails.\n")
    senders = {idx + 1: email for idx, email in enumerate(emails)}
    for idx, email in enumerate(emails):
        print(f"{idx + 1}. Sender: {email['sender']}, Subject: {email['subject']}")

    try:
        choices = input("\nEnter numbers for senders (comma-separated): ")
        selected_numbers = [int(num.strip()) for num in choices.split(",")]

        selected_senders = [senders[num] for num in selected_numbers if num in senders]
        new_label_name = input("Enter a name for the new folder: ")

        label_id = get_or_create_label(service, new_label_name)

        for email in selected_senders:
            sender_email = email['sender']
            message_ids = fetch_emails_from_sender(service, sender_email)

            if not message_ids:
                print(f"No emails found from {sender_email}.")
                continue

            move_emails_to_label(service, message_ids, label_id)
            create_filter_for_sender(service, sender_email, label_id)
            print(f"Emails moved and future emails from {sender_email} will be filtered to {new_label_name}.")

    except ValueError:
        print("Please enter valid numbers.")

