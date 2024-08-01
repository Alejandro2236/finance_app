from typing import Optional

from business_logic.controllers.controller import Controller
from business_logic.controllers.transaction_type_strategy_controller import TransactionTypeStrategyController
from business_logic.exceptions.object_not_found import ObjectNotFound
from business_logic.repositories.transaction_type_repository import TransactionTypeRepository


class TransactionTypeController(Controller):
    def __init__(self):
        super().__init__()
        self.__transaction_type_repository = TransactionTypeRepository()

    def create_transaction_type(self, transaction_type_name: str, requires_destination_pocket: bool) -> None:
        if self.transaction_type_exists(transaction_type_name) or transaction_type_name is None:
            return
        transaction_type_strategy_controller: TransactionTypeStrategyController = \
            self._controller_manager.get_controller('TransactionTypeStrategyController')
        strategy_name = transaction_type_name + 'BalanceStrategy'
        transaction_type_strategy_controller.create_strategy(strategy_name)
        self.__transaction_type_repository.create_transaction_type(
            transaction_type_name,
            requires_destination_pocket, strategy_name
        )
        transaction_type_strategy_controller.create_strategy(strategy_name)

    def process_amount_to_balance(self, transaction_type_name: str, balance: float, amount: float) -> float:
        transaction_type_strategy_controller: TransactionTypeStrategyController
        transaction_type_strategy_controller = self._controller_manager.get_controller(
            'TransactionTypeStrategyController'
        )
        transaction_type = self.__get_transaction_type(transaction_type_name)
        return transaction_type_strategy_controller.execute_balance_strategy(
            transaction_type['strategy_name'],
            balance,
            amount
        )

    def __get_transaction_type(self, transaction_type_name) -> Optional[dict]:
        return self.__transaction_type_repository.get_transaction_type_by_name(transaction_type_name)

    def transaction_type_exists(self, transaction_type_name: str) -> bool:
        transaction_type = self.__transaction_type_repository.get_transaction_type_by_name(transaction_type_name)
        if transaction_type is None:
            return False
        return True

    def requires_destination_pocket(self, transaction_type_name: str) -> bool:
        if self.transaction_type_exists(transaction_type_name):
            raise ObjectNotFound
        transaction_type = self.__transaction_type_repository.get_transaction_type_by_name(transaction_type_name)
        return transaction_type['requires_destination_pocket']
