class Dispatcher:
    """
    Agent dispatcher (admin), mewakili satu tim (2 driver).
    Menerima order, melakukan koordinasi internal dengan driver di tim-nya.
    Menyimpan log order yang dimenangkan timnya.
    """
    def __init__(self, dispatcher_id, drivers):
        self.dispatcher_id = dispatcher_id
        self.drivers = drivers
        self.order_log = []

    def koordinasi_order(self, order):
        """
        Mengumumkan order ke driver di tim ini, semua driver bid.
        Order diberikan ke driver dengan skor penawaran terendah.
        """
        print(f"[Dispatcher {self.dispatcher_id}] menerima order {order.order_id}")
        bids = []
        for driver in self.drivers:
            bid = driver.bid(order.location)
            bids.append(bid)
            print(f"  Driver {driver.driver_id} skor_penawaran: {bid[0]:.2f} (Jarak: {bid[2]}, Beban: {bid[3]}, Waktu: {bid[4]})")
        # Pilih driver dengan skor terkecil
        winner = min(bids, key=lambda x: x[0])
        # Assign order ke driver yang menang (beban bertambah di sini)
        winner[1].assign_order(winner[0], winner[4], order.order_id, winner[2])
        # Catat log di dispatcher
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
