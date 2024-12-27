from flask import Flask, render_template_string
from email_auth import authenticate_gmail
from email_utils import get_email_body

app = Flask(__name__)

@app.route('/email/<message_id>')
def email(message_id):
    service = authenticate_gmail()
    body = get_email_body(service, message_id)
    
    if body:
        # Render the email content as HTML
        return render_template_string(body)
    else:
        return render_template_string("<html><body><h1>No content found in this email.</h1></body></html>")

def start_server():
    """Start the Flask server."""
    app.run(port=5000)
