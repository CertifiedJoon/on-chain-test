import requests
from pprint import pprint


class Wallet:
    def __init__(self, walletAddress, secretFile):
        self._walletAddress = walletAddress
        self._apiKey = ""
        with open(secretFile) as f:
            lines = f.readlines()
            self._apiKey = lines[0].strip()

    def fetchTokenBalance(self, tokenAddress):
        params = {
            "module": "account",
            "action": "tokenbalance",
            "contractaddress": tokenAddress,
            "address": self.getWalletAddress(),
            "tag": "latest",
            "apiKey": self.getApiKey(),
        }

        r = requests.get("https://api-sepolia.etherscan.io/api", params)
        return r.json()["result"]

    def fetchTotalApprovedUSDCFor(self, logAddress, topic0, topic1, topic2):
        params = {
            "module": "logs",
            "action": "getLogs",
            "address": logAddress,
            "topic0": topic0,
            "topic1": topic1,
            "topic2": topic2,
            "apiKey": self.getApiKey(),
        }
        totalApprovedUSDC = 0
        results = requests.get("https://api-sepolia.etherscan.io/api", params).json()[
            "result"
        ]

        for result in results:
            totalApprovedUSDC += int(result["data"], 16)

        return totalApprovedUSDC / 1000000

    def getWalletAddress(self):
        return self._walletAddress

    def getApiKey(self):
        return self._apiKey


class Token:
    def __init__(self, tokenAddress, secretFile):
        self._tokenAddress = tokenAddress
        self._apiKey = ""
        with open(secretFile) as f:
            lines = f.readlines()
            self._apiKey = lines[0].strip()

    def getTotalSupply(self):
        params = {
            "module": "stats",
            "action": "tokensupply",
            "contractaddress": self.getTokenAddress(),
            "apiKey": self.getApiKey(),
        }

        r = requests.get("https://api-sepolia.etherscan.io/api", params)
        return int(r.json()["result"]) / 1000000

    def getTokenAddress(self):
        return self._tokenAddress

    def getApiKey(self):
        return self._apiKey


# fetch key
apiKey = ""
with open("secret2.txt") as f:
    lines = f.readlines()
    apiKey = lines[0].strip()

# ================================================================
# 1
walletAddress = "0x3CcFc9F04B510034afD1de63b2Fac824c7df1Fca"
payload = {
    "module": "account",
    "action": "balance",
    "address": walletAddress,
    "tag": "latest",
    "apiKey": apiKey,
}
r = requests.get("https://api-sepolia.etherscan.io/api", params=payload)
print("Q1")
print("Ether balance: " + str(r.json()["result"]) + "wei")


# ===============================================================
# 2


wallet = Wallet("0x3CcFc9F04B510034afD1de63b2Fac824c7df1Fca", "secret2.txt")
print("Q2, be aware of decimal representation of tokens")
print(
    "USDC balance: "
    + str(
        wallet.fetchTokenBalance(
            tokenAddress="0x1c7D4B196Cb0C7B01d743Fbc6116a902379C7238"
        )
    )
)

# ===============================================================
# 3
usdc = Token("0x1c7D4B196Cb0C7B01d743Fbc6116a902379C7238", "secret2.txt")
print("Q3, be aware of decimal representation of tokens")
print("USDC total supply: " + str(usdc.getTotalSupply()))


# ===============================================================
# 4

totalApprovedUSDC = wallet.fetchTotalApprovedUSDCFor(
    logAddress="0x1c7D4B196Cb0C7B01d743Fbc6116a902379C7238",
    topic0="0x8c5be1e5ebec7d5bd14f71427d1e84f3dd0314c0f7b2291e5b200ac8c7c3b925",
    topic1="0x0000000000000000000000003ccfc9f04b510034afd1de63b2fac824c7df1fca",
    topic2="0x0000000000000000000000003fc91a3afd70395cd496c647d5a6cc9d4b2b7fad",
)
print("Q4, be aware of decimal representation of tokens")
print("USDC approved for use: " + str(totalApprovedUSDC))
