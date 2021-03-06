import requests
import json


class RemoteOrderManager():
    def __init__(self, url, key, port=""):
        self._url = url
        self._port = port
        self._key = key
    @property
    def formatted_url(self):
        """
            sets the url dynamically
        """
        if self._port != "":
            return f"http://{self._url}:{self._port}"
        else:
            return f"https://{self._url}"

    def request_get_data(self, path, payload={}):
        """
            generic method to get data from the remote server
        """
        try:
            payload["key"] = self._key
            data = requests.get(self.formatted_url+path, json=json.dumps(payload)).json()
        except:
            data = []  # empty data if the request fails
        return data

    def request_post_data(self, path, payload={}):
        """
            generic method to post data to the remote server
        """
        try:
            payload["key"] = self._key
            data = requests.post(self.formatted_url+path, json=json.dumps(payload)).json()
        except:
            data = []
        return data

    def get_preparing_orders(self):
        return self.request_get_data("/api/kitchen_display/getcurrentpreparingorders")

    def get_new_orders(self, amount: int):
        return self.request_get_data("/api/kitchen_display/getqueuedorders", {"amount": amount})

    def finish_order(self, order_id: int):
        return self.request_post_data("/api/kitchen_display/changeStateToDone", {"order": order_id})

    def increment_done_quantity(self, order_id, dish_identifier):
        return self.request_post_data("/api/kitchen_display/incrementdonequantity", {"order": [order_id, dish_identifier]})

    def __str__(self):
        return self.formatted_url

if __name__ == "__main__":
    manager = RemoteOrderManager("192.168.1.48", "8000")
    print(manager)