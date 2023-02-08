import re

from api.exceptions.clients.exceptions import InvalidCredentials, FirstNameWrongFormat, LastNameWrongFormat, \
    EmailWrongFormat, PhoneWrongFormat, TelegramWrongFormat
from api.schemas.clients.clients_schemas import ClientContactSchema


class ClientsDataVerifier:
    def __init__(self):
        self.password_min_len = 10
        self.password_max_len = 20

        self.login_min_len = 5
        self.login_max_len = 20

        self.first_name_min_len = 2
        self.first_name_max_len = 15

        self.last_name_min_len = 5
        self.last_name_max_len = 20

        self.telegram_min_len = 3
        self.telegram_max_len = 20

        self.phone_max_len = 12

        self.email_regex = re.compile(r"^([-!#-'*+/-9=?A-Z^-~]+(\.[-!#-'*+/-9=?A-Z^-~]+)*|\"([]!#-[^-~ \t]|(\\[\t -~]))+\")@([-!#-'*+/-9=?A-Z^-~]+(\.[-!#-'*+/-9=?A-Z^-~]+)*|\[[\t -Z^-~]*])")
        self.telegram_regex = re.compile(r'^@[a-zA-Z0-9_.+-]+')
        self.phone_regex = re.compile(r"^\+?[0-9]{9}")

    def verify_password(self, password: str) -> None:
        if len(password) < self.password_min_len or len(password) > self.password_max_len:
            raise InvalidCredentials()

    def verify_login(self, login: str) -> None:
        if len(login) < self.login_min_len or len(login) > self.login_max_len:
            raise InvalidCredentials()

    def verify_first_name(self, first_name: str) -> None:
        if len(first_name) < self.first_name_min_len or len(first_name) > self.first_name_max_len:
            raise FirstNameWrongFormat()

    def verify_last_name(self, last_name: str) -> None:
        if len(last_name) < self.last_name_min_len or len(last_name) > self.last_name_max_len:
            raise LastNameWrongFormat()

    def verify_contact(self, client_contact_schema: ClientContactSchema):
        self.verify_email(client_contact_schema.email)
        self.verify_phone(client_contact_schema.phone)
        self.verify_telegram(client_contact_schema.telegram)

    def verify_email(self, email: str) -> None:
        if not re.fullmatch(self.email_regex, email):
            raise EmailWrongFormat()

    def verify_phone(self, phone: str) -> None:
        if not re.fullmatch(self.phone_regex, phone) or len(phone) > self.phone_max_len:
            raise PhoneWrongFormat()

    def verify_telegram(self, telegram: str) -> None:
        if not re.fullmatch(self.telegram_regex, telegram) \
               or (len(telegram) < self.telegram_min_len or len(telegram) > self.telegram_max_len):
            raise TelegramWrongFormat()

