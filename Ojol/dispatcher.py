class Dispatcher:
    """
    Agent dispatcher (admin/tim).
    Mengelola 2 driver, menerima order, melakukan bidding internal,
    dan menyimpan log order yang dimenangkan tim ini.
    """

    def __init__(self, dispatcher_id, drivers):
        # ID tim (Team1, Team2)
        self.dispatcher_id = dispatcher_id
        # List driver di tim ini
        self.drivers = drivers
        # Log seluruh order yang dimenangkan tim ini
        self.order_log = []

    def koordinasi_order(self, order):
        """
        Proses:
        1. Dispatcher menerima order dan mengumumkan ke driver di timnya
        2. Semua driver melakukan bid (skor_penawaran)
        3. Driver dengan skor terkecil di tim ini dipilih
        4. Driver tersebut assign order (beban bertambah)
        5. Log order tim diperbarui
        """
        print(f"[Dispatcher {self.dispatcher_id}] menerima order {order.order_id}")
        bids = []
        for driver in self.drivers:
            bid = driver.bid(order.location)
            bids.append(bid)
            print(f"  Driver {driver.driver_id} skor_penawaran: {bid[0]:.2f} (Jarak: {bid[2]}, Beban: {bid[3]}, Waktu: {bid[4]})")
        # Pilih driver dengan skor terkecil di tim ini
        winner = min(bids, key=lambda x: x[0])
        # Assign order ke driver yang menang (beban bertambah di class Driver)
        winner[1].assign_order(winner[0], winner[4], order.order_id, winner[2])
        # Catat log di dispatcher (untuk statistik tim)
        self.order_log.append({
            "order_id": order.order_id,
            "driver_id": winner[1].driver_id,
            "skor": winner[0],
            "jarak": winner[2],
            "beban": winner[1].beban,
            "waktu_respon": winner[4]
        })
        print(f"  ==> Order {order.order_id} diberikan ke Driver {winner[1].driver_id} (skor: {winner[0]:.2f})\n")
        return winner
