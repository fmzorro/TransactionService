import os
from abc import ABC, abstractmethod
from typing import Union

from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import Session, sessionmaker

from src.database.models.transaction_model import Base


class DBConnection(ABC):
    @abstractmethod
    def __init__(self):
        self.__config: Union[str, None]
        self.__engine: Union[Engine, None]
        self.__session: Union[Session, None]

    @property
    @abstractmethod
    def config(self):
        pass

    @property
    @abstractmethod
    def db_connection_url(self):
        pass

    @property
    @abstractmethod
    def engine(self):
        pass

    @property
    @abstractmethod
    def session(self):
        pass


class LocalDBConnection(DBConnection):
    def __init__(self):
        self.__config = None
        self.__engine = None
        self.__session = None

    @property
    def config(self):
        if not self.__config:
            self.__config = "sqlite:///database.db"

        return self.__config

    @property
    def db_connection_url(self):
        return f"{self.config}?check_same_thread=true"

    @property
    def engine(self):
        if not self.__engine:
            self.__engine = create_engine(self.db_connection_url)
            Base.metadata.create_all(bind=self.__engine)

        return self.__engine

    @property
    def session(self):
        return sessionmaker(autocommit=False, autoflush=False, bind=self.engine)


class HashicorpVaultDBConnection(DBConnection):
    def __init__(self):
        self.__config = None
        self.__engine = None
        self.__session = None

    @property
    def config(self):
        if not self.__config:
            self.__config = dict(
                database_username=os.getenv("DATABASE_USERNAME"),
                database_password=os.getenv("DATABASE_PASSWORD"),
                database_host_name=os.getenv("DATABASE_HOST_NAME"),
                database_port=os.getenv("DATABASE_PORT"),
                database_name=os.getenv("DATABASE_NAME"),
            )

        return self.__config

    @property
    def db_connection_url(self):
        return (
            "postgresql+psycopg2://"
            f"{self.config['database_username']}:"
            f"{self.config['database_password']}@"
            f"{self.config['database_host_name']}:"
            f"{self.config['database_port']}/"
            f"{self.config['database_name']}"
        )

    @property
    def engine(self):
        """
        Creates a SQLAlchemy engine, see below for more details:
        https://docs.sqlalchemy.org/en/20/core/engines.html

        Connection pooling:
        Reduces the cost of opening and closing connections by maintaining a “pool”
        of open connections to the database.
        https://docs.sqlalchemy.org/en/20/core/pooling.html

        Returns a connection resource to the database.
        """
        if not self.__engine:
            self.__engine = create_engine(
                self.db_connection_url,
                pool_pre_ping=True,  # Tests connections for liveness upon each checkout
                pool_size=32,
                max_overflow=64,  # Number of connections that can overflow pool size
            )
            Base.metadata.create_all(bind=self.__engine)

        return self.__engine

    @property
    def session(self):
        """
        Provides factory for Session objects with a fixed configuration.

        (a factory is an object for creating other objects)

        Uses connection resource from engine to connect to database.
        Handles all connections to the database and holds ongoing transactions

        session.flush() communicates a series of operations to the database (insert, update, delete).
        Saved as pending in the database. Changes are only persisted when session.commit() called.
        """
        if not self.__session:
            self.__session = sessionmaker(
                autocommit=False, autoflush=False, bind=self.engine
            )

        return self.__session


class DBConnectionFactory:
    @staticmethod
    def get_database_connection():
        database_env = os.getenv("DATABASE_ENV", "LOCAL").upper()
        if database_env == "LOCAL":
            return LocalDBConnection()
        elif database_env == "PRODUCTION":
            return HashicorpVaultDBConnection()


def get_db():
    session = None
    try:
        db_session = DBConnectionFactory().get_database_connection()
        session = db_session.session()
        yield session
    finally:
        if session:
            session.close()
