from sqlalchemy import Column, Integer, Float, Date, String, ForeignKey
from sqlalchemy.orm import relationship

from config.business_logic_db import BusinessLogicBase


class CategoryPercentageRecord(BusinessLogicBase):
    __tablename__ = 'category_percentage_record'
    id = Column(Integer, primary_key=True, autoincrement=True)
    percentage = Column(Float, nullable=False)
    record_date = Column(Date, nullable=False)
    category_name = Column(String(30), ForeignKey('category.name'), nullable=False)

    category = relationship('Category', backref='category_percentage_records')
