from datetime import date
from typing import Optional

from sqlalchemy import func, extract

from business_logic.exceptions.object_not_found import ObjectNotFound
from business_logic.models import Transaction
from business_logic.repositories.repository import Repository


class TransactionRepository(Repository):

    def create_transaction(
        self,
        transaction_date: date,
        amount: float,
        description: str,
        pocket_name: str,
        category_name: str,
        transaction_type_name: str,
        destination_pocket_name: Optional[str]
    ) -> None:
        with self._session_scope() as session:
            new_transaction = Transaction(
                transaction_date=transaction_date, amount=amount, description=description,
                pocket_name=pocket_name, category_name=category_name,
                transaction_type_name=transaction_type_name,
                destination_pocket_name=destination_pocket_name
            )
            session.add(new_transaction)

    def get_transactions_by_month(self, target_date: date) -> list[dict]:
        year, month = target_date.year, target_date.month
        with self._session_scope() as session:
            transactions = session.query(Transaction).filter(
                extract('year', Transaction.transaction_date) == year,
                extract('month', Transaction.transaction_date) == month
            ).all()
            transaction_list = []
            for transaction in transactions:
                transaction_list.append(
                    {
                        'id': transaction.id,
                        'transaction_date': transaction.transaction_date,
                        'amount': transaction.amount,
                        'description': transaction.description,
                        'pocket_name': transaction.pocket_name,
                        'category_name': transaction.category_name,
                        'transaction_type_name': transaction.transaction_type_name,
                        'destination_pocket_name': transaction.destination_pocket_name
                    }
                )
        return transaction_list

    def get_oldest_transaction_date(self) -> Optional[date]:
        with self._session_scope() as session:
            return session.query(func.min(Transaction.date)).scalar()

    def get_transactions_by_oldest_month_year(self) -> list[Transaction]:
        with self._session_scope() as session:
            oldest_record_date = self.get_oldest_transaction_date()
            oldest_month, oldest_year = oldest_record_date.month, oldest_record_date.year
            return session.query(Transaction).filter(
                func.extract('month', Transaction.transaction_date) == oldest_month,
                func.extract('year', Transaction.transaction_date) == oldest_year
            ).all()

    def delete_transaction_by_id(self, transaction_id: int) -> None:
        with self._session_scope() as session:
            transaction = session.query(Transaction).get(transaction_id)
            if transaction:
                session.delete(transaction)
            else:
                raise ObjectNotFound(f"Transaction with id {transaction_id} not found.")
