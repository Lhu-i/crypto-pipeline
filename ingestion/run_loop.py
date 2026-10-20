import logging
import time

from fetch_price import get_price
from load_prices import SYMBOLS, save_prices
from decimal import Decimal

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
)

INTERVAL_SECONDS = 10


def run_once():
    rows = []
    for symbol in SYMBOLS:
        data = get_price(symbol)
        rows.append((data["symbol"], Decimal(data["price"])))
    save_prices(rows)
    logging.info("Saved %d prices", len(rows))


if __name__ == "__main__":
    logging.info("Starting loop, interval=%ss. Press Ctrl+C to stop.", INTERVAL_SECONDS)
    try:
        while True:
            try:
                run_once()
            except Exception:
                logging.exception("Run failed, will retry next cycle")
            time.sleep(INTERVAL_SECONDS)
    except KeyboardInterrupt:
        logging.info("Stopped by user")