from towerbank import TowerbankAPI

def get_towebank_balance():
    t = TowerbankAPI()
    provider = t.get_provider_balance()

    return provider

def transfer_towerbank_balance(from_exchange, to_exchange, amount):
    t = TowerbankAPI()
    transfer = t.provider_transaction(from_exchange, to_exchange, amount)

    return transfer

def get_balance(exchage):
    return exchage.get('balance')

def order_by_high_to_low_amount(exchanges):
    order_exchange = exchanges
    order_exchange.sort(key=get_balance, reverse=True)

    return order_exchange

def order_by_low_to_high_amount(exchanges):
    order_exchange = exchanges
    order_exchange.sort(key=get_balance)

    return order_exchange

def amount_required_by_exchange(exchanges, minimum_amount):
    exchange = {}
    for e in exchanges:
        exchange[e['name']] = minimum_amount - float(e['balance'])

    return exchange

def amount_available_by_exchange(exchanges, minimum_amount):
    exchange = {}
    for e in exchanges:
        exchange[e['name']] = float(e['balance']) - minimum_amount

    return exchange


def separate_low_high_balance(exchange_balance, minimum_amount):
    exchange_low_balance, exchange_high_balance = [], []
    for exchange in exchange_balance["data"]:
        print(f"{exchange['name'].upper()}: PAB {exchange['balance']}")
        if float(exchange['balance']) < minimum_amount:
            exchange_low_balance.append(exchange)
        else:
            exchange_high_balance.append(exchange)
    
    return exchange_low_balance, exchange_high_balance


def balance_process(minimum_amount):
    exchange_low_balance, exchange_high_balance = [], []
    print("Obteniendo Balance de los Exchange...")
    exchange_balance = get_towebank_balance()
    exchange_low_balance, exchange_high_balance = separate_low_high_balance(
        exchange_balance, minimum_amount
    )

    print("\nConfiguración:")
    print(f"El monto mínimo límite es: PAB {minimum_amount} \n")

    if len(exchange_low_balance) == 0:
        print("No hay exchange que necesiten transferencia")
        return None
    
    if len(exchange_high_balance) == 0:
        print("No hay exchange con suficiente fondos para transferir")
        print("Notificar al Banco para que recargue fondos a todos los exchanges")
        return None

    print("Exchange que necesitan transferencia: ")
    exchange_low_balance = order_by_low_to_high_amount(exchange_low_balance)
    exchange_high_balance = order_by_high_to_low_amount(exchange_high_balance)
    for exchange in exchange_low_balance:
        print(f"{exchange['name'].upper()}: PAB {exchange['balance']}")
    
    print("\nProcesando...")
    amount_required = amount_required_by_exchange(exchange_low_balance, minimum_amount)
    amount_available = amount_available_by_exchange(exchange_high_balance, minimum_amount)
    for e_low in exchange_low_balance:
        for e_high in exchange_high_balance:
            amount_r = amount_required[e_low['name']]
            amount_a = amount_available[e_high['name']]
            if amount_r == 0:
                continue
            elif amount_a > amount_r:
                print(f"Transfiriendo PAB {amount_r} desde {e_high['name'].upper()} a {e_low['name'].upper()}")
                transfer = transfer_towerbank_balance(e_high['name'], e_low['name'], amount_r)
                print(f"Transferencia exitosa --> ID: {transfer['transactionid']}")
                amount_required[e_low['name']] = amount_required[e_low['name']] - amount_r
                amount_available[e_high['name']] = amount_available[e_high['name']] - amount_r
            else:
                print(f"Transfiriendo PAB {amount_a} desde {e_high['name'].upper()} a {e_low['name'].upper()}")
                transfer = transfer_towerbank_balance(e_high['name'], e_low['name'], amount_a)
                print(f"Transferencia exitosa --> ID: {transfer['transactionid']}")
                amount_required[e_low['name']] = amount_required[e_low['name']] - amount_a
                amount_available[e_high['name']] = amount_available[e_high['name']] - amount_a

    print("\nBalances actualizados: ")
    exchange_balance = get_towebank_balance()
    exchange_low_balance, exchange_high_balance = separate_low_high_balance(
        exchange_balance, minimum_amount
    )


if __name__ == "__main__":
    print("Bienvenido \n")

    minimum_amount = float(input("Indique el monto mínimo límite: "))
    balance_process(minimum_amount)
