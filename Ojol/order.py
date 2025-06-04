class Order:
    """
    Representasi order pelanggan.
    Setiap order punya id dan lokasi (simulasi: random).
    """
    def __init__(self, order_id, location):
        self.order_id = order_id
        self.location = location
