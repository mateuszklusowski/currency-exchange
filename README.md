# Overview
Script to automate the conversion of currency values and their storage on amazon s3.

Data are taken from the official api from the nbp.

The data entered are processed with requests, resulting in data from the available day (except weekends).

Datas are stored to the databade, converted to json file and pushed to the cloud.

If exchange already exists, script does not make request but get data from database.

**json file example:** *{exchanged_date}, {currency_to_exchange}-{currency_to_exchange_for}.json*
# How run script
First, clone the project
```bash
  git clone https://github.com/mateuszklusowski/currency-exchange.git
```
Go to the project directory
```bash
  cd currency-exchange
```
Install dependencies
```bash
  docker-compose build
```
Run script
```bash
  docker-compose run --rm app sh -c "python main.py"
```
Example data inputs
```bash
Enter the ammount: 10
Enter the currency you wish to exchange (THB, USD, AUD, HKD, CAD, NZD, SGD, EUR, HUF, CHF, GBP, UAH, JPY, CZK, DKK, ISK, NOK, SEK, HRK, RON, BGN, TRY, ILS, CLP, PHP, MXN, ZAR, BRL, MYR, IDR, INR, KRW, CNY, XDR): XDR
Enter the currency you wish to exchange for (THB, USD, AUD, HKD, CAD, NZD, SGD, EUR, HUF, CHF, GBP, UAH, JPY, CZK, DKK, ISK, NOK, SEK, HRK, RON, BGN, TRY, ILS, CLP, PHP, MXN, ZAR, BRL, MYR, IDR, INR, KRW, CNY, XDR): XDR
Enter date in format YYYY-MM-DD: 2022-10-13
```
If you get stuck, type "python main.py --help". 
```bash
  docker-compose run --rm app sh -c "python main.py --help"
```
Below you can see command result:
```bash
Usage: main.py [OPTIONS]

Options:
  --ammount FLOAT RANGE           [x<=None; required]
  --from_currency [THB|USD|AUD|HKD|CAD|NZD|SGD|EUR|HUF|CHF|GBP|UAH|JPY|CZK|DKK|ISK|NOK|SEK|HRK|RON|BGN|TRY|ILS|CLP|PHP|MXN|ZAR|BRL|MYR|IDR|INR|KRW|CNY|XDR]
                                  [required]
  --to_currency [THB|USD|AUD|HKD|CAD|NZD|SGD|EUR|HUF|CHF|GBP|UAH|JPY|CZK|DKK|ISK|NOK|SEK|HRK|RON|BGN|TRY|ILS|CLP|PHP|MXN|ZAR|BRL|MYR|IDR|INR|KRW|CNY|XDR]
                                  [required]
  --entry_date [%Y-%m-%d]         [required]
  --help                          Show this message and exit.

```
