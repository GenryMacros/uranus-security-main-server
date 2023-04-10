import json
import logging
import sys
from dataclasses import dataclass
from typing import Set

import requests
import urllib.request as urllib2
import urllib.error as urllib2_err
from socket_server.schemas.cameras import Cameras, DefaultResponse
from socket_server.schemas.user import UserAuthData


IS_LOG = True
logger = logging.getLogger(__name__)

if IS_LOG:
    logger.setLevel(logging.INFO)
    logger.addHandler(logging.StreamHandler(stream=sys.stdout))
    # do not print twice in sys.stdout
    logger.propagate = False


@dataclass
class Config:
    host: str
    port: int

    @classmethod
    def load_from_file(cls, file_path):
        with open(file_path, 'r') as f:
            config = json.load(f, object_hook=lambda d: Config(**d))
        return config


class Requester:

    def __init__(self, config_path="configs/requester_config.json"):
        config = Config.load_from_file(config_path)
        self.host = config.host
        self.port = config.port
        self.full_api_url = f"http://{self.host}:{self.port}"
        #self.is_server_available()

    def is_server_available(self) -> bool:
        try:
            urllib2.urlopen(self.full_api_url, timeout=1)
            return True
        except urllib2_err.URLError as err:
            logger.info("[REQUESTER] No connection to main server")
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

    def register_cameras(self, auth_data: UserAuthData, cams: Set[int]) -> DefaultResponse:
        if self.is_server_available():
            response = requests.post(f"{self.full_api_url}/clients/cameras/add", json={
                "id": auth_data.userId,
                "auth_token": auth_data.token,
                "cameras": [{"cam_id": str(cam)} for cam in cams]
            })
            response_data: DefaultResponse = DefaultResponse.load(response.json())
        else:
            response_data: DefaultResponse = DefaultResponse(success=False,
                                                             reason="Can't connect to main server.")
        return response_data
