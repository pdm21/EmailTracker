import webbrowser
from threading import Thread
from email_auth import authenticate_gmail
from email_utils import fetch_recent_emails, fetch_emails_from_sender
from email_server import start_server

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
        print(f"{idx + 1}. {sender}")
        senders[idx + 1] = sender

    # Prompt user to select a sender
    try:
        choice = int(input("\nEnter the number: "))
        if choice not in senders:
            print("Invalid choice.")
            return
        selected_sender = senders[choice]
    except ValueError:
        print("Please enter a valid number.")
        return

    # Fetch emails from the selected sender
    email_ids = fetch_emails_from_sender(service, selected_sender)
    if not email_ids:
        print(f"No emails found for {selected_sender}.")
        return

    print(f"\nDisplaying email from {selected_sender}...")

    # Start the Flask server
    server_thread = Thread(target=start_server)
    server_thread.start()

    # Open the first email in the browser
    webbrowser.open(f'http://127.0.0.1:5000/email/{email_ids[0]}')

if __name__ == '__main__':
    main()
