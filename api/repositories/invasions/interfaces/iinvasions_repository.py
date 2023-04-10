from typing import List


from api.models.invasions.invasions_models import Invasion
from api.schemas.invasions.invasions_input import InvasionAdd


class InvasionsRepositoryInterface:
    def add_invasion(self, invasion: InvasionAdd) -> Invasion:
        pass

    def get_invasions_after_date(self, date: str, camera_id: int) -> List[Invasion]:
        return []

    def delete_invasion(self, invasion_id: int) -> None:
        return
