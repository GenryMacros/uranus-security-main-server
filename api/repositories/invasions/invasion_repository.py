from time import time
from typing import List


from api.models.invasions.invasions_models import Invasion, Intruder, InvasionIntruders
from api.repositories.db.mysql_db_context import AppDBConf
from api.repositories.invasions.interfaces.iinvasions_repository import InvasionsRepositoryInterface
from api.schemas.invasions.invasions_input import InvasionAdd


class InvasionRepository(InvasionsRepositoryInterface):

    def __init__(self, db_context=AppDBConf.DB_SESSION):
        self.db_context = db_context

    def add_invasion(self, invasion: InvasionAdd) -> Invasion:
        new_invasion = Invasion(
            camera_id=invasion.cam_id,
            video_path=invasion.path,
            created=str(int(time())),
            is_deleted=False
        )
        self.db_context.add(new_invasion)
        self.db_context.commit()
        self.db_context.refresh(new_invasion)
        for invader in invasion.invaders:
            invader = self.db_context.query(Intruder).filter(Intruder.name == invader).first()
            if invader:
                self.db_context.add(InvasionIntruders(
                    invasion_id=new_invasion.id,
                    intruder_id=invader.id
                ))
        self.db_context.commit()
        return new_invasion

    def get_invasions_after_date(self, date: str, camera_id: int) -> (List[Invasion], List[List[str]]):
        invasions = self.db_context.query(Invasion).filter(Invasion.camera_id == camera_id
                                                           and Invasion.is_deleted is False
                                                           and int(Invasion.created) > int(date))
        intruders_per_session: List[List[str]] = []
        if invasions:
            invasions = list(invasions)
            for invasion in invasions:
                invasions2intruders = list(self.db_context.query(InvasionIntruders)
                                           .filter(InvasionIntruders.invasion_id == invasion.id))
                invaders = []
                for invasion2intruder in invasions2intruders:
                    invader = self.db_context.query(Intruder).filter(Intruder.id == invasion2intruder.intruder_id).first()
                    invaders.append(invader.name)
                intruders_per_session.append(invaders)
        return invasions, intruders_per_session

    def delete_invasion(self, invasion_id: int) -> None:
        self.db_context.query(Invasion).filter(Invasion.id == invasion_id).update(
            {
                Invasion.is_deleted: True
            }
        )
        self.db_context.commit()
