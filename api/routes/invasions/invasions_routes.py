from flask import Blueprint, send_file
from flask import request

from api.repositories.cameras.cameras_repository import CamerasRepository
from api.repositories.clients.clients_repository import ClientRepository
from api.repositories.invasions.invasion_repository import InvasionRepository

from api.schemas.default_response import DefaultResponse
from api.schemas.invasions.invasions_input import InvasionAdd, InvasionGet, InvasionDelete
from api.schemas.invasions.invasions_output import GetInvasionsOutput
from api.services.invasions.invasions_services import InvasionsService

invasions_blueprint = Blueprint("invasions_blueprint", __name__)
invasions_service = InvasionsService(ClientRepository(), CamerasRepository(),
                                     InvasionRepository())


@invasions_blueprint.route('/clients/cameras/invasions/add', methods=['POST'])
def add_invasion():
    body = request.get_json()
    request_data: InvasionAdd = InvasionAdd.load(body)
    added_invasion = invasions_service.add_invasion(request_data)
    return added_invasion.dump(), 200


@invasions_blueprint.route('/clients/cameras/invasions', methods=['POST'])
def get_invasions():
    body = request.get_json()
    request_data: InvasionGet = InvasionGet.load(body)
    invasions: GetInvasionsOutput = invasions_service.get_invasions(request_data)

    return invasions, 200


@invasions_blueprint.route('/clients/cameras/invasions', methods=['DELETE'])
def delete_invasions():
    request_data: InvasionDelete = InvasionDelete.load(request.get_json())
    invasions_service.delete_invasion(request_data)

    return DefaultResponse().dump(), 200


@invasions_blueprint.route('/clients/cameras/invasions/download', methods=['GET'])
def download_invasion():
    file_path = request.args.get("path", None)
    is_short = bool(request.args.get("is_short", None))
    client_id = int(request.args.get("user_id", None))
    timestamp = request.args.get("timestamp", None)
    token = request.args.get("token", None)

    if file_path is None or is_short is None or client_id is None or timestamp is None or token is None:
        return {"reason": "Invalid link", "success": False}, 400
    elif not invasions_service.check_download_token(token, client_id, timestamp):
        return {"reason": "Invalid token", "success": False}, 400

    if is_short:
        pass

    return send_file(file_path, as_attachment=True)
