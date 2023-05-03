import json
import logging
import sys
from dataclasses import dataclass
from typing import Set

import requests
import urllib.request as urllib2
import urllib.error as urllib2_err

from socket_server.events import EventTypeOut
from socket_server.schemas.cameras import Cameras, DefaultResponse
from socket_server.schemas.user import UserAuthData


IS_LOG = True
logger = logging.getLogger(__name__)

if IS_LOG:
    logger.setLevel(logging.INFO)
    logger.addHandler(logging.StreamHandler(stream=sys.stdout))
    logger.propagate = False


@dataclass
class Config:
    host: str
    port: int
    default_client_login: str
    default_client_password: str

    @classmethod
    def load_from_file(cls, file_path):
        with open(file_path, 'r') as f:
            config = json.load(f, object_hook=lambda d: Config(**d))
        return config


class Requester:

    def __init__(self, auth_data: UserAuthData,
                 config_path="configs/requester_config.json"):
        config = Config.load_from_file(config_path)
        self.host = config.host
        self.port = config.port
        self.full_api_url = f"http://{self.host}:{self.port}"
        self.auth_data = auth_data
        self.default_user_login = config.default_client_login
        self.default_user_password = config.default_client_password
        self.login()

    def login(self):
        if self.is_server_available():
            response = requests.post(f"{self.full_api_url}/clients/login", json={
                "username": self.default_user_login,
                "password": self.default_user_password
            })
            if response.status_code >= 400:
                logger.info("[REQUESTER] Login failed, data will be written local only")
            else:
                response_json = response.json()
                self.auth_data.publicKey = response_json['public_key']
                self.auth_data.refreshToken = response_json['refresh_token']
                self.auth_data.token = response_json['auth_token']
                self.auth_data.userId = response_json['id']
        else:
            logger.info("[REQUESTER] Server api is unavailable")

    def is_server_available(self) -> bool:
        try:
            urllib2.urlopen(self.full_api_url, timeout=1)
            return True
        except urllib2_err.URLError as err:
            logger.info("[REQUESTER] Server api is unavailable")
            return False

    def get_cameras(self, auth_data: UserAuthData) -> Cameras:
        if self.is_server_available():
            response = requests.post(f"{self.full_api_url}/clients/cameras", json={
                "id": auth_data.userId,
                "auth_token": auth_data.token
            })
            if response.status_code >= 400:
                cam_data: Cameras = Cameras([], [], False, '')
            else:
                cam_data: Cameras = Cameras.load(response.json())
        else:
            cam_data: Cameras = Cameras([], [], False, '')
        return cam_data

    def register_cameras(self, cams: Set[int]) -> DefaultResponse:
        if self.is_server_available():
            response = requests.post(f"{self.full_api_url}/clients/cameras/add", json={
                "id": self.auth_data.userId,
                "auth_token": self.auth_data.token,
                "cameras": [{"cam_id": str(cam)} for cam in cams]
            })
            response_data: DefaultResponse = DefaultResponse.load(response.json())
        else:
            response_data: DefaultResponse = DefaultResponse(success=False,
                                                             reason="Can't connect to main server.")
        return response_data

    def register_invasion(self, file_path: str, cam_id: int, detected: Set[str],
                          client, client_sid):
        if self.is_server_available():
            while True:
                response = requests.post(f"{self.full_api_url}/clients/cameras/invasions/add", json={
                    "client_id": self.auth_data.userId,
                    "auth_token": self.auth_data.token,
                    "cam_id": cam_id,
                    "path": file_path,
                    "invaders": list(detected)
                })
                if response.status_code >= 400:
                    if response.json()["reason"] == "Token is expired":
                        is_reauth_successful = self.reauth()
                        if is_reauth_successful:
                            client.emit(EventTypeOut.REAUTH_HAPPENED.value,
                                        data={
                                            "new_token": self.auth_data.token
                                        }, to=client_sid)
                    else:
                        logger.info("[REQUESTER] Failed to post new invasion on server")
                break
        else:
            logger.info("[REQUESTER] Server api is unavailable")

    def reauth(self) -> bool:
        is_successful = True
        if self.is_server_available():
            response = requests.post(f"{self.full_api_url}/clients/refresh", json={
                "user_id": self.auth_data.userId,
                "jwt": self.auth_data.token,
                "refresh": self.auth_data.refreshToken
            })
            if response.status_code >= 400:
                is_successful = False
                logger.info("[REQUESTER] Failed to post new invasion on server")
        else:
            logger.info("[REQUESTER] Server api is unavailable")
        return is_successful
