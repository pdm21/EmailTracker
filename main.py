from email_auth import authenticate_gmail
from email_utils import fetch_recent_emails, fetch_emails_from_sender, get_or_create_label, move_emails_to_label

def main():
    service = authenticate_gmail()

    # Fetch recent emails
    emails = fetch_recent_emails(service)
    if not emails:
        print("No emails found.")
        return

    # Display the emails with a numbered list
    print("\nSelect a sender by entering the corresponding number:\n")
    senders = {}
    for idx, email in enumerate(emails):
        sender = email['sender']
        print(f"{idx + 1}. Sender: {sender}, Subject: {email['subject']}")
        senders[idx + 1] = email

    # Prompt user to select a sender
    try:
        choice = int(input("\nEnter the number: "))
        if choice not in senders:
            print("Invalid choice.")
            return
        selected_email = senders[choice]
        sender_email = selected_email['sender']
    except ValueError:
        print("Please enter a valid number.")
        return

    # Fetch emails from the selected sender
    message_ids = fetch_emails_from_sender(service, sender_email)
    if not message_ids:
        print(f"No emails found from {sender_email}.")
        return

    # Get or create the label
    label_id = get_or_create_label(service, "EmailTracker/Unsubscribe")

    # Move emails to the label
    print(f"Moving {len(message_ids)} emails from {sender_email} to 'EmailTracker/Unsubscribe' and removing them from the inbox...")
    move_emails_to_label(service, message_ids, label_id)

    print("Emails moved successfully!")

if __name__ == '__main__':
    main()
