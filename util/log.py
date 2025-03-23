import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(message)s",
    handlers=[
        logging.FileHandler("./data/app.log"),
        logging.StreamHandler() 
    ]
)

log = logging.getLogger("app_logger")