def create_filter_for_sender(service, sender_email, label_id):
    """Create a Gmail filter to route future emails from a sender to a specific label."""
    filter_body = {
        "criteria": {"from": sender_email},
        "action": {"addLabelIds": [label_id], "removeLabelIds": ["INBOX"]}
    }
    service.users().settings().filters().create(userId='me', body=filter_body).execute()
    print(f"Filter created for {sender_email}. Future emails will go to the specified folder.")

