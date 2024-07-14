import ccxt
from pprint import pprint


class FutureSpotPriceFetcher:
    def __init__(self, secret_file):
        with open(secret_file) as f:
            lines = f.readlines()
            apiKey = lines[0].strip()
            secretKey = lines[1].strip()
            self._exchange = ccxt.binance(
                config={
                    "apiKey": apiKey,
                    "secret": secretKey,
                }
            )
        self._priceMap = {}  # sym : price

    def getAllPrice(self):
        self._updatePriceMap()
        self._updatePriceMap(spot=False)
        return self._priceMap

    def _updatePriceMap(self, spot=True):
        priceMap = self.getPriceMap()
        self.setExchangeToSpot() if spot else self.setExchangeToFutures()
        tickers = self.getExchange().fetchTickers()
        for sym, info in tickers.items():
            if info["ask"] and info["bid"]:
                priceMap[sym] = info["bid"] + ((info["ask"] - info["bid"]) / 2)

    def getExchange(self):
        return self._exchange

    def setExchangeToFutures(self):
        exchange = self.getExchange()
        exchange.options["defaultType"] = "future"

    def setExchangeToSpot(self):
        exchange = self.getExchange()
        exchange.options["defaultType"] = "spot"

    def getPriceMap(self):
        return self._priceMap


if __name__ == "__main__":
    fetcher = FutureSpotPriceFetcher("secret.txt")
    pprint(fetcher.getAllPrice())
