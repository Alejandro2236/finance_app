from abc import ABC
from contextlib import contextmanager

from config.business_logic_db import BusinessLogicSession


class Repository(ABC):
    def __init__(self):
        self.__session = None

    @contextmanager
    def _session_scope(self):
        """Provide a transactional scope around a series of operations."""
        self.__connect()
        try:
            yield self.__session
            self.__session.commit()
        except Exception:
            if self.__session:
                self.__session.rollback()
            raise
        finally:
            self.__disconnect()

    def __connect(self):
        if not self.__session:
            self.__session = BusinessLogicSession()

    def __disconnect(self):
        if self.__session:
            self.__session.close()
            self.__session = None
