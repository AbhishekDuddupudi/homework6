# main.py
import os
import logging
import logging.config
from dotenv import load_dotenv

# Import your REPL app
from app.app import App

def setup_logging():

    if os.path.isfile("logging.conf"):
        logging.config.fileConfig("logging.conf", disable_existing_loggers=False)
        logging.info("Loaded logging configuration from logging.conf.")
    else:
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
        )
        logging.info("No logging.conf found. Using basicConfig instead.")

def main():
    # 1) Load environment variables
    load_dotenv()  # loads from .env by default
    env_name = os.getenv("ENV_NAME", "unknown-env")
    log_level = os.getenv("LOG_LEVEL", "INFO")

    # 2) Configure logging
    setup_logging()
    logger = logging.getLogger(__name__)
    logger.setLevel(log_level)

    # 3) Log environment
    logger.info("Starting Calculator REPL in environment: %s", env_name)

    # 4) Start the application
    App.start()

if __name__ == "__main__":
    main()
