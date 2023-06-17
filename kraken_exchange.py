import os
from decimal import Decimal
from dotenv import load_dotenv
from requests.exceptions import HTTPError

from krakenex import *

PAIR = {
    "BTCUSDT": "XBTUSDT",
    "ETHUSDT": "ETHUSDT",
}

load_dotenv()
API_KEY = os.getenv('KRAKEN_API_KEY')
SECRET_KEY = os.getenv('KRAKEN_SECRET_KEY')

class KrakenApi():

    def __init__(self):
        self.client = API(key=API_KEY, secret=SECRET_KEY)

    def get_account(self):
        return self.client.query_private("Balance")

    def get_market_prices(self, pairs: list):
        prices = dict()
        for pair in pairs:
            try:
                response = self.client.query_public('Ticker', {'pair': pair})
            except HTTPError as e:
                print(str(e))
            else:
                data = response
                market = data["result"][PAIR[pair]]
                price = (Decimal(market["a"][0]) + Decimal(market["b"][0])) / 2
                prices[pair] = price

        return prices
            