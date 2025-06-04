import random

class Driver:
    """
    Representasi agent pengemudi/driver ojol.
    Memiliki atribut id, tim, beban, log order, dan method bid (tawar order).
    Beban driver akan bertambah setiap menerima order (tidak direset setiap order).
    """
    def __init__(self, driver_id, team):
        self.driver_id = driver_id
        self.team = team
        self.beban = 0
        self.total_order = 0
        self.total_skor = 0
        self.total_waktu_respon = 0
        self.log_order = []

    def bid(self, order_location):
        """
        Melakukan penawaran (bidding) untuk order baru.
        Skor dihitung berdasarkan jarak, beban (REAL-TIME), dan waktu respon.
        """
        jarak = random.randint(1, 10)
        waktu_respon = random.randint(1, 5)
        skor = self.hitung_skor_penawaran(jarak, waktu_respon)
        return skor, self, jarak, self.beban, waktu_respon

    def hitung_skor_penawaran(self, jarak, waktu_respon):
        """
        Rumus scoring: skor_penawaran = 0.6*jarak + 0.3*beban + 0.1*waktu_respon
        """
        return 0.6 * jarak + 0.3 * self.beban + 0.1 * waktu_respon

    def assign_order(self, skor, waktu_respon, order_id, jarak):
        """
        Dipanggil saat driver menang bidding dan dapat order.
        Beban bertambah 1.
        Data order disimpan untuk statistik/analisis.
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
