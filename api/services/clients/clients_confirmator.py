import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from flask import render_template


class ClientsConfirmator:

    def __init__(self):
        self.google_login = "uranussec@gmail.com"
        self.google_api_pass = "ivcoritxotjtqkcw"

    def send_email_confirmation(self, token: str, client_email: str, confirmation_method):
        from api.services.clients.clients_services import ConfirmationMethod
        gmail_connection = smtplib.SMTP('smtp.gmail.com', 587)
        gmail_connection.starttls()
        gmail_connection.login(self.google_login, self.google_api_pass)

        if confirmation_method == ConfirmationMethod.SHORT_CODE:
            message = self.generate_confirmation_code_mail(token, client_email)
        elif confirmation_method == ConfirmationMethod.LINK:
            message = self.generate_confirmation_code_mail(token, client_email)
        else:
            raise NotImplementedError()
        gmail_connection.sendmail(self.google_login, client_email, message.as_string())
        gmail_connection.quit()

    def generate_confirmation_link_mail(self, token: str, client_email: str):
        confirm_url = f"http://localhost:8010/users/confirm?token={token}"
        html = render_template('confirmation_template.html', confirm=confirm_url)
        message = self.gmail_form(client_email, html)

        return message

    def generate_confirmation_code_mail(self, code: str, client_email: str):
        html = render_template('confirmation_template.html', confirm=code)
        message = self.gmail_form(client_email, html)

        return message

    def gmail_form(self, to: str, html) -> MIMEMultipart:
        msg = MIMEMultipart('alternative')
        msg['Subject'] = "Link"
        msg['From'] = "Email confirmation"
        msg['To'] = to
        msg.preamble = ""
        msg.attach(MIMEText(html, 'html'))
        return msg
