import importlib
import inspect
import pkgutil
from typing import List, Dict, Type

from business_logic.controllers.controller import Controller
from business_logic.repositories.transaction_type_strategy_repository import TransactionTypeStrategyRepository
from business_logic.strategies.balance_strategy import BalanceStrategy


class TransactionTypeStrategyController(Controller):
    __PACKAGE_NAME = 'business_logic.strategies'

    def __init__(self):
        super().__init__()
        self.__transaction_type_strategy_repository = TransactionTypeStrategyRepository()
        self.__strategy_classes: Dict[str, Type[BalanceStrategy]] = self.__get_strategy_classes_dict()

    def create_strategy(self, strategy_name: str) -> None:
        if self.exists_strategy(strategy_name) or strategy_name is None:
            return
        self.__transaction_type_strategy_repository.create_strategy(strategy_name)

    def execute_balance_strategy(self, strategy_name: str, balance: float, amount: float) -> float:
        strategy_type = self.__strategy_classes[strategy_name]
        strategy_class = strategy_type()
        return strategy_class.process_balance(balance, amount)

    def exists_strategy(self, strategy_name: str) -> bool:
        transaction_type_strategy = self.__transaction_type_strategy_repository.get_strategy_by_name(strategy_name)
        if transaction_type_strategy is None:
            return False
        return True

    def __get_strategy_classes_dict(self) -> Dict[str, Type[BalanceStrategy]]:
        strategy_classes_dict = {}
        package = importlib.import_module(self.__PACKAGE_NAME)
        for _, module_name, _ in pkgutil.iter_modules(package.__path__):
            full_module_name = f'{self.__PACKAGE_NAME}.{module_name}'
            strategy_classes = self.__get_strategy_classes(full_module_name)
            for strategy_class in strategy_classes:
                strategy_classes_dict[strategy_class.__name__] = strategy_class
        return strategy_classes_dict

    @staticmethod
    def __get_strategy_classes(full_module_name: str) -> List[Type[BalanceStrategy]]:
        strategy_classes = []
        module = importlib.import_module(full_module_name)
        for name, obj in inspect.getmembers(module, inspect.isclass):
            if issubclass(obj, BalanceStrategy) and obj is not BalanceStrategy:
                strategy_classes.append(obj)
        return strategy_classes
