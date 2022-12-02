import sqlite3


class Database:
    def __init__(self, database_name):
        self.connection = sqlite3.connect(database_name)
        self.cursor = self.connection.cursor()

        self.cursor.execute(
            """
            CREATE TABLE if not exists last_operations(
                from_currency text,
                to_currency text,
                value float,
                exchange_rate_date text
            );
            """
        )

    def check_values_for_currencies(self, from_currency, to_currency, date):
        query = f"""
            SELECT
                value
            FROM
                last_operations
            WHERE
                from_currency LIKE %{from_currency}s
            AND
                to_currency LIKE %{to_currency}s
            AND
                exchange_rate_date LIKE %{date}s;""",{
                'from_currency': from_currency,
                'to_currency': to_currency,
                'date': date
            }

        return self.cursor.execute(query)

    def __del__(self):
        self.connection.close()
