from driver import Driver
from dispatcher import Dispatcher
from order import Order
from utils import evaluasi_tim, statistik_driver, analisis_global
import random
from collections import Counter

# Inisialisasi dua tim, masing-masing terdiri dari dua driver
drivers_team1 = [Driver('D1', 'Team1'), Driver('D2', 'Team1')]
drivers_team2 = [Driver('D3', 'Team2'), Driver('D4', 'Team2')]
all_drivers = drivers_team1 + drivers_team2

# Buat agent dispatcher untuk masing-masing tim
dispatcher1 = Dispatcher('Team1', drivers_team1)
dispatcher2 = Dispatcher('Team2', drivers_team2)

# Simpan semua hasil
results = []

print("\n=== SIMULASI 10 ORDER OJEK ONLINE (AUCTION MULTI AGENT 2 vs 2) ===\n")
for i in range(1, 11):
    order = Order(f"O{i}", random.randint(1, 20))
    print(f"--- ORDER {order.order_id} ---")
    winner1 = dispatcher1.koordinasi_order(order)
    winner2 = dispatcher2.koordinasi_order(order)

    if winner1[0] < winner2[0]:
        chosen = winner1
        team = dispatcher1.dispatcher_id
    elif winner2[0] < winner1[0]:
        chosen = winner2
        team = dispatcher2.dispatcher_id
    else:
        print("  [Tie-breaker Global] Skor identik, masuk fase bid ulang...")
        all_candidates = [winner1[1], winner2[1]]
        tie_bids = []

        bid_count = 0
        while True:
            tie_bids.clear()
            bid_count += 1
            print(f"    [Bid ulang #{bid_count}]")
            for driver in all_candidates:
                simulated_beban = max(0, driver.beban - 1)
                jarak = 5
                waktu_respon = 5
                skor = 0.6 * jarak + 0.3 * simulated_beban + 0.1 * waktu_respon
                tie_bids.append((skor, driver))
                print(f"      Driver {driver.driver_id} bid ulang dengan skor: {skor:.2f} (beban dikurangi jadi {simulated_beban})")
            
            min_score = min(tie_bids, key=lambda x: x[0])[0]
            best_bidders = [tb for tb in tie_bids if tb[0] == min_score]
            if len(best_bidders) == 1:
                chosen = best_bidders[0]
                break
            elif all(b[1].beban == 0 for b in best_bidders):
                chosen = random.choice(best_bidders)
                print("    [Dipilih secara acak karena skor & beban identik]")
                break

        team = dispatcher1.dispatcher_id if chosen[1] in dispatcher1.drivers else dispatcher2.dispatcher_id
        print(f"  ==> Driver {chosen[1].driver_id} menang setelah bid ulang (skor: {chosen[0]:.2f})\n")

    print(f"*** Order {order.order_id} dimenangkan oleh {chosen[1].driver_id} dari {team} (skor: {chosen[0]:.2f})\n")
    results.append((order.order_id, team, chosen[1].driver_id, chosen[0]))

# SIMULASI INTERNAL TIE-BREAKER
print("\n=== SIMULASI 5 ORDER INTERNAL TIE-BREAKER (1 Dispatcher, Skor Identik) ===\n")
for i in range(11, 16):
    order = Order(f"O{i}", 10)
    print(f"--- ORDER {order.order_id} ---")
    # Paksa kondisi internal tie
    for d in dispatcher1.drivers:
        d.beban = 5  # bikin skor sama
    winner1 = dispatcher1.koordinasi_order(order)
    winner2 = dispatcher2.koordinasi_order(order)
    chosen = winner1
    team = dispatcher1.dispatcher_id
    print(f"*** Order {order.order_id} dimenangkan oleh {chosen[1].driver_id} dari {team} (skor: {chosen[0]:.2f})\n")
    results.append((order.order_id, team, chosen[1].driver_id, chosen[0]))

# SIMULASI GLOBAL TIE-BREAKER (2 Dispatcher, hasil sama)
print("\n=== SIMULASI 5 ORDER GLOBAL TIE-BREAKER (Skor Identik antar Dispatcher) ===\n")

# Pakai override bid agar hasil fix sama (simulasi)
original_bid = Driver.bid
def fixed_bid(self, order_location):
    jarak = 5
    waktu_respon = 5
    skor = 0.6 * jarak + 0.3 * 5 + 0.1 * waktu_respon  # skor = 5.0
    return skor, self, jarak, 5, waktu_respon

for driver in all_drivers:
    driver.bid = fixed_bid.__get__(driver, Driver)

for i in range(16, 21):
    order = Order(f"O{i}", 10)
    print(f"--- ORDER {order.order_id} ---")
    winner1 = dispatcher1.koordinasi_order(order)
    winner2 = dispatcher2.koordinasi_order(order)

    if winner1[0] < winner2[0]:
        chosen = winner1
        team = dispatcher1.dispatcher_id
    elif winner2[0] < winner1[0]:
        chosen = winner2
        team = dispatcher2.dispatcher_id
    else:
        print("  [Tie-breaker Global] Skor identik, masuk fase bid ulang...")
        all_candidates = [winner1[1], winner2[1]]
        tie_bids = []
        bid_count = 0
        while True:
            tie_bids.clear()
            bid_count += 1
            print(f"    [Bid ulang #{bid_count}]")
            for driver in all_candidates:
                simulated_beban = max(0, driver.beban - 1)
                jarak = 5
                waktu_respon = 5
                skor = 0.6 * jarak + 0.3 * simulated_beban + 0.1 * waktu_respon
                tie_bids.append((skor, driver))
                print(f"      Driver {driver.driver_id} bid ulang dengan skor: {skor:.2f} (beban dikurangi jadi {simulated_beban})")

            min_score = min(tie_bids, key=lambda x: x[0])[0]
            best_bidders = [tb for tb in tie_bids if tb[0] == min_score]
            if len(best_bidders) == 1:
                chosen = best_bidders[0]
                break
            elif all(b[1].beban == 0 for b in best_bidders):
                chosen = random.choice(best_bidders)
                print("    [Dipilih secara acak karena skor & beban identik]")
                break

        team = dispatcher1.dispatcher_id if chosen[1] in dispatcher1.drivers else dispatcher2.dispatcher_id
        print(f"  ==> Driver {chosen[1].driver_id} menang setelah bid ulang (skor: {chosen[0]:.2f})\n")

    print(f"*** Order {order.order_id} dimenangkan oleh {chosen[1].driver_id} dari {team} (skor: {chosen[0]:.2f})\n")
    results.append((order.order_id, team, chosen[1].driver_id, chosen[0]))

# Kembalikan fungsi bid asli
for driver in all_drivers:
    driver.bid = original_bid.__get__(driver, Driver)

# Rekap distribusi order per tim
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
