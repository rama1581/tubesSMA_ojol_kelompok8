import random

class Dispatcher:
    """
    Agent dispatcher (admin/tim).
    Mengelola 2 driver, menerima order, melakukan bidding internal,
    dan menyimpan log order yang dimenangkan tim ini.
    """

    def __init__(self, dispatcher_id, drivers):
        self.dispatcher_id = dispatcher_id  # ID tim (Team1, Team2)
        self.drivers = drivers              # List driver di tim ini
        self.order_log = []                 # Log seluruh order yang dimenangkan tim ini

    def koordinasi_order(self, order):
        """
        Proses koordinasi:
        1. Dispatcher menerima order dan broadcast ke drivernya
        2. Semua driver melakukan bid (skor_penawaran)
        3. Jika satu pemenang → assign langsung
        4. Jika dua driver punya skor identik → tie-breaker internal
        5. Assign driver, update beban, dan catat log
        """
        print(f"[Dispatcher {self.dispatcher_id}] menerima order {order.order_id}")
        bids = []

        for driver in self.drivers:
            bid = driver.bid(order.location)
            bids.append(bid)
            print(f"  Driver {driver.driver_id} skor_penawaran: {bid[0]:.2f} (Jarak: {bid[2]}, Beban: {bid[3]}, Waktu: {bid[4]})")

        # Ambil skor terkecil
        min_skor = min(bids, key=lambda x: x[0])[0]
        kandidat = [bid for bid in bids if bid[0] == min_skor]

        if len(kandidat) > 1:
            print(f"  [Tie-breaker internal] {len(kandidat)} driver memiliki skor identik.")

            attempt = 1
            MAX_ATTEMPT = 5  # batas maksimal bid ulang
            prev_scores = None  # simpan skor sebelumnya

            while True:
                print(f"    [Bid ulang #{attempt}]")
                tie_bids = []
                for bid in kandidat:
                    driver = bid[1]
                    # Hitung ulang jarak dan waktu respon berdasarkan lokasi order
                    jarak, waktu_respon = driver.hitung_jarak_dan_waktu(order.location)
                    
                    # Simulasikan pengurangan beban tiap bid ulang
                    simulated_beban = max(0, driver.beban - attempt)

                    # Hitung skor baru
                    new_skor = 0.6 * jarak + 0.3 * simulated_beban + 0.1 * waktu_respon

                    tie_bids.append((new_skor, driver, jarak, simulated_beban, waktu_respon))
                    print(f"      Driver {driver.driver_id} bid ulang dengan skor: {new_skor:.2f} (jarak: {jarak}, waktu: {waktu_respon}, beban dikurangi jadi {simulated_beban})")

                skor_list = [t[0] for t in tie_bids]

                # Jika skor stagnan dan semua beban sudah minimum, pilih random
                if prev_scores == skor_list and all(t[3] == 0 for t in tie_bids):
                    print("    Skor tidak berubah dan semua beban minimum. Driver dipilih secara acak.\n")
                    winner = random.choice(tie_bids)
                    break

                prev_scores = skor_list

                # Jika mencapai batas maksimal bid ulang, pilih random
                if attempt >= MAX_ATTEMPT:
                    print(f"    Mencapai batas maksimal bid ulang ({MAX_ATTEMPT}). Driver dipilih secara acak.\n")
                    winner = random.choice(tie_bids)
                    break

                # Jika skor sudah berbeda, keluar dari loop
                if len(set(skor_list)) > 1:
                    break

                attempt += 1

            if 'winner' not in locals():
                winner = min(tie_bids, key=lambda x: x[0])
        else:
            winner = kandidat[0]


        driver = winner[1]
        driver.assign_order(winner[0], winner[4], order.order_id, winner[2])

        self.order_log.append({
            "order_id": order.order_id,
            "driver_id": driver.driver_id,
            "skor": winner[0],
            "jarak": winner[2],
            "beban": driver.beban,
            "waktu_respon": winner[4]
        })

        print(f"  ==> Order {order.order_id} diberikan ke Driver {driver.driver_id} (skor: {winner[0]:.2f})\n")
        return winner
