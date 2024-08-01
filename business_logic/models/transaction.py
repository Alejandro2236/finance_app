from sqlalchemy import Column, Integer, Date, Float, String, ForeignKey
from sqlalchemy.orm import relationship

from config.business_logic_db import BusinessLogicBase


class Transaction(BusinessLogicBase):
    __tablename__ = 'transaction'
    id = Column(Integer, primary_key=True, autoincrement=True)
    transaction_date = Column(Date, nullable=False)
    amount = Column(Float, nullable=False)
    description = Column(String, nullable=True)
    pocket_name = Column(String(30), ForeignKey('pocket.name'), nullable=False)
    category_name = Column(String(30), ForeignKey('category.name'), nullable=False)
    transaction_type_name = Column(String(30), ForeignKey('transaction_type.name'), nullable=False)
    destination_pocket_name = Column(String(30), ForeignKey('pocket.name'), nullable=True)

    pocket = relationship('Pocket', foreign_keys=[pocket_name], backref='transactions')
    category = relationship('Category', backref='transactions')
    transaction_type = relationship('TransactionType', backref='transactions')
    destination_pocket = relationship(
        'Pocket', foreign_keys=[destination_pocket_name],
        backref='destination_transactions'
        )
