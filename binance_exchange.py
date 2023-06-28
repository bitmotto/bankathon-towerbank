import os
from dotenv import load_dotenv
from decimal import Decimal

from binance.spot import Spot as Client


load_dotenv()
BASE_URL = os.getenv('BINANCE_BASE_URL')
API_KEY = os.getenv('BINANCE_API_KEY')
SECRET_KEY = os.getenv('BINANCE_SECRET_KEY')

class BinanceApi():

    def __init__(self):
        self.client = Client(
            base_url=BASE_URL, api_key=API_KEY, api_secret=SECRET_KEY
        )

    def account(self):
       return self.client.account()

    def get_market_prices(self, pairs: list):
        # https://binance-docs.github.io/apidocs/spot/en/#current-average-price

        prices = dict()
        book_tickers = self.client.book_ticker(symbols=pairs)
        for book in book_tickers:
            price = (Decimal(book["askPrice"]) + Decimal(book["bidPrice"])) / 2
            prices[book['symbol']] = price

        return prices

    
    def new_buy_market_order(self, pair: str, stable_coin_amount: str):
        order = self.client.new_order(
            symbol=pair,
            side="BUY",
            type="MARKET",
            quoteOrderQty=stable_coin_amount,
        )

        return order


