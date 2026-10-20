import sys
from decimal import Decimal
from pathlib import Path

from prefect import flow, task

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "ingestion"))

from dbt.cli.main import dbtRunner  # noqa: E402
from fetch_price import get_price  # noqa: E402
from load_prices import SYMBOLS, save_prices  # noqa: E402

DBT_DIR = str(ROOT / "dbt_project")


@task(retries=3, retry_delay_seconds=5)
def fetch_and_load():
    rows = []
    for symbol in SYMBOLS:
        data = get_price(symbol)
        rows.append((data["symbol"], Decimal(data["price"])))
    save_prices(rows)
    return len(rows)


@task
def run_dbt():
    result = dbtRunner().invoke(
        ["build", "--project-dir", DBT_DIR, "--profiles-dir", DBT_DIR]
    )
    if not result.success:
        raise RuntimeError("dbt build failed")


@flow(log_prints=True)
def crypto_pipeline():
    count = fetch_and_load()
    print(f"Saved {count} prices")
    run_dbt()


if __name__ == "__main__":
    crypto_pipeline()