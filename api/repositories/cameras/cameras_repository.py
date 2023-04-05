from typing import List

from api.exceptions.cameras.exceptions import CamerasNotFound
from api.models.cameras.cameras_models import Cameras
from api.repositories.cameras.interfaces.icameras_repository import CamerasRepositoryInterface
from api.repositories.db.mysql_db_context import AppDBConf


class CamerasRepository(CamerasRepositoryInterface):

    def __init__(self, db_context=AppDBConf.DB_SESSION):
        self.db_context = db_context

    def add_cam(self, client_id: int, cam_name: str) -> Cameras:
        new_cam = Cameras(
            client_id=client_id,
            device_name=cam_name,
            is_deleted=False
        )
        self.db_context.add(new_cam)
        self.db_context.commit()
        self.db_context.refresh(new_cam)
        return new_cam

    def get_cams_by_client_id(self, client_id: int) -> List[Cameras]:
        cameras = self.db_context.query(Cameras).filter(Cameras.client_id == client_id and Cameras.is_deleted is False).ToList()
        return cameras

    def is_cam_in_db(self, client_id: int, cam_name: str) -> bool:
        cam = self.db_context.query(Cameras)\
            .filter(Cameras.client_id == client_id and Cameras.device_name == cam_name and Cameras.is_deleted is False).first()
        if cam is None:
            return False
        return True

    def is_deleted(self, cam_id: int) -> bool:
        cam = self.db_context.query(Cameras) \
            .filter(Cameras.id == cam_id).first()
        return cam.is_deleted

    def delete(self, client_id: int, cam_ids: List[int]) -> None:
        self.db_context.query(Cameras).filter(Cameras.client_id == client_id).update(
            {
                Cameras.is_deleted: True
            }
        )
        self.db_context.commit()

    def get_by_id(self, cam_id: int) -> Cameras:
        cam = self.db_context.query(Cameras).filter(Cameras.id == cam_id and Cameras.is_deleted is False).first()
        if cam is None:
            raise CamerasNotFound()
        return cam
