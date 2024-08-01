from datetime import date
from typing import Optional

from sqlalchemy import func

from business_logic.exceptions.object_not_found import ObjectNotFound
from business_logic.models import PocketCategoryBalanceRecord
from business_logic.repositories.repository import Repository


class PocketCategoryBalanceRecordRepository(Repository):

    def create_record(
        self, balance: float, record_date: date, pocket_name: str,
        category_name: str
    ) -> None:
        with self._session_scope() as session:
            new_pocket_category_balance_record = PocketCategoryBalanceRecord(
                balance=balance, record_date=record_date,
                pocket_name=pocket_name,
                category_name=category_name
            )
            session.add(new_pocket_category_balance_record)

    def get_record_at_month(self, target_date: date, pocket_name: str, category_name: str) -> Optional[dict]:
        with self._session_scope() as session:
            record = session.query(PocketCategoryBalanceRecord).filter(
                func.extract('month', PocketCategoryBalanceRecord.record_date) == target_date.month,
                func.extract('year', PocketCategoryBalanceRecord.record_date) == target_date.year,
                PocketCategoryBalanceRecord.pocket_name == pocket_name,
                PocketCategoryBalanceRecord.category_name == category_name
            ).first()
            if record is None:
                return None
            return {
                'id': record.id,
                'balance': record.balance,
                'record_date': record.record_date,
                'pocket_name': record.pocket_name,
                'category_name': record.category_name
            }

    def get_latest_record_date(self) -> Optional[date]:
        with self._session_scope() as session:
            return session.query(func.max(PocketCategoryBalanceRecord.record_date)).scalar()

    def get_all_records(self) -> list[dict]:
        records_list = []
        with self._session_scope() as session:
            records: list[PocketCategoryBalanceRecord] = session.query(PocketCategoryBalanceRecord).all()
            for record in records:
                records_list.append(
                    {
                        'id': record.id,
                        'balance': record.balance,
                        'record_date': record.record_date,
                        'pocket_name': record.pocket_name,
                        'category_name': record.category_name
                    }
                )
        return records_list

    def update_record(self, record_date: date, actual_pocket_name: str, actual_category_name: str, **kwargs) -> None:
        with self._session_scope() as session:
            record = session.query(PocketCategoryBalanceRecord).filter(
                func.extract(
                    'month',
                    PocketCategoryBalanceRecord.record_date
                ) == record_date.month,
                func.extract(
                    'year',
                    PocketCategoryBalanceRecord.record_date
                ) == record_date.year,
                PocketCategoryBalanceRecord.pocket_name == actual_pocket_name,
                PocketCategoryBalanceRecord.category_name == actual_category_name
            ).first()
            if record:
                for key, value in kwargs.items():
                    if not hasattr(record, key):
                        raise AttributeError(f"{PocketCategoryBalanceRecord.__name__} object has no attribute '{key}'")
                    setattr(record, key, value)
                print(f"Updating record {record.id} with values: {kwargs}")
                if record.record_date.month == 4:
                    print(record.balance)
                session.add(record)
            else:
                raise ObjectNotFound(f"Record not found for the given date: {record_date}.")

    def delete_all_records(self):
        with self._session_scope() as session:
            session.query(PocketCategoryBalanceRecord).delete()
