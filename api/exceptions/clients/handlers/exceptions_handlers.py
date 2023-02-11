from itsdangerous import SignatureExpired

from api.exceptions.clients.exceptions import TokenIsExpired, ClientExists, ClientNotFound, SignupFailed, \
    InvalidCredentials, InvalidTokens, FirstNameWrongFormat, \
    LastNameWrongFormat, EmailWrongFormat, PhoneWrongFormat, TelegramWrongFormat, TokenIsInvalid


def handle_client_exists_exception(e: ClientExists):
    return {"success": False, "reason": e.message}, 404


def handle_client_not_found_exception(e: ClientNotFound):
    return {"success": False, "reason": e.message}, 400


def handle_signup_failure_exception(e: SignupFailed):
    return {"success": False, "reason": e.message}, 400


def handle_invalid_credentials_exception(e: InvalidCredentials):
    return {"success": False, "reason": e.message}, 404


def handle_invalid_tokens_exception(e: InvalidTokens):
    return {"success": False, "reason": e.message}, 400


def handle_token_expired_exception(e: TokenIsExpired):
    return {"success": False, "reason": e.message}, 400


def handle_first_name_format_exception(e: FirstNameWrongFormat):
    return {"success": False, "reason": e.message}, 400


def handle_last_name_format_exception(e: LastNameWrongFormat):
    return {"success": False, "reason": e.message}, 400


def handle_email_format_exception(e: EmailWrongFormat):
    return {"success": False, "reason": e.message}, 400


def handle_phone_format_exception(e: PhoneWrongFormat):
    return {"success": False, "reason": e.message}, 400


def handle_telegram_format_exception(e: TelegramWrongFormat):
    return {"success": False, "reason": e.message}, 400


def handle_signature_expired_exception(e: SignatureExpired):
    return {"success": False, "reason": "Signup token is expired"}, 400


def handle_invalid_token_exception(e: TokenIsInvalid):
    return {"success": False, "reason": e.message}, 400
