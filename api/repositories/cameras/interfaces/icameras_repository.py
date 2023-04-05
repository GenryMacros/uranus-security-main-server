from typing import List

from api.models.cameras.cameras_models import Cameras


class CamerasRepositoryInterface:

    def add_cam(self, client_id: int, cam_name: str) -> Cameras:
        return Cameras()

    def get_cams_by_client_id(self, client_id: int) -> List[Cameras]:
        return Cameras()

    def is_cam_in_db(self, client_id: int, cam_name: str) -> bool:
        return False

    def is_deleted(self, cam_id: int) -> bool:
        return False

    def delete(self, client_id: int, cam_ids: List[int]) -> None:
        return

    def get_by_id(self, cam_id: int) -> Cameras:
        return Cameras()
