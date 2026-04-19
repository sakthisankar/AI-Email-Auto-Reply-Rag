import logging  # Logging module
import time  # Delay for retry

logging.basicConfig(
    filename='app.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def retry(func, retries=3, delay=2):
    for attempt in range(retries):
        try:
            return func()
        except Exception as e:
            logging.error(f"Attempt {attempt+1} failed: {str(e)}")
            time.sleep(delay)
    logging.critical("All retry attempts failed")
    return None
