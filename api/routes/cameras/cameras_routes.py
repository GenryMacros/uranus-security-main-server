from flask import Blueprint
from flask import request

from api.repositories.cameras.cameras_repository import CamerasRepository
from api.repositories.clients.clients_repository import ClientRepository

from api.schemas.cameras.cameras_input import CamsRegister, CamsGet, CamsDelete
from api.schemas.cameras.cameras_output import Cameras
from api.schemas.default_response import DefaultResponse
from api.services.cameras.cameras_services import CamerasService


cameras_blueprint = Blueprint("cameras_blueprint", __name__)
cameras_service = CamerasService(ClientRepository(), CamerasRepository())


@cameras_blueprint.route('/clients/cameras/add', methods=['POST'])
def add():
    request_data: CamsRegister = CamsRegister().load(request.get_json())
    cameras_service.register(request_data)
    return DefaultResponse(success=True).dump(), 200


@cameras_blueprint.route('/clients/cameras', methods=['POST'])
def get_cameras():
    body = request.get_json()
    request_data: CamsGet = CamsGet.load(body)
    cams: Cameras = cameras_service.get_cams(request_data)

    return cams.dump(), 200


@cameras_blueprint.route('/clients/cameras', methods=['DELETE'])
def delete_cameras():
    request_data: CamsDelete = CamsDelete.load(request.get_json())
    cameras_service.delete_cams(request_data)

    return DefaultResponse().dump(), 200

