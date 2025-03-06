from uuid import uuid4
from datetime import datetime, timezone

from sqlalchemy.orm import Session

from src.schemas.transaction_schema import Transaction
from src.database.models.transaction_model import TransactionModel


def create_transaction(
    transaction_schema: Transaction, db: Session
) -> TransactionModel:
    # Should begin by checking transaction ID not already created

    # transaction_schema.user_id needs to be set somehow?

    transaction_obj = TransactionModel(
        transaction_id=uuid4().hex,
        user_id=1,
        value=transaction_schema.value,
        type=transaction_schema.type,
        balance=transaction_schema.balance,
        transaction_date=datetime.strptime(transaction_schema.date, "%d %b %Y"),
        created=datetime.now(tz=timezone.utc),
    )

    db.add(transaction_obj)
    db.commit()
    db.refresh(transaction_obj)

    return transaction_obj


def get_transaction_by_id(transaction_id: str, db: Session) -> TransactionModel:
    return (
        db.query(TransactionModel)
        .filter(TransactionModel.transaction_id == transaction_id)
        .first()
    )


def get_transaction_by_unique_attributes(
    value: int, balance: int, date: str, db: Session
) -> list[TransactionModel]:
    return (
        db.query(TransactionModel)
        .filter(TransactionModel.value == value)
        .filter(TransactionModel.balance == balance)
        .filter(TransactionModel.transaction_date == date)
        .all()
    )


def update_transaction_by_id(
    transaction_schema: Transaction, db: Session
) -> TransactionModel:
    transaction_to_update = (
        db.query(TransactionModel)
        .filter(TransactionModel.transaction_id == transaction_schema.transaction_id)
        .first()
    )

    new_values = TransactionModel.model_dump(exclude_unset=True, exclude_none=True)

    for key, value in new_values.items():
        setattr(transaction_to_update, key, value)

    db.add(transaction_to_update)
    db.commit()
    db.refresh(transaction_to_update)

    return transaction_to_update


def delete_transaction_by_id(transaction_id: str, db: Session) -> None:
    db.query(TransactionModel).filter(
        TransactionModel.transaction_id == transaction_id
    ).delete()
    db.commit()

    print(db)
