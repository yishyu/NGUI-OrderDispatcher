from remote_order_manager import RemoteOrderManager as ROM
import threading
import logging

class Order():
    """
        Local representation of an order
        It stores the whole payload received from through the api
        The getter allows access in the payload
    """
    def __init__(self, order: dict):
        self._order = order

    def get_id(self):
        return self._order['pk']

    def get_color(self):
        return self._order['color']['name']

    def get_color_hex(self):
        return self._order['color']['hex_or_rgba']

    def get_position(self):
        return self._order['color']['position']

    def find_dish(self, number):
        """
            Checks if a certain dish is in the order
            Updates its finished quantity if it exists
        """
        for dish in self._order['dishes']:
            if dish['dish']['identifier'] == number and not dish['done']:
                dish['quantity_done'] += 1
                dish['quantity_left'] = dish['quantity'] - dish['quantity_done']
                dish['done'] = dish['quantity_left'] == 0
                return True
        return False

    def done(self):
        for dish in self._order['dishes']:
            if not dish['done']:
                return False
        return True

class LocalOrderManager():
    def __init__(self, creds, led_manager):
        self._led_manager = led_manager
        self._creds = creds
        # create the remote order manager
        self._remote_order_manager = ROM(creds["remote_url"], creds["shop_key"], creds["remote_port"]) if creds.get("remote_port", "") != "" else ROM(creds["remote_url"], creds["shop_key"])
        self._done_orders = []
        self._preparing_orders = []
        self._thread_launched = False
        for order in self._remote_order_manager.get_preparing_orders():  # in case the app crashes with unfinished preparing orders
            self._preparing_orders.append(Order(order))
        self.pull_new_orders()  # fetches new orders


    def find_update_order(self, number):
        """
            Finds an order containing this dish
        """
        for order in self._preparing_orders:
            if order.find_dish(number):
                return order


    def pull_new_orders(self):
        """
            Fetches new orders if the current preparing orders amount is less than
            the amount set in the credentials
        """
        amount = self._creds["order_amount"]-len(self._preparing_orders)
        if amount > 0:
            new_orders = self._remote_order_manager.get_new_orders(amount)
            for order in new_orders:
                self._preparing_orders.append(Order(order))
            if len(self._preparing_orders) < self._creds["order_amount"]:
                self._thread_launched = True
                threading.Timer(self._creds["request_delay"], self.pull_new_orders).start()  # launch a new thread to fetch the orders

    def terminate_order(self, order_id):
        """
            Move the finished order locally
        """
        for order in self._preparing_orders:
            if order.get_id() == order_id:
                self._preparing_orders.remove(order)
                self._done_orders.append(order)
                break

    def increment_done_quantity(self, number):
        """
            Main logic of the localOrderManager
        """
        # find order where the dish is located in
        # update local order
        order = self.find_update_order(number)
        if not order:
            logging.warning("Dish Not in any preparing order")
        else:
            order_id = order.get_id()
            # update the remote order by calling self._remote_order_manager
            self._remote_order_manager.increment_done_quantity(order_id, number)
            # Light up the corresponding LED TODO
            self._led_manager.light_up_led(order.get_color_hex(), order.get_position())
            if order.done():
                logging.info("order is done !")
                for i in range(5):
                    self._led_manager.light_up_led(order.get_color_hex(), order.get_position())

                # 1) move local order from preparing_orders to _done_orders
                self.terminate_order(order_id)
                # 2) update the remote order
                self._remote_order_manager.finish_order(order_id)
                # 3) pull a new order
                if not self._thread_launched:
                    self.pull_new_orders()

    def __str__(self):
        return f"LocalOrderManager having {len(self._preparing_orders)} preparing orders"