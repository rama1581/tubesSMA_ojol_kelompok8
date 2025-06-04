class Order:
    """
    Representasi order pelanggan.
    Setiap order punya ID unik dan lokasi (random, sebagai simulasi).
    """
    def __init__(self, order_id, location):
        self.order_id = order_id
        self.location = location
