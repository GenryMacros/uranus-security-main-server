import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from flask import render_template


class ClientsConfirmator:

    def __init__(self):
        self.google_login = "uranussec@gmail.com"
        self.google_api_pass = "ivcoritxotjtqkcw"

    def send_email_confirmation(self, token: str, client_email: str):
        gmail_connection = smtplib.SMTP('smtp.gmail.com', 587)
        gmail_connection.starttls()
        gmail_connection.login(self.google_login, self.google_api_pass)

        html = render_template('confirmation_template.html', confirm_token=token)
        message = self.gmail_form(client_email, html)
        gmail_connection.sendmail(self.google_login, client_email, message.as_string())
        gmail_connection.quit()

    def gmail_form(self, to: str, html) -> MIMEMultipart:
        msg = MIMEMultipart('alternative')
        msg['Subject'] = "Link"
        msg['From'] = "Email confirmation"
        msg['To'] = to
        msg.preamble = ""
        msg.attach(MIMEText(html, 'html'))
        return msg
