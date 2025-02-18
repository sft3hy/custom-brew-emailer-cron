import smtplib
import ssl
from email.message import EmailMessage
import os

# Define email sender and receiver
email_sender = 'custombrew1@gmail.com'
email_password = os.environ['CUSTOM_BREW_EMAIL_PASSWORD']

def send_email(subject: str, body: str, email_recipient: str):
    # Create email message
    em = EmailMessage()
    em['From'] = "Custom Brew"
    em['To'] = email_recipient
    em['Subject'] = subject

    # Set email content as HTML
    em.add_alternative(body, subtype='html')

    # Add SSL (layer of security)
    context = ssl.create_default_context()

    # Log in and send the email
    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(email_sender, email_password)
        smtp.sendmail(email_sender, email_recipient, em.as_string())
        print(f'Sent email to {email_recipient}')

# send_email("poo", "poooo", "smaueltown@gmail.com")