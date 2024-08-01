from typing import Optional

from business_logic.models import TransactionType
from business_logic.repositories.repository import Repository


class TransactionTypeRepository(Repository):

    def create_transaction_type(self, name: str, requires_destination_pocket: bool, strategy_name: str) -> None:
        with self._session_scope() as session:
            new_transaction_type = TransactionType(
                name=name,
                requires_destination_pocket=requires_destination_pocket,
                strategy_name=strategy_name
            )
            session.add(new_transaction_type)

    def get_transaction_type_by_name(self, name: str) -> Optional[dict]:
        with self._session_scope() as session:
            transaction_type: TransactionType = session.query(TransactionType).get(name)
            if not transaction_type:
                return None
            return {
                'name': transaction_type.name,
                'requires_destination_pocket': transaction_type.requires_destination_pocket,
                'strategy_name': transaction_type.strategy_name
            }
