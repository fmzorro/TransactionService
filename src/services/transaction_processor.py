from sqlalchemy.orm import Session

from src.database.transactions_crud import (
    create_transaction,
    get_transaction_by_unique_attributes,
)
from src.schemas.transaction_schema import Transaction


class TransactionProcessor:
    def process_transaction(
        self, db_session: Session, transaction_list: list[Transaction]
    ):
        for transaction in transaction_list:
            transaction_found = get_transaction_by_unique_attributes(
                value=transaction.value,
                balance=transaction.balance,
                date=transaction.date,
                db=db_session,
            )

            if transaction_found:
                print(f"Transaction already processed: {transaction}")

            created_transaction = create_transaction(
                transaction_schema=transaction, db=db_session
            )
            print(created_transaction)
