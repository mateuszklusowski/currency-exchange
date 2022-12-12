import datetime
import asyncio
import click
import httpx
from .database import Database
from .aws_bucket import Bucket

CURRENCIES = [
    "THB",
    "USD",
    "AUD",
    "HKD",
    "CAD",
    "NZD",
    "SGD",
    "EUR",
    "HUF",
    "CHF",
    "GBP",
    "UAH",
    "JPY",
    "CZK",
    "DKK",
    "ISK",
    "NOK",
    "SEK",
    "HRK",
    "RON",
    "BGN",
    "TRY",
    "ILS",
    "CLP",
    "PHP",
    "MXN",
    "ZAR",
    "BRL",
    "MYR",
    "IDR",
    "INR",
    "KRW",
    "CNY",
    "XDR",
]

CURRENCY_URL = "http://api.nbp.pl/api/exchangerates/rates/A/"

client = httpx.AsyncClient(timeout=None)


async def check_api_call(date, currency: str):
    new_date = date.strftime("%Y-%m-%d")
    # Create request
    url = f"{CURRENCY_URL}{currency}/{new_date}/?format=json"
    response = await client.get(url)

    if response.status_code == 200:
        return response
    return False


async def get_currencies_mid(
    date, from_currency: str, to_currency: str
) -> dict:
    response = await check_api_call(date, from_currency)
    # Check that datas with the current date are available
    while not response:
        date = date - datetime.timedelta(days=1)
        response = await check_api_call(date, from_currency)

    mid_values = {}
    mid_values.update({from_currency: response.json()["rates"][0]["mid"]})
    # Add to_currency to the dict
    response = await check_api_call(date, to_currency)
    mid_values.update({to_currency: response.json()["rates"][0]["mid"]})
    # Added result date
    mid_values.update({"date": response.json()["rates"][0]["effectiveDate"]})
    return mid_values


@click.command()
@click.option(
    "--ammount",
    type=click.FloatRange(),
    required=True,
    prompt="Enter the ammount",
)
@click.option(
    "--from_currency",
    type=click.Choice(CURRENCIES),
    required=True,
    prompt="Enter the currency you wish to exchange",
)
@click.option(
    "--to_currency",
    type=click.Choice(CURRENCIES),
    required=True,
    prompt="Enter the currency you wish to exchange for",
)
@click.option(
    "--entry_date",
    type=click.DateTime(formats=("%Y-%m-%d",)),
    required=True,
    prompt="Enter date in format YYYY-MM-DD",
)
def get_current(
    ammount, from_currency, to_currency, entry_date, db=Database("sqlite3.db")
) -> dict:
    if entry_date < datetime.datetime(2002, 1, 2):
        raise ValueError("Too old date.")

    exchanged_dict = {
        "ammount": ammount,
        "from_currency": from_currency,
        "to_currency": to_currency,
    }
    # Get values if exists
    query = db.check_values_for_currencies(
        from_currency, to_currency, entry_date.strftime("%Y-%m-%d")
    ).fetchone()
    # Insert values to the database
    if query is None:
        data_values = asyncio.run(
            get_currencies_mid(entry_date, from_currency, to_currency)
        )
        exchanged_value = float(
            data_values[from_currency] / data_values[to_currency]
        )
        db.cursor.execute(
            "INSERT INTO last_operations VALUES (?, ?, ?, ?)",
            (
                from_currency,
                to_currency,
                exchanged_value,
                data_values["date"],
            ),
        )
        db.connection.commit()
        exchanged_dict.update(
            {"exchanged_ammount": round((exchanged_value * ammount), 2)}
        )
        exchanged_dict.update({"exchange_rate_date": data_values["date"]})
    else:
        exchanged_dict.update(
            {"exchanged_ammount": round((query[0] * ammount), 2)}
        )
        exchanged_dict.update({"exchange_rate_date": query[1]})

    client = Bucket()
    client.add_file(exchanged_dict)

    del db
    return exchanged_dict


if __name__ == "__main__":
    get_current()
