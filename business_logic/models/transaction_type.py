from sqlalchemy import Column, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from config.business_logic_db import BusinessLogicBase


class TransactionType(BusinessLogicBase):
    __tablename__ = 'transaction_type'
    name = Column(String(30), primary_key=True)
    requires_destination_pocket = Column(Boolean, default=False)
    strategy_name = Column(String(30), ForeignKey('strategy.name'), unique=True, nullable=False)

    strategy = relationship(
        "TransactionTypeStrategy",
        uselist=False,
        backref="transaction_type",
        foreign_keys=[strategy_name]
        )
