from remote_order_manager import RemoteOrderManager as ROM
import threading


class Order():
    def __init__(self, order: dict):
        self._order = order

    def get_id(self):
        return self._order['pk']

    def find_dish(self, number):
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
    def __init__(self, creds):
        self._creds = creds
        self._remote_order_manager = ROM(creds["remote_url"], creds["remote_port"], creds["shop_key"])
        self._done_orders = []
        self._preparing_orders = []
        self._thread_launched = False
        for order in self._remote_order_manager.get_preparing_orders():
            print(order)
            self._preparing_orders.append(Order(order))
        self.pull_new_orders()


    def find_update_order(self, number):
        for order in self._preparing_orders:
            if order.find_dish(number):
                return order.get_id(), order.done()
        return -1, False


    def pull_new_orders(self):
        amount = self._creds["order_amount"]-len(self._preparing_orders)
        print(f"Fetching {amount} new orders")
        if amount > 0:
            for order in self._remote_order_manager.get_new_orders(amount):
                self._preparing_orders.append(Order(order))
            if len(self._preparing_orders) < self._creds["order_amount"]:
                self._thread_launched = True
                threading.Timer(10, self.pull_new_orders).start()

    def terminate_order(self, order_id):
        for order in self._preparing_orders:
            if order.get_id() == order_id:
                self._preparing_orders.remove(order)
                self._done_orders.append(order)
                break

    def increment_done_quantity(self, number):
        # find order where the dish is located in
        # update local order
        order_id, order_done = self.find_update_order(number)
        if order_id == -1:
            print("Dish Not in any preparing order")
        else:
            print("Incremented dish")

            # update the remote order by calling self._remote_order_manager
            self._remote_order_manager.increment_done_quantity(order_id, number)
            if order_done:
                print("order is done !")
                # 1) move local order from preparing_orders to _done_orders
                self.terminate_order(order_id)
                # 2) update the remote order
                self._remote_order_manager.finish_order(order_id)
                # 3) pull a new order
                if not self._thread_launched:
                    self.pull_new_orders()

    def __str__(self):
        return f"LocalOrderManager having {len(self._preparing_orders)} preparing orders"