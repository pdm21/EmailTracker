def move_emails_to_label(service, message_ids, label_id):
    """Move emails to the specified label and remove them from the inbox."""
    for msg_id in message_ids:
        # Add the label
        service.users().messages().modify(
            userId='me',
            id=msg_id,
            body={'addLabelIds': [label_id], 'removeLabelIds': ['INBOX']}
        ).execute()
