import sqlite3


class Database:
    def __init__(self, database_name: str):
        self.connection = sqlite3.connect(database_name)
        self.cursor = self.connection.cursor()
        # Create a new databse if now exists
        self.cursor.execute(
            "CREATE TABLE if not exists last_operations(\
            from_currency text,\
            to_currency text,\
            value float,\
            exchange_rate_date text);"
        )

    def check_values_for_currencies(
        self, from_currency: str, to_currency: str, date: str
    ):
        # Get the value and date of the exchange
        return self.cursor.execute(
            "SELECT value, exchange_rate_date \
            FROM last_operations \
            WHERE from_currency LIKE ? \
            AND to_currency LIKE ? \
            AND exchange_rate_date LIKE ?",
            (from_currency, to_currency, date),
        )
