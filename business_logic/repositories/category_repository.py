from typing import Optional

from business_logic.models import Category
from business_logic.repositories.repository import Repository


class CategoryRepository(Repository):

    def create_category(self, name: str) -> None:
        with self._session_scope() as session:
            new_category = Category(name=name)
            session.add(new_category)

    def get_category_by_name(self, name: str) -> Optional[dict]:
        with self._session_scope() as session:
            category: Category = session.query(Category).get(name)
            if not category:
                return None
            return {'name': category.name}

    def get_all_category_names(self) -> list[str]:
        category_names: list
        with self._session_scope() as session:
            categories = session.query(Category).all()
            category_names = [category.name for category in categories]
        return category_names
