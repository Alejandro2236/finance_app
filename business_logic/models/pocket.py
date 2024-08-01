from sqlalchemy import Column, String

from config.business_logic_db import BusinessLogicBase


class Pocket(BusinessLogicBase):
    __tablename__ = 'pocket'
    name = Column(String(30), primary_key=True)
