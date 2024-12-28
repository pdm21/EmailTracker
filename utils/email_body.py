import base64

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
