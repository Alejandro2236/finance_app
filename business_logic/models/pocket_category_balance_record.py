from sqlalchemy import Column, Float, Integer, Date, String, ForeignKey
from sqlalchemy.orm import relationship

from config.business_logic_db import BusinessLogicBase


class PocketCategoryBalanceRecord(BusinessLogicBase):
    __tablename__ = 'pocket_category_balance_record'
    id = Column(Integer, primary_key=True, autoincrement=True)
    balance = Column(Float, nullable=False)
    record_date = Column(Date, nullable=False)
    pocket_name = Column(String(30), ForeignKey('pocket.name'), nullable=False)
    category_name = Column(String(30), ForeignKey('category.name'), nullable=False)

    pocket = relationship('Pocket', backref='pocket_category_balance_record')
    category = relationship('Category', backref='pocket_category_balance_record')
