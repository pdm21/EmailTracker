from email_auth import authenticate_gmail

def fetch_recent_emails(service, max_results=20):
    """Fetch recent emails and list their senders."""
    results = service.users().messages().list(userId='me', maxResults=max_results).execute()
    messages = results.get('messages', [])

    if not messages:
        print("No emails found.")
        return []

    email_list = []
    for msg in messages:
        message = service.users().messages().get(userId='me', id=msg['id'], format='full').execute()
        headers = message['payload'].get('headers', [])
        sender = "Unknown"
        subject = "No Subject"
        for header in headers:
            if header['name'].lower() == 'from':  # Get sender
                sender = header['value']
            if header['name'].lower() == 'subject':  # Get subject
                subject = header['value']
        email_list.append({"sender": sender, "subject": subject, "id": msg['id']})

    return email_list

def main():
    service = authenticate_gmail()
    print("Fetching the last 100 emails...")
    emails = fetch_recent_emails(service)

    if not emails:
        print("No emails found.")
    else:
        print(f"\nFound {len(emails)} emails:\n")
        for idx, email in enumerate(emails):
            print(f"{idx + 1}. Sender: {email['sender']}, Subject: {email['subject']}")

if __name__ == '__main__':
    main()
