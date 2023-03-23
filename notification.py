from email.message import EmailMessage
import ssl
import smtplib
import random
from flask import session

def send_notification(receiver):
    email_address = "martin.v.doychinov@gmail.com"
    email_password = "alrxkirjonmjqmxl"
    email_receiver = receiver

    subject = "New friend invitation"
    body = """
    You have a new friend invitation! Please check your account!
    """

    em = EmailMessage()
    em['Form'] = email_address
    em['To'] = email_receiver
    em['Subject'] = subject
    em.set_content(body)

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(email_address, email_password)
        smtp.sendmail(email_address, email_receiver, em.as_string())
