# Bitmotto App - Towerbank

Este repositorio contiene la solución a los problemas planteados en el Bankathon de Towerbank. La solución fue desarrollada en Python 3.

## Instalación de requerimientos

```bash
pip install -r requirements.txt
```

## Variables de Entorno

Cree el archivo .env en el directorio raiz del proyecto e inserte las siguientes variables con los valores correspondiente. Ver .env-example

```bash
BINANCE_API_KEY="binance api key"
BINANCE_SECRET_KEY="binance secrret key"
BINANCE_BASE_URL="https://testnet.binance.vision"

KRAKEN_API_KEY="kraken api key"
KRAKEN_SECRET_KEY="kraken secret key"

TOWERBANK_API_KEY="Towerbank api key"
TOWERBANK_BASE_URL="https://towerbank.bankathontb.com/bankathon/v1"
```

## Usage

Para correr la simulación de compra y venta:

```python
python3 market.py
```

Para probar la simulación de balanceo de fondos:

```python
python3 exchange_transaction.py
```
