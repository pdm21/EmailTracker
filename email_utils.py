from email_auth import authenticate_gmail

def fetch_recent_emails(service, max_results=100):
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

def fetch_emails_from_sender(service, sender_email):
    """Fetch the IDs of emails from a specific sender."""
    query = f"from:{sender_email}"
    results = service.users().messages().list(userId='me', maxResults=10, q=query).execute()
    messages = results.get('messages', [])
    return [msg['id'] for msg in messages]
