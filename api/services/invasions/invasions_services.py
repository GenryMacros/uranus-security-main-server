import base64
import enum
import os
import time

from flask import url_for

from api.exceptions.clients.exceptions import InvalidTokens, TokenIsExpired
from api.repositories.cameras.interfaces.icameras_repository import CamerasRepositoryInterface
from api.repositories.clients.clients_repository import ClientRepositoryInterface
from api.repositories.invasions.interfaces.iinvasions_repository import InvasionsRepositoryInterface
from api.schemas.invasions.invasions_input import InvasionAdd, InvasionGet, InvasionDelete
from api.schemas.invasions.invasions_output import InvasionSchema, GetInvasionsOutput
from api.utils.jwt.jwt_handler import JwtHandler
from api.utils.secrets.secrets_handler import SecretsHandler


class ConfirmationMethod(enum.Enum):
    LINK = 0,
    SHORT_CODE = 1


class InvasionsService:

    def __init__(self, clients_repository: ClientRepositoryInterface,
                 cameras_repository: CamerasRepositoryInterface,
                 invasions_repository: InvasionsRepositoryInterface):
        self.cameras_repository = cameras_repository
        self.clients_repository = clients_repository
        self.invasions_repository = invasions_repository
        self.confirmation_method = ConfirmationMethod.SHORT_CODE

    def add_invasion(self, invasion: InvasionAdd) -> InvasionSchema:
        self.check_jwt_token(invasion.auth_token, invasion.client_id)
        added = self.invasions_repository.add_invasion(invasion)
        return InvasionSchema(
            id=added.id,
            success=True
        )

    def get_invasions(self, data: InvasionGet) -> GetInvasionsOutput:
        self.check_jwt_token(data.auth_token, data.client_id)
        invasions = self.invasions_repository.get_invasions_after_date(data.date, data.cam_id)
        cam_local_name = self.cameras_repository.get_by_id(data.cam_id).device_name
        response = GetInvasionsOutput()
        response_editable = {"invasions": [], "success": False}
        timestamp = int(time.time())
        download_token = self.__gen_download_token(data.client_id, timestamp).decode('utf-8')

        for inv in invasions:
            invasion_name = inv.video_path.split("\\")[-2]
            local_video_name = inv.video_path.split("\\")[-1]
            response_editable["invasions"].append(dict(
                id=inv.id,
                date=inv.created,
                file_name=f"{invasion_name}.mp4",
                link="http://10.0.2.2:8010" + url_for('static', filename=f"invasions/{str(cam_local_name)}/{invasion_name}/{local_video_name}"),
                link_short=f"http://localhost:8010/clients/cameras/invasions/download?"
                           f"path={inv.video_path}&"
                           f"is_short=1&"
                           f"user_id={data.client_id}&"
                           f"timestamp={timestamp}&"
                           f"token={download_token}"
            ))
        response_editable['success'] = True
        return GetInvasionsOutput.dump(response, response_editable)

    def __gen_download_token(self, client_id: int, timestamp: int):
        public, private = self.clients_repository.get_client_keys(client_id)
        token = SecretsHandler.sign_message(str(timestamp).encode('utf-8'), private)
        return token

    def check_download_token(self, token: str, client_id: int, timestamp: str) -> bool:
        public, private = self.clients_repository.get_client_keys(client_id)
        signature = base64.b64decode(token.encode('utf-8'))
        return SecretsHandler.is_signature_valid(
            public_key=public,
            signature=signature,
            message=timestamp.encode('utf-8')
        )

    def delete_invasion(self, data: InvasionDelete):
        self.check_jwt_token(data.auth_token, data.client_id)
        self.invasions_repository.delete_invasion(data.invasion_id)

    def check_jwt_token(self, token: str, client_id: int) -> None:
        public = self.clients_repository.get_client_public_key(client_id)
        is_token_signature_valid = JwtHandler.is_token_valid(token, public)
        if not is_token_signature_valid:
            raise InvalidTokens()
        token_body_info = JwtHandler.retrieve_body_info_from_token_jwt(token)
        if token_body_info.expiration_date <= time.time():
            raise TokenIsExpired()
