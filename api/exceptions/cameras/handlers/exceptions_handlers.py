from api.exceptions.cameras.exceptions import CamerasNotFound


def handle_cameras_exists_exception(e: CamerasNotFound):
    return {"success": False, "reason": e.message}, 404
