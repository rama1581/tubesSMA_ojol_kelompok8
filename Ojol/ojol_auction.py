from driver import Driver                      # Import class Driver
from dispatcher import Dispatcher              # Import class Dispatcher
from order import Order                        # Import class Order
from utils import evaluasi_tim, statistik_driver, analisis_global  # Import fungsi evaluasi
import random                                 # Import modul random untuk simulasi
from collections import Counter                # Import Counter untuk rekap hasil

# Inisialisasi dua tim, masing-masing terdiri dari dua driver
drivers_team1 = [Driver('D1', 'Team1'), Driver('D2', 'Team1')]     # Driver tim 1
drivers_team2 = [Driver('D3', 'Team2'), Driver('D4', 'Team2')]     # Driver tim 2
all_drivers = drivers_team1 + drivers_team2                        # Gabungkan semua driver

# Buat agent dispatcher untuk masing-masing tim
dispatcher1 = Dispatcher('Team1', drivers_team1)                   # Dispatcher tim 1
dispatcher2 = Dispatcher('Team2', drivers_team2)                   # Dispatcher tim 2

results = []  # List untuk menyimpan hasil simulasi

# --- SIMULASI 3 ORDER: SEMUA DRIVER SAMA ---
def bid_sama(self, order_location):                                # Fungsi bid untuk kondisi semua driver sama
    jarak = 7                                                      # Set nilai jarak tetap
    waktu_respon = 3                                               # Set nilai waktu respon tetap
    skor = 0.6 * jarak + 0.3 * self.beban + 0.1 * waktu_respon     # Hitung skor penawaran
    return skor, self, jarak, self.beban, waktu_respon             # Return hasil bid

# Simpan fungsi bid asli dulu
original_bid = Driver.bid                                          # Simpan fungsi bid asli

# Override fungsi bid pada semua driver untuk simulasi “semua sama” dan set beban awal
for driver in all_drivers:
    driver.bid = bid_sama.__get__(driver, Driver)                  # Override method bid
    driver.beban = 5                                               # Set beban awal = 5

print("\n=== SIMULASI 3 ORDER (SEMUA DRIVER SAMA) ===\n")
for i in range(1, 2):                                              # Jalankan untuk 1 order (bisa diganti jadi 4 kalau mau)
    order = Order(f"O_SIM_{i}", random.randint(1, 20))             # Buat order baru dengan lokasi random
    print(f"--- ORDER {order.order_id} ---")
    winner1 = dispatcher1.koordinasi_order(order)                  # Koordinasi bidding tim 1
    winner2 = dispatcher2.koordinasi_order(order)                  # Koordinasi bidding tim 2

    # Pilih pemenang dari kedua tim
    if winner1[0] < winner2[0]:
        chosen = winner1
        team = dispatcher1.dispatcher_id
    elif winner2[0] < winner1[0]:
        chosen = winner2
        team = dispatcher2.dispatcher_id
    else:
        # Jika skor identik, lakukan global tie-breaker (bid ulang antar dispatcher)
        print("  [Tie-breaker Global] Skor identik, masuk fase bid ulang...")
        all_candidates = [winner1, winner2]
        attempt = 1
        MAX_ATTEMPT = 5
        prev_scores = None

        while True:
            print(f"    [Bid ulang Global #{attempt}]")
            tie_bids = []
            for bid in all_candidates:
                driver = bid[1]
                prev_jarak = bid[2]
                prev_beban = bid[3]
                prev_waktu_respon = bid[4]
                # Pengurangan beban random, jarak dan waktu tetap
                if prev_beban > 0:
                    pengurang = random.randint(1, prev_beban)
                else:
                    pengurang = 0
                simulated_beban = max(0, prev_beban - pengurang)
                new_skor = 0.6 * prev_jarak + 0.3 * simulated_beban + 0.1 * prev_waktu_respon
                tie_bids.append((new_skor, driver, prev_jarak, simulated_beban, prev_waktu_respon))
                print(f"      Driver {driver.driver_id} bid ulang global dengan skor: {new_skor:.2f} (jarak: {prev_jarak}, waktu: {prev_waktu_respon}, beban dikurangi jadi {simulated_beban})")

            skor_list = [t[0] for t in tie_bids]

            # Jika skor stagnan & semua beban habis, pilih random
            if prev_scores == skor_list and all(t[3] == 0 for t in tie_bids):
                print("    Skor tidak berubah dan semua beban minimum. Driver dipilih secara acak.\n")
                chosen = random.choice(tie_bids)
                break

            prev_scores = skor_list

            # Jika sudah MAX_ATTEMPT, acak juga
            if attempt >= MAX_ATTEMPT:
                print(f"    Mencapai batas maksimal bid ulang ({MAX_ATTEMPT}). Driver dipilih secara acak.\n")
                chosen = random.choice(tie_bids)
                break

            # Jika skor sudah beda, pilih skor terkecil dan keluar
            if len(set(skor_list)) > 1:
                chosen = min(tie_bids, key=lambda x: x[0])
                break

            attempt += 1

        # Tentukan pemenang dari tim mana
        team = dispatcher1.dispatcher_id if chosen[1] in dispatcher1.drivers else dispatcher2.dispatcher_id
        print(f"  ==> Driver {chosen[1].driver_id} menang setelah bid ulang (skor: {chosen[0]:.2f})\n")

    print(f"*** Order {order.order_id} dimenangkan oleh {chosen[1].driver_id} dari {team} (skor: {chosen[0]:.2f})\n")
    results.append((order.order_id, team, chosen[1].driver_id, chosen[0]))

# --- KEMBALIKAN FUNGSI BID KE ASLINYA ---
for driver in all_drivers:
    driver.bid = original_bid.__get__(driver, Driver)              # Restore fungsi bid asli
    driver.beban = 0   # Reset beban ke 0 agar fresh

# === SIMULASI 10 ORDER RANDOM SEPERTI KODE ASLI ===
print("\n=== SIMULASI 10 ORDER OJEK ONLINE (AUCTION MULTI AGENT 2 vs 2) ===\n")
for i in range(1, 11):                                             # 10 order random
    order = Order(f"O{i}", random.randint(1, 20))                  # Buat order baru (lokasi random)
    print(f"--- ORDER {order.order_id} ---")
    winner1 = dispatcher1.koordinasi_order(order)                  # Koordinasi bidding tim 1
    winner2 = dispatcher2.koordinasi_order(order)                  # Koordinasi bidding tim 2

    # Tentukan pemenang
    if winner1[0] < winner2[0]:
        chosen = winner1
        team = dispatcher1.dispatcher_id
    elif winner2[0] < winner1[0]:
        chosen = winner2
        team = dispatcher2.dispatcher_id
    else:
        # Tie-breaker global (skor identik)
        print("  [Tie-breaker Global] Skor identik, masuk fase bid ulang...")
        all_candidates = [winner1, winner2]
        attempt = 1
        MAX_ATTEMPT = 5
        prev_scores = None

        while True:
            print(f"    [Bid ulang Global #{attempt}]")
            tie_bids = []
            for bid in all_candidates:
                driver = bid[1]
                prev_jarak = bid[2]
                prev_beban = bid[3]
                prev_waktu_respon = bid[4]
                if prev_beban > 0:
                    pengurang = random.randint(1, prev_beban)
                else:
                    pengurang = 0
                simulated_beban = max(0, prev_beban - pengurang)
                new_skor = 0.6 * prev_jarak + 0.3 * simulated_beban + 0.1 * prev_waktu_respon
                tie_bids.append((new_skor, driver, prev_jarak, simulated_beban, prev_waktu_respon))
                print(f"      Driver {driver.driver_id} bid ulang global dengan skor: {new_skor:.2f} (jarak: {prev_jarak}, waktu: {prev_waktu_respon}, beban dikurangi jadi {simulated_beban})")

            skor_list = [t[0] for t in tie_bids]

            if prev_scores == skor_list and all(t[3] == 0 for t in tie_bids):
                print("    Skor tidak berubah dan semua beban minimum. Driver dipilih secara acak.\n")
                chosen = random.choice(tie_bids)
                break

            prev_scores = skor_list

            if attempt >= MAX_ATTEMPT:
                print(f"    Mencapai batas maksimal bid ulang ({MAX_ATTEMPT}). Driver dipilih secara acak.\n")
                chosen = random.choice(tie_bids)
                break

            if len(set(skor_list)) > 1:
                chosen = min(tie_bids, key=lambda x: x[0])
                break

            attempt += 1

        team = dispatcher1.dispatcher_id if chosen[1] in dispatcher1.drivers else dispatcher2.dispatcher_id
        print(f"  ==> Driver {chosen[1].driver_id} menang setelah bid ulang (skor: {chosen[0]:.2f})\n")

    print(f"*** Order {order.order_id} dimenangkan oleh {chosen[1].driver_id} dari {team} (skor: {chosen[0]:.2f})\n")
    results.append((order.order_id, team, chosen[1].driver_id, chosen[0]))

# # SIMULASI INTERNAL TIE-BREAKER
# print("\n=== SIMULASI 5 ORDER TIE-BREAKER ===\n")
# for i in range(11, 12):
#     order = Order(f"O{i}", 10)
#     print(f"--- ORDER {order.order_id} ---")
#     # Paksa kondisi internal tie
#     for d in dispatcher1.drivers:
#         d.beban = 5  # bikin skor sama
#     winner1 = dispatcher1.koordinasi_order(order)
#     winner2 = dispatcher2.koordinasi_order(order)
#     chosen = winner1
#     team = dispatcher1.dispatcher_id
#     print(f"*** Order {order.order_id} dimenangkan oleh {chosen[1].driver_id} dari {team} (skor: {chosen[0]:.2f})\n")
#     results.append((order.order_id, team, chosen[1].driver_id, chosen[0]))

# # SIMULASI GLOBAL TIE-BREAKER (2 Dispatcher, hasil sama)
# print("\n=== SIMULASI 5 ORDER GLOBAL TIE-BREAKER (Skor Identik antar Dispatcher) ===\n")

# for i in range(16, 21):
#     order = Order(f"O{i}", 10)
#     print(f"--- ORDER {order.order_id} ---")
#     winner1 = dispatcher1.koordinasi_order(order)
#     winner2 = dispatcher2.koordinasi_order(order)

#     if winner1[0] < winner2[0]:
#         chosen = winner1
#         team = dispatcher1.dispatcher_id
#     elif winner2[0] < winner1[0]:
#         chosen = winner2
#         team = dispatcher2.dispatcher_id
#     else:
#         print("  [Tie-breaker Global] Skor identik, masuk fase bid ulang...")
#         all_candidates = [winner1, winner2]
#         attempt = 1
#         MAX_ATTEMPT = 5
#         prev_scores = None

#         while True:
#             print(f"    [Bid ulang Global #{attempt}]")
#             tie_bids = []
#             for bid in all_candidates:
#                 driver = bid[1]
#                 prev_jarak = bid[2]
#                 prev_beban = bid[3]
#                 prev_waktu_respon = bid[4]
#                 simulated_beban = max(0, prev_beban - attempt)
#                 new_skor = 0.6 * prev_jarak + 0.3 * simulated_beban + 0.1 * prev_waktu_respon
#                 tie_bids.append((new_skor, driver, prev_jarak, simulated_beban, prev_waktu_respon))
#                 print(f"      Driver {driver.driver_id} bid ulang global dengan skor: {new_skor:.2f} (jarak: {prev_jarak}, waktu: {prev_waktu_respon}, beban dikurangi jadi {simulated_beban})")

#             skor_list = [t[0] for t in tie_bids]

#             if prev_scores == skor_list and all(t[3] == 0 for t in tie_bids):
#                 print("    Skor tidak berubah dan semua beban minimum. Driver dipilih secara acak.\n")
#                 chosen = random.choice(tie_bids)
#                 break

#             prev_scores = skor_list

#             if attempt >= MAX_ATTEMPT:
#                 print(f"    Mencapai batas maksimal bid ulang ({MAX_ATTEMPT}). Driver dipilih secara acak.\n")
#                 chosen = random.choice(tie_bids)
#                 break

#             if len(set(skor_list)) > 1:
#                 chosen = min(tie_bids, key=lambda x: x[0])
#                 break

#             attempt += 1

#         team = dispatcher1.dispatcher_id if chosen[1] in dispatcher1.drivers else dispatcher2.dispatcher_id
#         print(f"  ==> Driver {chosen[1].driver_id} menang setelah bid ulang (skor: {chosen[0]:.2f})\n")

#     print(f"*** Order {order.order_id} dimenangkan oleh {chosen[1].driver_id} dari {team} (skor: {chosen[0]:.2f})\n")
#     results.append((order.order_id, team, chosen[1].driver_id, chosen[0]))

# --- Rekap distribusi order per tim ---
print("\n=== Distribusi order antar tim ===")
team_count = Counter([r[1] for r in results])
print(dict(team_count), "\n")

# Evaluasi performa tiap tim
evaluasi_tim(dispatcher1, "Team 1")
evaluasi_tim(dispatcher2, "Team 2")

print("=== Statistik Tiap Driver ===")
statistik_driver(all_drivers)

analisis_global(results, all_drivers)

print("=== SIMULASI SELESAI ===\n")
