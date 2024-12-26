from email_auth import authenticate_gmail

def fetch_unique_senders(service):
    """Fetch unique senders from the last 100 emails."""
    query = ''  # Fetch all emails
    results = service.users().messages().list(userId='me', maxResults=100, q=query).execute()
    messages = results.get('messages', [])

    if not messages:
        print("No emails found.")
        return []

    senders = set()  # Use a set to store unique senders
    for msg in messages:
        message = service.users().messages().get(userId='me', id=msg['id'], format='full').execute()
        headers = message['payload'].get('headers', [])
        
        for header in headers:
            if header['name'].lower() == 'from':  # Find the sender
                senders.add(header['value'])
                break

    return list(senders)

def main():
    service = authenticate_gmail()
    print("Fetching unique senders from the last 100 emails...")
    senders = fetch_unique_senders(service)

    if not senders:
        print("No senders found.")
    else:
        print(f"\nFound {len(senders)} unique senders:")
        for sender in senders:
            print(sender)

if __name__ == '__main__':
    main()

