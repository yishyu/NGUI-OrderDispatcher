import requests
import json
import time


def neworders():
    """
        Syncronizes the orders from the restaurant online ordering platform
        into our dispatcher database
    """
    # source_url = 'http://127.0.0.1:8000/api/orders/getshoporders'
    # source_shop_key = '766d486752d4d39ab7e3712d8b0132f745b3f1ccf17b97775d7429db0fe0e480'
    source_url = 'https://dev.chifuri.be/api/orders/getshoporders'
    source_shop_key = 'ub9e69fc6cdbce99f3155f596fb7147ce438a0854c63f927a434c2cb270243e16'

    target_url = "http://127.0.0.1:8000/api/kitchen_display/addneworders"
    target_shop_key = "JzCH8aWmZDmigAp7eXJ2456LHQYXK9NKdwwHeWbwhkFfTCEhPcETfffwHbMXRJ6yfquYw2T7Dtv6y"
    # target_url = 'https://orderdispatcher.chifuri.be/api/kitchen_display/addneworders'
    # target_shop_key = 'GKmkLecS9oWGCC5jzUFZavLUnYen9SNCAckKe3M6RCS5zJ7AhwGosXbB9hCc2heV'
    json_obj = {"key": source_shop_key}
    data = requests.get(source_url, json=json.dumps(json_obj))
    data = data.json()
    data["key"] = target_shop_key
    requests.post(target_url, json=json.dumps(data))
    return len(data["online"])


while True:
    print("Starting Sync ...")
    nb_orders = neworders()
    print(f"Synced {nb_orders} order(s) so far !")
    time.sleep(5)
