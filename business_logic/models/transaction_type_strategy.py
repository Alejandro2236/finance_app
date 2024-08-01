from sqlalchemy import Column, String

from config.business_logic_db import BusinessLogicBase


class TransactionTypeStrategy(BusinessLogicBase):
    __tablename__ = 'strategy'
    name = Column(String(30), primary_key=True)
