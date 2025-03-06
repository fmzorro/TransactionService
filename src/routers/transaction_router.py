from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy.orm import Session

from src.database.db_connection import get_db
from src.schemas.transaction_schema import Transaction
from src.services.transaction_processor import TransactionProcessor

transaction_router = APIRouter(
    prefix="/transaction",
    tags=["Transactions"],
    responses={404: {"description": "Not found"}},
    # Get user somehow? Token?
)


@transaction_router.post("/")
def upload_transaction(
    transactions: list[Transaction], db_session: Session = Depends(get_db)
):
    """
    Receives transactions as JSON files.

    Determines if each transaction is new or not.

    Writes new transactions to the database.
    """
    try:
        TransactionProcessor().process_transaction(
            db_session=db_session, transaction_list=transactions
        )
    except HTTPException as exception:
        print(f"Exception: {exception}")
        raise exception
