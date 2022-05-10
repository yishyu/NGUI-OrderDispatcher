from order_manager import LocalOrderManager as LOM
import json
from ID_recognition import capture_id
import time
import logging
from LED import LEDManager
logging.getLogger().setLevel(logging.INFO)

CREDS_PATH = "./memory/creds"
try:
    with open(f"{CREDS_PATH}/credentials.json", "r") as creds:
        creds = json.load(creds)
except Exception as exception:
    logging.error(f"{exception}: Please create a credential file")
    exit()

led_manager = LEDManager()
order_manager = LOM(creds, led_manager)

logging.debug("order_manager initiated ...")
while 1:
    number = capture_id()
    # number = input('Identifier : ').strip()
    order_manager.increment_done_quantity(number)
    print(number)
    time.sleep(2)

