from email_auth import authenticate_gmail
import base64

def fetch_recent_emails(service, max_results=20):
    """Fetch recent emails and list their senders."""
    # Exclude emails with the 'EmailTracker/Unsubscribe' label
    exclude_label = "label:EmailTracker/Unsubscribe"

    # Add a query to fetch only inbox emails excluding already processed ones
    query = f"in:inbox -{exclude_label}"
    
    results = service.users().messages().list(userId='me', maxResults=max_results, q=query).execute()
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
    results = service.users().messages().list(userId='me', maxResults=100, q=query).execute()
    messages = results.get('messages', [])
    return [msg['id'] for msg in messages]

def get_email_body(service, message_id):
    """Fetch the body of an email by its ID."""
    try:
        message = service.users().messages().get(userId='me', id=message_id, format='full').execute()
        payload = message.get('payload', {})
        body = None

        # Check for the main body
        if 'parts' in payload:
            for part in payload['parts']:
                if part['mimeType'] == 'text/html':  # Look for HTML content
                    body = part['body'].get('data')
                    break
                elif part['mimeType'] == 'text/plain':  # Fall back to plain text
                    body = part['body'].get('data')
                    break
        else:
            # Directly check the body if there are no parts
            body = payload.get('body', {}).get('data')

        if body:
            # Decode the body
            return base64.urlsafe_b64decode(body).decode('utf-8')
        else:
            return "No content found in this email."
    except Exception as e:
        return f"Error fetching email body: {str(e)}"

def get_or_create_label(service, label_name):
    """Get or create a label in Gmail."""
    labels = service.users().labels().list(userId='me').execute().get('labels', [])
    for label in labels:
        if label['name'] == label_name:
            return label['id']
    
    # If label doesn't exist, create it
    label_body = {
        'name': label_name,
        'labelListVisibility': 'labelShow',
        'messageListVisibility': 'show'
    }
    label = service.users().labels().create(userId='me', body=label_body).execute()
    return label['id']

def move_emails_to_label(service, message_ids, label_id):
    """Move emails to the specified label and remove them from the inbox."""
    for msg_id in message_ids:
        # Add the label
        service.users().messages().modify(
            userId='me',
            id=msg_id,
            body={'addLabelIds': [label_id], 'removeLabelIds': ['INBOX']}
        ).execute()
