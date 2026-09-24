import logging
import os


# Create logs folder if it doesn't exist
os.makedirs(
    "logs",
    exist_ok=True
)

# Configure logging
logging.basicConfig(
    filename="logs/audit.log",
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)


def write_log(message):

    print(message)

    logging.info(message)