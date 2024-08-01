import calendar
from datetime import date

from dateutil.relativedelta import relativedelta

from business_logic.controllers.controller import Controller
from business_logic.controllers.transaction_controller import TransactionController
from business_logic.repositories.pocket_category_balance_record_repository import PocketCategoryBalanceRecordRepository


class PocketCategoryBalanceRecordController(Controller):
    def __init__(self):
        super().__init__()
        self.__pocket_category_balance_record_repository = PocketCategoryBalanceRecordRepository()

    def update_last_12_months(self) -> None:
        initial_date = date.today() - relativedelta(months=12)
        self.__update_since_date(initial_date)

    def update_missing_month_records(self) -> None:
        last_record_date = self.__pocket_category_balance_record_repository.get_latest_record_date()
        if last_record_date is not None:
            initial_date = last_record_date + relativedelta(months=1)
            self.__update_since_date(initial_date)
            return
        transaction_controller: TransactionController = self._controller_manager.get_controller('TransactionController')
        oldest_transaction_date = transaction_controller.get_oldest_transaction_date()
        if oldest_transaction_date is not None:
            self.__update_since_date(oldest_transaction_date)
            return
        initial_date = date.today() - relativedelta(months=1)
        self.__update_since_date(initial_date)

    def __update_since_date(self, initial_date: date) -> None:
        current_date = date.today()
        current_year, current_month = current_date.year, current_date.month
        auxiliary_date = initial_date
        while auxiliary_date.year != current_year or auxiliary_date.month != current_month:
            self.__update_pocket_category_balance_records_at_month(auxiliary_date)
            auxiliary_date = auxiliary_date + relativedelta(months=1)

    def __update_pocket_category_balance_records_at_month(self, target_date: date) -> None:
        transaction_controller: TransactionController = self._controller_manager.get_controller('TransactionController')
        balances_list = transaction_controller.get_total_balance_at_month(target_date)
        if balances_list is None:
            return
        _, last_month_day = calendar.monthrange(target_date.year, target_date.month)
        date_at_last_month_day = date(target_date.year, target_date.month, last_month_day)
        for balances in balances_list:
            if self.__record_exists(target_date, balances['pocket'], balances['category']):
                self.__pocket_category_balance_record_repository.update_record(
                    record_date=date_at_last_month_day,
                    actual_pocket_name=balances['pocket'],
                    actual_category_name=balances['category'],
                    balance=balances['total_amount']
                )
                continue
            self.__pocket_category_balance_record_repository.create_record(
                balances['total_amount'],
                date_at_last_month_day,
                balances['pocket'],
                balances['category']
            )

    def get_all_records(self) -> list[dict]:
        return self.__pocket_category_balance_record_repository.get_all_records()

    def __record_exists(self, target_date: date, pocket_name: str, category_name: str) -> bool:
        record_at_month = self.__pocket_category_balance_record_repository.get_record_at_month(
            target_date,
            pocket_name,
            category_name
        )
        if record_at_month is None:
            return False
        return True

    def delete_all_records(self):
        self.__pocket_category_balance_record_repository.delete_all_records()
