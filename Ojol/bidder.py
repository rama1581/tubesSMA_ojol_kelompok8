import random

class Bidder:
    def __init__(self, order_id, price_ceiling, bank_capacity, will_power):
        self.order_id = order_id
        self.price_ceiling = price_ceiling  # max driver mau bayar ongkos atau max harga yg dia terima
        self.bank_capacity = bank_capacity  # kemampuan finansial driver (misal saldo)
        self.will_power = will_power        # motivasi/bid power driver
        self.driver_id = id(self)           # unik id untuk driver (bisa diganti)

    def interact(self, content, auction_type, price, protocol, agent_id=None):
        # content contoh: "harga:jarak:auction_type:protocol"
        price = int(price)
        distance = random.randint(1, 10)  # misal jarak random km (bisa diganti dgn input nyata)
        # driver bid harga berdasarkan price_ceiling dan will_power, jarak bisa pengaruh harga
        bid_price = max(price - self.will_power * 10, 0)

        # driver hanya bisa bid jika masih mampu bayar ongkos dan jarak masuk akal
        if bid_price <= self.price_ceiling and bid_price <= self.bank_capacity:
            print(f"Driver {self.driver_id} bids {bid_price} for order {self.order_id} (distance {distance}km)")
            return [bid_price, self]
        else:
            print(f"Driver {self.driver_id} skips bidding for order {self.order_id}")
            return [float('inf'), self]  # gak bid, dianggap bid tak terbatas

    def notify_win(self, content):
        print(f"Driver {self.driver_id} notified of winning: {content}")
