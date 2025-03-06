from sqlalchemy import Column
from sqlalchemy.orm import declarative_base
from sqlalchemy.dialects.postgresql import CHAR, DATE, NUMERIC, VARCHAR, TIMESTAMP

Base = declarative_base()


class TransactionModel(Base):
    __tablename__ = "Transactions"
    _table_args__ = {"schema": "trans_data"}

    transaction_id = Column(CHAR(20), primary_key=True, nullable=False)
    user_id = Column(CHAR(15), nullable=False, index=True)
    value = Column(NUMERIC, nullable=False)
    type = Column(VARCHAR(250))
    balance = Column(NUMERIC, nullable=False)
    transaction_date = Column(DATE, nullable=False)
    created = Column(TIMESTAMP, nullable=False)
