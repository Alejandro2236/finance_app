from sqlalchemy import Column, String

from config.business_logic_db import BusinessLogicBase


class Category(BusinessLogicBase):
    __tablename__ = 'category'
    name = Column(String(30), primary_key=True)
