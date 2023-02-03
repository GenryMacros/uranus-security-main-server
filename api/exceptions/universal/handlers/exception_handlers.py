
from api.exceptions.universal.exceptions import InvalidRequest


def handle_invalid_request_exception(e: InvalidRequest):
    return {"success": False, "reason": e.message}, 403
