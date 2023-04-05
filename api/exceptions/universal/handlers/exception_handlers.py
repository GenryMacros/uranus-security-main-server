import marshmallow

from api.exceptions.universal.exceptions import InvalidRequest


def handle_invalid_request_exception(e: InvalidRequest):
    return {"success": False, "reason": e.message}, 403


def handle_value_exception(e: ValueError):
    return {"success": False, "reason": e.__str__()}, 403


def handle_validation_exception(e: marshmallow.exceptions.ValidationError):
    return {"success": False, "reason": "Invalid request body"}, 400
