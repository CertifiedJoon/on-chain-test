import ccxt

with open("secret.txt") as f:
    lines = f.readlines()
    apiKey = lines[0].strip()
    secretKey = lines[1].strip()

exchange = ccxt.binance(
    config={
        "apiKey": apiKey,
        "secret": secretKey,
    }
)

tickers = exchange.fetchTickers()

print(tickers)
