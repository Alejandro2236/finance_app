import os
from time import sleep

from dotenv import load_dotenv
from sqlalchemy import create_engine, inspect
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from business_logic import models

load_dotenv()

business_logic_db_string_connection = os.getenv('DB_BUSINESS_LOGIC_CONNECTION')

business_logic_engine = create_engine(business_logic_db_string_connection)

BusinessLogicSession = sessionmaker(bind=business_logic_engine)

BusinessLogicBase = declarative_base()


def init_business_logic_db():
    BusinessLogicBase.metadata.create_all(bind=business_logic_engine)


def get_table_names():
    inspector = inspect(business_logic_engine)
    return inspector.get_table_names()


def delete_all_tables():
    BusinessLogicBase.metadata.drop_all(bind=business_logic_engine)
    BusinessLogicBase.metadata.clear()


def reset_db():
    from business_logic import models

    # Drop all tables
    BusinessLogicBase.metadata.drop_all(bind=business_logic_engine)
    sleep(5)
    # Clear the metadata
    BusinessLogicBase.metadata.clear()
    sleep(5)
    # Create all tables
    BusinessLogicBase.metadata.create_all(bind=business_logic_engine)
    sleep(5)
