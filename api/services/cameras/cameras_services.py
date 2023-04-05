import base64
import enum
import time

from api.exceptions.clients.exceptions import InvalidTokens, TokenIsExpired
from api.repositories.cameras.interfaces.icameras_repository import CamerasRepositoryInterface
from api.repositories.clients.clients_repository import ClientRepositoryInterface
from api.schemas.cameras.cameras_input import CamsRegister, CamsGet, CamsDelete
from api.schemas.cameras.cameras_output import Cameras
from api.utils.jwt.jwt_handler import JwtHandler


class ConfirmationMethod(enum.Enum):
    LINK = 0,
    SHORT_CODE = 1


class CamerasService:

    def __init__(self, clients_repository: ClientRepositoryInterface,
                 cameras_repository: CamerasRepositoryInterface):
        self.cameras_repository = cameras_repository
        self.clients_repository = clients_repository
        self.confirmation_method = ConfirmationMethod.SHORT_CODE

    def register(self, data: CamsRegister) -> None:
        self.check_jwt_token(data["auth_token"], data["id"])
        for cam in data["cameras"]:
            if not self.cameras_repository.is_cam_in_db(data["id"], str(cam["cam_id"])):
                self.cameras_repository.add_cam(data["id"], str(cam["cam_id"]))

    def get_cams(self, data: CamsGet) -> Cameras:
        self.check_jwt_token(data.auth_token, data.id)
        cams = self.cameras_repository.get_cams_by_client_id(data.id)
        output = Cameras([], [])
        for cam in cams:
            output.cam_ids.append(cam.id)
            output.cam_names.append(cam.device_name)
        return output

    def delete_cams(self, data: CamsDelete):
        self.check_jwt_token(data.auth_token, data.id)
        self.cameras_repository.delete(data.id, data.cam_names)

    def check_jwt_token(self, token: str, client_id: int) -> None:
        public = self.clients_repository.get_client_public_key(client_id)
        is_token_signature_valid = JwtHandler.is_token_valid(token, public)
        if not is_token_signature_valid:
            raise InvalidTokens()
        token_body_info = JwtHandler.retrieve_body_info_from_token_jwt(token)
        if token_body_info.expiration_date <= time.time():
            raise TokenIsExpired()
