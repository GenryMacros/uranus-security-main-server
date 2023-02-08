
from api.exceptions.clients.exceptions import TokenIsExpired, ClientExists, ClientNotFound, SignupFailed, \
    InvalidCredentials, InvalidTokens, UsernameWrongFormat, PasswordWrongFormat


def handle_client_exists_exception(e: ClientExists):
    return {"success": False, "reason": e.message}, 404


def handle_client_not_found_exception(e: ClientNotFound):
    return {"success": False, "reason": e.message}, 400


def handle_signup_failure_exception(e: SignupFailed):
    return {"success": False, "reason": e.message}, 400


def handle_invalid_username_format_exception(e: UsernameWrongFormat):
    return {"success": False, "reason": e.message}, 404


def handle_invalid_password_format_exception(e: PasswordWrongFormat):
    return {"success": False, "reason": e.message}, 404


def handle_invalid_credentials_exception(e: InvalidCredentials):
    return {"success": False, "reason": e.message}, 404


def handle_invalid_tokens_exception(e: InvalidTokens):
    return {"success": False, "reason": e.message}, 400


def handle_token_expired_exception(e: TokenIsExpired):
    return {"success": False, "reason": e.message}, 400
