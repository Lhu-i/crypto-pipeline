import requests

URL = "https://api.binance.com/api/v3/ticker/price"


def get_price(symbol):
    response = requests.get(URL, params={"symbol": symbol}, timeout=10)
    response.raise_for_status()
    return response.json()


if __name__ == "__main__":
    for symbol in ["BTCUSDT", "ETHUSDT", "SOLUSDT"]:
        data = get_price(symbol)
        print(data)