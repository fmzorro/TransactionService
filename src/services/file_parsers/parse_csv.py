from io import StringIO
import csv

from pydantic import ValidationError

from src.database.models.transactions import Transactions


class ParseCSV:
    def __init__(self, file_contents):
        self.file_contents = file_contents

    def parse(self):
        csv_file = csv.DictReader(StringIO(self.file_contents))
        transactions = []
        for row in csv_file:
            try:
                record = Transactions(
                    date=row["Date"],
                    type=row["Type"],
                    description=row["Description"],
                    value=row["Value"],
                    balance=row["Balance"],
                    account_name=row["Account Name"],
                    account_number=row["Account Number"],
                )
                transactions.append(record)
            except ValidationError as e:
                print(f"Failed to parse file\nReason: {e}")
                raise e

        return transactions
