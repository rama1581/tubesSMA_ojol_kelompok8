import random  # Import modul random untuk simulasi pengacakan beban

class Dispatcher:
    """
    Agent dispatcher (admin/tim).
    Mengelola 2 driver, menerima order, melakukan bidding internal,
    dan menyimpan log order yang dimenangkan tim ini.
    """

    def __init__(self, dispatcher_id, drivers):
        # Inisialisasi Dispatcher dengan ID (nama tim) dan daftar driver pada tim ini
        self.dispatcher_id = dispatcher_id  # Contoh: "Team1" atau "Team2"
        self.drivers = drivers              # List berisi objek Driver
        self.order_log = []                 # Log seluruh order yang dimenangkan tim ini

    def koordinasi_order(self, order):
        """
        Proses koordinasi internal bidding dalam satu tim:
        1. Dispatcher menerima order baru dan membroadcast ke seluruh driver dalam tim.
        2. Semua driver melakukan bid (menghitung skor_penawaran masing-masing).
        3. Jika ada satu driver dengan skor terendah → langsung assign order ke driver itu.
        4. Jika ada dua driver atau lebih dengan skor identik (tie) → dilakukan tie-breaker (bid ulang).
           Pada tie-breaker, hanya beban yang boleh berkurang secara acak, jarak dan waktu tetap!
           Jika setelah beberapa kali bid ulang tetap tie, pemenang dipilih secara acak.
        5. Setelah pemenang bidding didapat, assign order ke driver, update beban dan catat log.
        """
        print(f"[Dispatcher {self.dispatcher_id}] menerima order {order.order_id}")  # Cetak info penerimaan order oleh dispatcher
        bids = []  # List untuk menampung hasil bid driver

        # 1. Setiap driver melakukan bid terhadap order ini
        for driver in self.drivers:
            bid = driver.bid(order.location)  # Driver melakukan bid untuk order ini
            bids.append(bid)  # Simpan hasil bid
            print(f"  Driver {driver.driver_id} skor_penawaran: {bid[0]:.2f} (Jarak: {bid[2]}, Beban: {bid[3]}, Waktu: {bid[4]})")

        # 2. Cari skor penawaran terkecil di antara semua driver
        min_skor = min(bids, key=lambda x: x[0])[0]  # Ambil nilai skor terkecil dari semua bid
        kandidat = [bid for bid in bids if bid[0] == min_skor]  # List kandidat pemenang (bisa 1 atau lebih)

        # 3. Jika terjadi tie (lebih dari satu driver dengan skor sama), lakukan bid ulang/tie-breaker
        if len(kandidat) > 1:
            print(f"  [Tie-breaker internal] {len(kandidat)} driver memiliki skor identik.")

            attempt = 1
            MAX_ATTEMPT = 5  # Batas maksimal bid ulang supaya tidak infinite loop
            prev_scores = None  # Untuk mendeteksi jika skor stagnan

            while True:
                print(f"    [Bid ulang #{attempt}]")
                tie_bids = []  # List untuk hasil bid ulang
                for bid in kandidat:
                    driver = bid[1]              # Ambil objek driver dari bid
                    prev_jarak = bid[2]          # Ambil jarak dari bid awal (TETAP)
                    prev_beban = bid[3]          # Ambil beban dari bid awal
                    prev_waktu_respon = bid[4]   # Ambil waktu respon dari bid awal (TETAP)

                    # Pengurangan beban secara acak pada tiap bid ulang, minimal 1, maksimal sisa beban
                    if prev_beban > 0:
                        pengurang = random.randint(1, prev_beban)
                    else:
                        pengurang = 0
                    simulated_beban = max(0, prev_beban - pengurang)  # Pastikan tidak negatif

                    # Skor baru dihitung dengan beban terbaru, jarak dan waktu tetap dari bid awal
                    new_skor = 0.6 * prev_jarak + 0.3 * simulated_beban + 0.1 * prev_waktu_respon

                    tie_bids.append((new_skor, driver, prev_jarak, simulated_beban, prev_waktu_respon))
                    print(f"      Driver {driver.driver_id} bid ulang dengan skor: {new_skor:.2f} (jarak: {prev_jarak}, waktu: {prev_waktu_respon}, beban awal: {prev_beban}, pengurang: {pengurang}, sisa beban: {simulated_beban})")

                # 4. Cek apakah skor stagnan & semua beban sudah minimum (0)
                skor_list = [t[0] for t in tie_bids]  # Ambil semua skor bid ulang
                if prev_scores == skor_list and all(t[3] == 0 for t in tie_bids):
                    print("    Skor tidak berubah dan semua beban minimum. Driver dipilih secara acak.\n")
                    winner = random.choice(tie_bids)  # Pilih pemenang secara acak
                    break

                prev_scores = skor_list

                # Jika sudah MAX_ATTEMPT, paksa acak juga
                if attempt >= MAX_ATTEMPT:
                    print(f"    Mencapai batas maksimal bid ulang ({MAX_ATTEMPT}). Driver dipilih secara acak.\n")
                    winner = random.choice(tie_bids)
                    break

                # Jika setelah bid ulang skor sudah berbeda, pilih pemenang dengan skor terendah dan keluar loop
                if len(set(skor_list)) > 1:
                    break

                attempt += 1

            # Jika belum ada winner (skor sudah beda), ambil yang terkecil
            if 'winner' not in locals():
                winner = min(tie_bids, key=lambda x: x[0])
        else:
            # Tidak terjadi tie, pemenang langsung
            winner = kandidat[0]

        # 5. Assign order ke driver pemenang, update beban dan statistik, catat di order_log
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
        return winner  # Return hasil pemenang bidding

