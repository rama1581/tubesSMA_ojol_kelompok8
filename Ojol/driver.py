import random

class Driver:
    """
    Representasi agent pengemudi (driver) ojol.
    Setiap driver menyimpan id, tim, beban, dan statistik order.
    """

    def __init__(self, driver_id, team):
        # ID unik driver (misal D1, D2, dst)
        self.driver_id = driver_id
        # Nama tim (Team1, Team2)
        self.team = team
        # Beban order yang sedang/historis ditangani (bertambah jika menang order)
        self.beban = 0
        # Statistik total order, skor, dan waktu respon
        self.total_order = 0
        self.total_skor = 0
        self.total_waktu_respon = 0
        # List untuk mencatat semua order yang dimenangkan
        self.log_order = []

    def bid(self, order_location):
        """
        Simulasi driver menerima order dan melakukan bidding (penawaran skor).
        - jarak: random (simulasi)
        - waktu respon: random (simulasi)
        - beban: real-time (sudah sesuai order yang dimenangkan sebelumnya)
        """
        jarak = random.randint(1, 10)
        waktu_respon = random.randint(1, 5)
        skor = self.hitung_skor_penawaran(jarak, waktu_respon)
        return skor, self, jarak, self.beban, waktu_respon

    def hitung_skor_penawaran(self, jarak, waktu_respon):
        """
        Hitung skor penawaran driver berdasarkan proposal:
        skor_penawaran = 0.6 * jarak + 0.3 * beban + 0.1 * waktu_respon
        """
        return 0.6 * jarak + 0.3 * self.beban + 0.1 * waktu_respon

    def assign_order(self, skor, waktu_respon, order_id, jarak):
        """
        Dipanggil ketika driver menang bidding (mendapat order).
        - Beban bertambah satu
        - Statistik dan log order diperbarui
        """
        self.beban += 1
        self.total_order += 1
        self.total_skor += skor
        self.total_waktu_respon += waktu_respon
        self.log_order.append({
            "order_id": order_id,
            "skor": skor,
            "jarak": jarak,
            "beban": self.beban,
            "waktu_respon": waktu_respon
        })
