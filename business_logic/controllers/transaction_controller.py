from datetime import date
from typing import Optional

from business_logic.controllers.category_percentage_record_controller import CategoryPercentageRecordController
from business_logic.controllers.controller import Controller
from business_logic.controllers.pocket_controller import PocketController
from business_logic.controllers.transaction_type_controller import TransactionTypeController
from business_logic.models import Transaction
from business_logic.repositories.transaction_repository import TransactionRepository


class TransactionController(Controller):
    def __init__(self):
        super().__init__()
        self.__transaction_repository = TransactionRepository()

    def create_transaction(
        self,
        transaction_date: date,
        amount: float,
        description: Optional[str],
        pocket_name: str,
        category_name: str,
        transaction_type_name: str,
        destination_pocket_name: Optional[str]
    ) -> None:
        if not self.__pocket_exists(pocket_name):
            raise ValueError(f"The pocket {pocket_name} doesn't exists")
        if not self.__category_exists(category_name):
            raise ValueError(f"The category {category_name} doesn't exists")
        if not self.__transaction_type_exists(transaction_type_name):
            raise ValueError(f"The transaction type {transaction_type_name} doesn't exists")
        if amount <= 0:
            raise ValueError('Transaction amount must be greater than zero')
        if transaction_type_name == 'Transfer':
            if not destination_pocket_name:
                raise ValueError('A transfer type transaction requires a destination pocket.')
            if not self.__pocket_exists(destination_pocket_name):
                raise ValueError(f"The destination pocket '{destination_pocket_name}' doesn't exist.")
        elif destination_pocket_name:
            raise ValueError('Only transfer transactions can have a destination pocket.')
        self.__transaction_repository.create_transaction(
            transaction_date,
            amount,
            description,
            pocket_name,
            category_name,
            transaction_type_name,
            destination_pocket_name
        )

    """
    def get_total_balance_at_month(self, target_date: date) -> list[dict]:
        transactions = self.__get_transactions_by_month(target_date)
        data_by_category_and_pocket = self.__initialize_dict_for_balance_data()
        for transaction in transactions:
            if transaction['category_name'] == 'General':
                distributed_general_transaction = self.__distribute_general_transaction(
                    transaction['amount'],
                    transaction['transaction_date']
                )
                for category, amount in distributed_general_transaction.items():
                    if self.__need_transfer(transaction):
                        key = (category, transaction['destination_pocket_name'])
                        data_by_category_and_pocket[key] += transaction['amount']
                    key = (category, transaction['pocket_name'])
                    data_by_category_and_pocket[key] = self.__process_amount_to_balance(
                        transaction['transaction_type_name'],
                        data_by_category_and_pocket[key],
                        amount
                    )
                continue
            if self.__need_transfer(transaction):
                key = (transaction['category_name'], transaction['destination_pocket_name'])
                data_by_category_and_pocket[key] += transaction['amount']
            key = (transaction['category_name'], transaction['pocket_name'])
            data_by_category_and_pocket[key] = self.__process_amount_to_balance(
                transaction['transaction_type_name'],
                data_by_category_and_pocket[key],
                transaction['amount']
            )
        return [{'category': key[0], 'pocket': key[1], 'total_amount': value} for key, value in
                data_by_category_and_pocket.items()
    """

    def get_total_balance_at_month(self, target_date: date) -> list[dict]:
        transactions = self.__get_transactions_by_month(target_date)
        data_by_category_and_pocket = self.__initialize_dict_for_balance_data()
        for transaction in transactions:
            if transaction['category_name'] == 'General':
                self.__process_general_transaction(transaction, data_by_category_and_pocket)
            else:
                self.__process_specific_transaction(transaction, data_by_category_and_pocket)
        return self.__format_balance_data(data_by_category_and_pocket)

    def __process_general_transaction(self, transaction: dict, data_by_category_and_pocket: dict) -> None:
        distributed_general_transaction = self.__distribute_general_transaction(
            transaction['amount'],
            transaction['transaction_date']
        )
        for category, amount in distributed_general_transaction.items():
            if self.__need_transfer(transaction):
                key = (category, transaction['destination_pocket_name'])
                data_by_category_and_pocket[key] += transaction['amount']
            key = (category, transaction['pocket_name'])
            data_by_category_and_pocket[key] = self.__process_amount_to_balance(
                transaction['transaction_type_name'],
                data_by_category_and_pocket[key],
                amount
            )

    def __process_specific_transaction(self, transaction: dict, data_by_category_and_pocket: dict) -> None:
        if self.__need_transfer(transaction):
            key = (transaction['category_name'], transaction['destination_pocket_name'])
            data_by_category_and_pocket[key] += transaction['amount']
        key = (transaction['category_name'], transaction['pocket_name'])
        data_by_category_and_pocket[key] = self.__process_amount_to_balance(
            transaction['transaction_type_name'],
            data_by_category_and_pocket[key],
            transaction['amount']
        )

    def __update_transfer_balance(self):
        raise NotImplementedError

    def __update_balance(self, data: dict, category: str, pocket: str, transaction: dict, amount: Optional[float] = None) -> None:
        key = (category, pocket)
        transaction_amount = amount if amount is not None else transaction['amount']
        data[key] = self.__process_amount_to_balance(
            transaction['transaction_type_name'],
            data[key],
            transaction_amount
        )

    @staticmethod
    def __format_balance_data(data_by_category_and_pocket: dict) -> list[dict]:
        return [{'category': key[0], 'pocket': key[1], 'total_amount': value} for key, value in
                data_by_category_and_pocket.items()]

    @staticmethod
    def __need_transfer(transaction: dict) -> bool:
        return transaction['destination_pocket_name'] is not None and transaction['transaction_type_name'] == 'Transfer'

    def __distribute_general_transaction(self, amount: float, transaction_date: date) -> dict[str, float]:
        category_percentage_record_controller: CategoryPercentageRecordController
        category_percentage_record_controller = self._controller_manager.get_controller(
            'CategoryPercentageRecordController'
        )
        category_percentages_at_date = category_percentage_record_controller.get_category_percentages_at_date(
            transaction_date
        )
        distributed_amount_by_category = {}
        for category, percentage in category_percentages_at_date.items():
            distributed_amount_by_category[category] = amount * percentage
        return distributed_amount_by_category

    def __process_amount_to_balance(self, transaction_type_name: str, balance: float, amount: float) -> float:
        transaction_type_controller: TransactionTypeController
        transaction_type_controller = self._controller_manager.get_controller('TransactionTypeController')
        return transaction_type_controller.process_amount_to_balance(transaction_type_name, balance, amount)

    def __initialize_dict_for_balance_data(self) -> dict[(str, str), float]:
        data_dict = {}
        categories = self.__get_all_category_names()
        pockets = self.__get_all_pocket_names()
        for category in categories:
            for pocket in pockets:
                if category == 'General':
                    continue
                data_dict[(category, pocket)] = 0.0
        return data_dict

    def __get_all_category_names(self) -> list[str]:
        category_controller = self._controller_manager.get_controller('CategoryController')
        return category_controller.get_all_category_names()

    def __get_all_pocket_names(self) -> list[str]:
        pocket_controller: PocketController = self._controller_manager.get_controller('PocketController')
        return pocket_controller.get_all_pocket_names()

    def __get_transactions_by_month(self, target_date: date) -> list[dict]:
        return self.__transaction_repository.get_transactions_by_month(target_date)

    def __pocket_exists(self, pocket_name: str) -> bool:
        pocket_controller = self._controller_manager.get_controller('PocketController')
        if pocket_controller.pocket_exists(pocket_name):
            return True
        return False

    def __category_exists(self, category_name: str) -> bool:
        category_controller = self._controller_manager.get_controller('CategoryController')
        if category_controller.category_exists(category_name):
            return True
        return False

    def __transaction_type_exists(self, transaction_type_name: str) -> bool:
        transaction_type_controller = self._controller_manager.get_controller('TransactionTypeController')
        if transaction_type_controller.transaction_type_exists(transaction_type_name):
            return True
        return False

    def get_transactions_by_oldest_month_year(self) -> list[Transaction]:
        return self.__transaction_repository.get_transactions_by_oldest_month_year()

    def get_oldest_transaction_date(self) -> Optional[date]:
        return self.__transaction_repository.get_oldest_transaction_date()

    def delete_transaction_by_id(self, transaction_id: int) -> None:
        self.__transaction_repository.delete_transaction_by_id(transaction_id)
