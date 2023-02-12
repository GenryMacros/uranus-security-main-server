from flask import Flask
from itsdangerous import SignatureExpired, BadTimeSignature

from api.exceptions.clients.exceptions import InvalidTokens, InvalidCredentials, SignupFailed, ClientExists, \
    ClientNotFound, TokenIsExpired, FirstNameWrongFormat, LastNameWrongFormat, EmailWrongFormat, PhoneWrongFormat, \
    TelegramWrongFormat
from api.exceptions.clients.handlers.exceptions_handlers import handle_invalid_tokens_exception, \
    handle_signup_failure_exception, handle_invalid_credentials_exception, handle_client_exists_exception, \
    handle_client_not_found_exception, handle_token_expired_exception, handle_first_name_format_exception, \
    handle_last_name_format_exception, handle_email_format_exception, handle_phone_format_exception, \
    handle_telegram_format_exception, handle_signature_expired_exception, handle_signature_invalid_exception
from api.exceptions.universal.exceptions import InvalidRequest
from api.exceptions.universal.handlers.exception_handlers import handle_invalid_request_exception, \
    handle_value_exception
from api.routes.clients.clients_routes import logging_blueprint


def register_error_handlers(app: Flask):
    app.register_error_handler(InvalidTokens, handle_invalid_tokens_exception)
    app.register_error_handler(InvalidCredentials, handle_invalid_credentials_exception)
    app.register_error_handler(SignupFailed, handle_signup_failure_exception)
    app.register_error_handler(ClientExists, handle_client_exists_exception)
    app.register_error_handler(ClientNotFound, handle_client_not_found_exception)
    app.register_error_handler(TokenIsExpired, handle_token_expired_exception)
    app.register_error_handler(InvalidRequest, handle_invalid_request_exception)
    app.register_error_handler(FirstNameWrongFormat, handle_first_name_format_exception)
    app.register_error_handler(LastNameWrongFormat, handle_last_name_format_exception)
    app.register_error_handler(EmailWrongFormat, handle_email_format_exception)
    app.register_error_handler(PhoneWrongFormat, handle_phone_format_exception)
    app.register_error_handler(TelegramWrongFormat, handle_telegram_format_exception)
    app.register_error_handler(SignatureExpired, handle_signature_expired_exception)
    app.register_error_handler(BadTimeSignature, handle_signature_invalid_exception)
    app.register_error_handler(ValueError, handle_value_exception)

def register_blueprints(app: Flask):
    app.register_blueprint(logging_blueprint)
    pass


if __name__ == '__main__':
    app = Flask(__name__, template_folder='templates')
    register_blueprints(app)
    register_error_handlers(app)
    app.run(host="localhost", port=8010)
