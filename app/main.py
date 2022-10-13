import click

import json

from datetime import datetime, timedelta

import asyncio

import httpx

from database import Database

from aws_bucket import Bucket

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

CHECK_URL = "http://api.nbp.pl/api/exchangerates/tables/A/"
CURRENCY_URL = "http://api.nbp.pl/api/exchangerates/rates/A/"


async def check_api_call(entry_date):
    url = f'{CHECK_URL}{entry_date.strftime("%Y-%m-%d")}/'

    async with httpx.AsyncClient(timeout=None) as client:
        response = await client.get(url)

    if response.status_code == 400:
        return False

    if response.status_code == 200:
        return True


async def get_currencies_mid(date, from_currency, to_currency):
    mid_values = {}
    curency_list = (from_currency + " " + to_currency).split(" ")

    for currency in curency_list:

        url = f'{CURRENCY_URL}{currency}/{date.strftime("%Y-%m-%d")}/?format=json'

        async with httpx.AsyncClient(timeout=None) as client:
            response = await client.get(url)

        mid_values.update({currency: response.json()["rates"][0]["mid"]})

    return mid_values


@click.command()
@click.option(
    "--ammount", type=click.FloatRange(), required=True, prompt="Enter the ammount"
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
):

    if entry_date < datetime(2002, 1, 2):
        raise ValueError("Too old date")

    today = datetime.today().strftime("%Y-%m-%d")

    while entry_date.strftime("%Y-%m-%d") > today:
        entry_date = entry_date - timedelta(days=1)

    while entry_date.weekday() > 4:
        entry_date = entry_date - timedelta(days=1)

    while not asyncio.run(check_api_call(entry_date)):
        entry_date = entry_date - timedelta(days=1)

    value = db.check_values_for_currencies(
        from_currency, to_currency, entry_date.strftime("%Y-%m-%d")
    ).fetchone()

    if value is None:
        data_values = asyncio.run(
            get_currencies_mid(entry_date, from_currency, to_currency)
        )
        value = float(data_values[from_currency] / data_values[to_currency])

        db.cursor.execute(
            "INSERT INTO last_operations VALUES (?, ?, ?, ?)",
            (
                f"{from_currency}",
                f"{to_currency}",
                f"{value}",
                f'{entry_date.strftime("%Y-%m-%d")}',
            ),
        )
        db.connection.commit()
    else:
        value = value[0]

    exchanged_dict = {
            "ammount": ammount,
            "from_currency": from_currency,
            "to_currency": to_currency,
            "exchanged_ammount": round((value * ammount), 2),
            "exchange_rate_date": entry_date.strftime("%Y-%m-%d"),
        }
    
    client = Bucket()
    client.add_file(exchanged_dict)

    del db
    return exchanged_dict

if __name__ == "__main__":
    get_current()
