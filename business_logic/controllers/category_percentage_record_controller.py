from datetime import date
from typing import Dict, List

from business_logic.controllers.category_controller import CategoryController
from business_logic.controllers.controller import Controller
from business_logic.repositories.category_percentage_record_repository import CategoryPercentageRecordRepository


class CategoryPercentageRecordController(Controller):
    __COMPARISON_TOLERANCE_LEVEL = 1e-6

    def __init__(self):
        super().__init__()
        self.__category_percentage_record_repository = CategoryPercentageRecordRepository()

    def change_category_percentages(self, category_percentages: dict[str, float], record_date: date) -> None:
        if not self.__validate_category_percentage_data(category_percentages):
            return
        if not self.__verify_percentages_total(list(category_percentages.values())):
            return
        category_percentage_records_data = self.__format_category_percentage_data(category_percentages, record_date)
        self.__category_percentage_record_repository.create_category_percentage_records(
            category_percentage_records_data
        )

    def get_category_percentages_at_date(self, target_date: date) -> Dict[str, float]:
        category_percentage_records_at_date = \
            self.__category_percentage_record_repository.get_records_with_closest_date_before(target_date)
        category_percentages_at_date = {}
        for category_percentage_record in category_percentage_records_at_date:
            category_percentages_at_date[
                category_percentage_record['category_name']] = category_percentage_record['percentage']
        return category_percentages_at_date

    def __validate_category_percentage_data(self, category_percentages: dict[str, float]) -> bool:
        category_controller: CategoryController = self._controller_manager.get_controller('CategoryController')
        category_names = category_controller.get_all_category_names()
        category_names.remove('General')
        return set(category_percentages.keys()) == set(category_names)

    def __verify_percentages_total(self, percentages: list[float]) -> bool:
        total = sum(percentages)
        return abs(total - 1) < self.__COMPARISON_TOLERANCE_LEVEL

    @staticmethod
    def __format_category_percentage_data(
        category_percentages: dict[str, float],
        record_date: date
        ) -> List[dict]:
        formatted_data = []
        for category_name, percentage in category_percentages.items():
            category_percentage_record = {
                'percentage': percentage, 'record_date': record_date,
                'category_name': category_name
            }
            formatted_data.append(category_percentage_record)
        return formatted_data
