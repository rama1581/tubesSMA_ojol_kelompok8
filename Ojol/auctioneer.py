class Auctioneer:
    def __init__(self, order_id, base_price):
        self.product_id = order_id
        self.base_price = base_price  # harga dasar order

    def announce_order(self):
        print(f"Auctioneer announces order {self.product_id} with base price {self.base_price}")
