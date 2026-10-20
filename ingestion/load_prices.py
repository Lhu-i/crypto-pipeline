import os
from decimal import Decimal

import psycopg2
from dotenv import load_dotenv

from fetch_price import get_price

load_dotenv()

SYMBOLS = ["BTCUSDT", "ETHUSDT", "SOLUSDT"]

CREATE_TABLE = """
CREATE TABLE IF NOT EXISTS raw_prices (
    id SERIAL PRIMARY KEY,
    symbol TEXT NOT NULL,
    price NUMERIC(20, 8) NOT NULL,
    fetched_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
"""


def get_connection():
    return psycopg2.connect(
        host="localhost",
        port=5432,
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD"),
        dbname=os.getenv("POSTGRES_DB"),
    )


def save_prices(rows):
    conn = get_connection()
    try:
        with conn:
            with conn.cursor() as cur:
                cur.execute(CREATE_TABLE)
                cur.executemany(
                    "INSERT INTO raw_prices (symbol, price) VALUES (%s, %s)",
                    rows,
                )
    finally:
        conn.close()


if __name__ == "__main__":
    rows = []
    for symbol in SYMBOLS:
        data = get_price(symbol)
        rows.append((data["symbol"], Decimal(data["price"])))

    save_prices(rows)
    print(f"Saved {len(rows)} prices")