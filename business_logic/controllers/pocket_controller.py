from typing import List

from business_logic.controllers.controller import Controller
from business_logic.repositories.pocket_repository import PocketRepository


class PocketController(Controller):
    def __init__(self):
        super().__init__()
        self.__pocket_repository = PocketRepository()

    def create_pocket(self, pocket_name: str) -> None:
        if self.pocket_exists(pocket_name) or pocket_name is None:
            return
        self.__pocket_repository.create_pocket(pocket_name)

    def pocket_exists(self, pocket_name: str) -> bool:
        pocket = self.__pocket_repository.get_pocket_by_name(pocket_name)
        if pocket is None:
            return False
        return True

    def get_all_pocket_names(self) -> List[str]:
        return self.__pocket_repository.get_all_pocket_names()
