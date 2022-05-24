from order_manager import LocalOrderManager as LOM
import json
from ID_recognition import capture_id
import time
import logging
from LED import LEDManager
logging.getLogger().setLevel(logging.INFO)

CREDS_PATH = "./memory/creds"

"""
    set up the application credentials containing the remote server url-port
    the api key and some parameters for the local app
"""
try:
    with open(f"{CREDS_PATH}/credentials.json", "r") as creds:
        creds = json.load(creds)
except Exception as exception:
    logging.error(f"{exception}: Please create a credential file")
    exit()

led_manager = LEDManager()  # creation of the led manager
order_manager = LOM(creds, led_manager)  # creation of the local order manager

logging.debug("order_manager initiated ...")
while 1:
    number = capture_id()  # scanning the box
    order_manager.increment_done_quantity(number)  # updating the orders
    time.sleep(2)  # wait for 2 seconds before scanning again

