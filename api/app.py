import json
from dataclasses import dataclass

import marshmallow
from flask import Flask
from itsdangerous import SignatureExpired, BadTimeSignature

from api.exceptions.cameras.exceptions import CamerasNotFound
from api.exceptions.cameras.handlers.exceptions_handlers import handle_cameras_exists_exception
from api.exceptions.clients.exceptions import InvalidTokens, InvalidCredentials, SignupFailed, ClientExists, \
    ClientNotFound, TokenIsExpired, FirstNameWrongFormat, LastNameWrongFormat, EmailWrongFormat, PhoneWrongFormat, \
    TelegramWrongFormat, TokenIsInvalid
from api.exceptions.clients.handlers.exceptions_handlers import handle_invalid_tokens_exception, \
    handle_signup_failure_exception, handle_invalid_credentials_exception, handle_client_exists_exception, \
    handle_client_not_found_exception, handle_token_expired_exception, handle_first_name_format_exception, \
    handle_last_name_format_exception, handle_email_format_exception, handle_phone_format_exception, \
    handle_telegram_format_exception, handle_signature_expired_exception, handle_signature_invalid_exception, \
    handle_invalid_token_exception
from api.exceptions.universal.exceptions import InvalidRequest
from api.exceptions.universal.handlers.exception_handlers import handle_invalid_request_exception, \
    handle_value_exception, handle_validation_exception
from api.routes.cameras.cameras_routes import cameras_blueprint
from api.routes.clients.clients_routes import users_blueprint
from api.routes.invasions.invasions_routes import invasions_blueprint


def register_error_handlers(app: Flask):
    app.register_error_handler(marshmallow.exceptions.ValidationError, handle_validation_exception)
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
    app.register_error_handler(TokenIsInvalid, handle_invalid_token_exception)
    app.register_error_handler(ValueError, handle_value_exception)
    app.register_error_handler(CamerasNotFound, handle_cameras_exists_exception)


def register_blueprints(app: Flask):
    app.register_blueprint(users_blueprint)
    app.register_blueprint(cameras_blueprint)
    app.register_blueprint(invasions_blueprint)


@dataclass
class Config:
    host: str
    port: int

    @classmethod
    def load_from_file(cls, file_path):
        with open(file_path, 'r') as f:
            config = json.load(f, object_hook=lambda d: Config(**d))
        return config


if __name__ == '__main__':
    app = Flask(__name__, template_folder='templates', static_folder='static')
    config = Config.load_from_file("config.json")
    register_blueprints(app)
    register_error_handlers(app)
    app.run(host=config.host, port=config.port)
