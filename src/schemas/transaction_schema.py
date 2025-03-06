from decimal import Decimal

from pydantic import BaseModel


class Transaction(BaseModel):
    date: str
    type: str
    description: str
    value: Decimal
    balance: Decimal
    account_name: str
    account_number: str
