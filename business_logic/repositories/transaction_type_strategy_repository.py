from typing import Optional

from business_logic.models.transaction_type_strategy import TransactionTypeStrategy
from business_logic.repositories.repository import Repository


class TransactionTypeStrategyRepository(Repository):

    def create_strategy(self, strategy_name: str) -> None:
        with self._session_scope() as session:
            new_transaction_type_strategy = TransactionTypeStrategy(name=strategy_name)
            session.add(new_transaction_type_strategy)

    def get_strategy_by_name(self, name: str) -> Optional[TransactionTypeStrategy]:
        with self._session_scope() as session:
            transaction_type_strategy = session.query(TransactionTypeStrategy).get(name)
        return transaction_type_strategy
