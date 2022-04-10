from order_manager import LocalOrderManager as LOM
import json


try:
    with open("credentials.json", "r") as creds:
        creds = json.load(creds)
except Exception as exception:
    print(f"{exception}: Please create a credential file")
    exit()

order_manager = LOM(creds)
number = 'ptq'
order_manager.increment_done_quantity(number)
order_manager.increment_done_quantity('R2')
order_manager.increment_done_quantity('R2')
order_manager.increment_done_quantity('R2')
while 1:
    # TODO: computer vision Here
    # TODO: AI model Here

    # TODO: Update Local & Remote
    # if predicted_number certainty > x %:
    # order_manager.increment_done_quantity(predicted_number)
    pass