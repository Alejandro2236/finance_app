from business_logic.controllers.controller import Controller
from business_logic.repositories.category_repository import CategoryRepository


class CategoryController(Controller):
    def __init__(self):
        super().__init__()
        self.__category_repository = CategoryRepository()

    def create_category(self, category_name: str) -> None:
        if self.category_exists(category_name) or category_name is None:
            return
        self.__category_repository.create_category(category_name)

    def category_exists(self, category_name: str) -> bool:
        category = self.__category_repository.get_category_by_name(category_name)
        if category is None:
            return False
        return True

    def get_all_category_names(self) -> list[str]:
        return self.__category_repository.get_all_category_names()
