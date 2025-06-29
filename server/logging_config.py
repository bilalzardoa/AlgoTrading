# logging_config.py
import logging
import os

# Bepaal de absolute pad naar de logs-directory, relatief t.o.v. dit bestand
BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # bv. .../server/
LOG_DIR = os.path.join(BASE_DIR, "..", "logs")
LOG_FILE = os.path.join(LOG_DIR, "trading.log")

# Zorg dat de logs-map bestaat
os.makedirs(LOG_DIR, exist_ok=True)

# Configureer logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE),
        # logging.StreamHandler()  # optioneel: ook naar console
    ]
)
