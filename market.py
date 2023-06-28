import time
from decimal import Decimal
from binance_exchange import BinanceApi
from kraken_exchange import KrakenApi
from towerbank import TowerbankAPI

EXCHANGES = ["BINANCE", "KRAKEN"]
PAIRS = ["BTCUSDT", "ETHUSDT"]

def get_market_price_from_binance(pairs):
    b = BinanceApi()
    return b.get_market_prices(pairs)

def get_market_price_from_kraken(pairs):
    k = KrakenApi()
    return k.get_market_prices(pairs)

def get_market_prices(pairs):
    b_prices = get_market_price_from_binance(pairs)
    k_prices = get_market_price_from_kraken(pairs)

    return { "KRAKEN": k_prices, "BINANCE": b_prices }


def get_best_price_for_buy():
    pairs = ["BTCUSDT", "ETHUSDT"]
    prices = get_market_prices(pairs)
    best = []
    for pair in pairs:
        exchange_name = None,
        price = 100000000000000
        for exchange in EXCHANGES:
            exchange_price = prices[exchange][pair]
            if exchange_price < price:
                price = exchange_price
                exchange_name = exchange
        best.append(
            {
                "pair": pair,
                "price": price,
                "exchange": exchange_name
            }
        )
    
    return prices, best


def get_best_price_for_sell():
    pairs = ["BTCUSDT", "ETHUSDT"]
    prices = get_market_prices(pairs)
    best = []
    for pair in pairs:
        exchange_name = None,
        price = 0
        for exchange in EXCHANGES:
            exchange_price = prices[exchange][pair]
            if exchange_price > price:
                price = exchange_price
                exchange_name = exchange
        best.append(
            {
                "pair": pair,
                "price": price,
                "exchange": exchange_name
            }
        )
    
    return prices, best

def get_binance_user_balance():
    binance = BinanceApi()
    account = binance.account()
    print(f"Account type: {account['accountType']}")
    for balance in account["balances"]:
        print(balance)

def get_account_balance():
    get_binance_user_balance()

def create_buy_order():
    asset = input("Indique el asset a comprar: ")
    usdt_amount = input("Cuantos USDT va a utilizar: ")
    if asset.upper() not in ["BTC", "ETH"]:
        raise ValueError("Asset no permitido")
    
    pair = f"{asset.upper()}USDT"
    amount = Decimal(usdt_amount)
    binance = BinanceApi()
    order = binance.new_buy_market_order(pair, amount)
    print(order)


def get_towebank_balance():
    t = TowerbankAPI()
    provider = t.get_provider_balance()

    return provider


def buy_cripto(client_info):
    try:
        amount = float(input("¿Cúanto desea comprar (expresado en PAB)? "))
    except Exception:
        raise ValueError("Monto incorrecto")
    
    if amount > client_info["balance"]:
        print("Error: Saldo Insuficiente")
        print("Intente nuevamente")
        return None

    cryptocurrency = input("¿Cuál cripto desea comprar? ").upper()
    pair = f"{cryptocurrency}USDT"
    if pair not in PAIRS:
        print("Criptomoneda no habilitada")
        print("Intente nuevamente")
        return None


    prices, best_price = get_best_price_for_buy()
    print(f"\nPrices:")
    for e in EXCHANGES:
        print(f"{e}: {prices[e]}")

    best_exchange = "BINANCE"
    print(f"\nBest Prices for buy:")
    for b in best_price:
        if pair == b['pair']:
            best_exchange = b['exchange']
            print(f"{b['pair']}: {b['price']} - Exchange: {b['exchange']}")

    exchange_balance = get_towebank_balance()
    towerbank_balance = 0
    for e in exchange_balance["data"]:
        if best_exchange.lower() == e["name"]:
            towerbank_balance = float(e["balance"])

    if amount > towerbank_balance:
        print("No se puede realizar la compra en este momento")
        print("Intente más tarde")
        return None

    # TODO: Hacer la compra en cripto.
    # Este método está hecha para Binance falta para Kraken 
    # Simulación de la compra en el exchange
    print("\nComprando criptos...")
    time.sleep(3)

    print("\n¡Compra éxitosa!\n")
    
    transaction = t.account_transaction(client_info['accountId'], amount, "sale")
    print(f"Transaction ID: {transaction['transferId']} - Monto: {amount}")
    print(f"Balance {transaction['balance']}")


def sell_cripto(client_info):
    try:
        amount = float(input("¿Cúanto desea vender (expresado en PAB)? "))
    except Exception:
        raise ValueError("Monto incorrecto")
    
    # TODO: Validación del balance del usuario en cripto
    # if amount > client_info["balance"]:
    #    print("Error: Saldo Insuficiente")
    #    print("Intente nuevamente")
    #    return None

    cryptocurrency = input("¿Cuál cripto desea vender? ").upper()
    pair = f"{cryptocurrency}USDT"
    if pair not in PAIRS:
        print("Criptomoneda no habilitada")
        print("Intente nuevamente")
        return None


    prices, best_price = get_best_price_for_sell()
    print(f"\nPrices:")
    for e in EXCHANGES:
        print(f"{e}: {prices[e]}")

    best_exchange = "BINANCE"
    print(f"\nBest Prices for sell:")
    for b in best_price:
        if pair == b['pair']:
            best_exchange = b['exchange']
            print(f"{b['pair']}: {b['price']} - Exchange: {b['exchange']}")

    # TODO: Obtener el balance de towerbank en cripto
    '''exchange_balance = get_towebank_balance()
    towerbank_balance = 0
    for e in exchange_balance["data"]:
        if best_exchange.lower() == e["name"]:
            towerbank_balance = float(e["balance"])

    if amount > towerbank_balance:
        print("No se puede realizar la compra en este momento")
        print("Intente más tarde")
        return None
    '''

    # TODO: Hacer la venta en cripto.
    # Este método está hecha para Binance falta para Kraken 
    # Simulación de la venta en el exchange
    print("\nVendienco criptos...")
    time.sleep(3)
    
    print("\n¡Venta éxitosa!\n")
    
    transaction = t.account_transaction(client_info['accountId'], amount, "purchase")
    print(f"Transaction ID: {transaction['transferId']} - Monto: {amount}")
    print(f"Balance {transaction['balance']}")


def funds_balance():
    exchange_balance = get_towebank_balance()
    print(exchange_balance)

    return None


if __name__ == "__main__":
    print("Bienvenido\n")
    t = TowerbankAPI()
    client_info = t.get_client_account()

    print("Información de la cuenta del cliente:")
    print("--------------------------------------------------------------------------")
    print(f"| Nro. cuenta {client_info['accountId']} - Balance: PAB {client_info['balance']} |")
    print("--------------------------------------------------------------------------\n")

    print("Operaciones disponibles:")
    print("--------------------------------------------------------------------------")
    print("1.- Compra de criptomoneda")
    print("2.- Venta de criptomoneda")
    option = input("Presione cualquier otro valor para salir: ")
    print("\n")

    if option == "1":
        buy_cripto(client_info)
    elif option == "2":
        sell_cripto(client_info)
    else:
        print("Gracias, nos vemos pronto.")
