from datetime import date

from sqlalchemy import desc

from business_logic.models import CategoryPercentageRecord
from business_logic.repositories.repository import Repository


class CategoryPercentageRecordRepository(Repository):

    def create_category_percentage_record(self, percentage: float, record_date: date, category_name: str) -> None:
        with self._session_scope() as session:
            new_category_percentage_record = CategoryPercentageRecord(
                percentage=percentage, record_date=record_date,
                category_name=category_name
            )
            session.add(new_category_percentage_record)

    def create_category_percentage_records(self, category_percentage_records: list[dict]) -> bool:
        with self._session_scope() as session:
            for category_percentage_record_data in category_percentage_records:
                category_percentage_record = CategoryPercentageRecord(**category_percentage_record_data)
                session.add(category_percentage_record)
        return True

    def get_records_with_closest_date_before(self, target_date: date) -> list[dict]:
        with self._session_scope() as session:
            closest_date_before = session.query(CategoryPercentageRecord.record_date).filter(
                CategoryPercentageRecord.record_date < target_date
            ).order_by(desc(CategoryPercentageRecord.record_date)).first().record_date
            if not closest_date_before:
                return []
            category_percentage_records = session.query(CategoryPercentageRecord) \
                .filter(CategoryPercentageRecord.record_date == closest_date_before).all()
            records_list = []
            for category_percentage_record in category_percentage_records:
                records_list.append(
                    {
                        'id': category_percentage_record.id,
                        'percentage': category_percentage_record.percentage,
                        'record_date': category_percentage_record.record_date,
                        'category_name': category_percentage_record.category_name
                    }
                )
            return records_list
