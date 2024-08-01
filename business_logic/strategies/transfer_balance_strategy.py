from business_logic.strategies.balance_strategy import BalanceStrategy


class TransferBalanceStrategy(BalanceStrategy):
    def process_balance(self, incoming_balance: float, transaction_amount: float) -> float:
        return incoming_balance - transaction_amount
