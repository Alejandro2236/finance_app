from abc import ABC, abstractmethod


class BalanceStrategy(ABC):
    @abstractmethod
    def process_balance(self, incoming_balance: float, transaction_amount: float) -> float:
        pass
