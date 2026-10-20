import time

from pipeline import crypto_pipeline

INTERVAL_SECONDS = 60

if __name__ == "__main__":
    try:
        while True:
            started = time.time()
            try:
                crypto_pipeline()
            except Exception as exc:
                print(f"Run failed: {exc}")
            elapsed = time.time() - started
            time.sleep(max(0, INTERVAL_SECONDS - elapsed))
    except KeyboardInterrupt:
        print("Stopped by user")