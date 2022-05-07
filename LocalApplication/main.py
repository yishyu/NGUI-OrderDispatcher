from order_manager import LocalOrderManager as LOM
import json
from ID_recognition import capture_id
import time
import logging
logging.getLogger().setLevel(logging.INFO)

try:
    with open("credentials.json", "r") as creds:
        creds = json.load(creds)
except Exception as exception:
    logging.error(f"{exception}: Please create a credential file")
    exit()

order_manager = LOM(creds)
logging.debug("order_manager initiated ...")
while 1:
    number = capture_id()
    # number = input('Identifier : ').strip()
    order_manager.increment_done_quantity(number)
    print(number)
    time.sleep(2)

