from flask import Flask, render_template_string
from email_utils import fetch_recent_emails, fetch_emails_from_sender

app = Flask(__name__)

@app.route('/email/<message_id>')
def email(message_id):
    service = authenticate_gmail()
    body = get_email_body(service, message_id)
    if body:
        body = body.encode('utf-8').decode('utf-8')
    else:
        body = "No content found."
    return render_template_string(f"<html><body>{body}</body></html>")

def start_server():
    """Start the Flask server."""
    app.run(port=5000)
