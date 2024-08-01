from typing import Optional

from business_logic.models.pocket import Pocket
from business_logic.repositories.repository import Repository


class PocketRepository(Repository):

    def create_pocket(self, name: str) -> None:
        with self._session_scope() as session:
            new_pocket = Pocket(name=name)
            session.add(new_pocket)

    def get_pocket_by_name(self, name) -> Optional[Pocket]:
        with self._session_scope() as session:
            pocket = session.query(Pocket).get(name)
        return pocket

    def get_all_pocket_names(self) -> list[str]:
        pocket_names: list
        with self._session_scope() as session:
            pockets = session.query(Pocket).all()
            pocket_names = [pocket.name for pocket in pockets]
        return pocket_names
