from driver import Driver
from dispatcher import Dispatcher
from order import Order
from utils import evaluasi_tim, statistik_driver, analisis_global
import random
from collections import Counter

if __name__ == "__main__":
    # Setup: 2 tim dispatcher, masing-masing 2 driver
    drivers_team1 = [Driver('D1', 'Team1'), Driver('D2', 'Team1')]
    drivers_team2 = [Driver('D3', 'Team2'), Driver('D4', 'Team2')]
    all_drivers = drivers_team1 + drivers_team2

    dispatcher1 = Dispatcher('Team1', drivers_team1)
    dispatcher2 = Dispatcher('Team2', drivers_team2)

    # Simulasi 10 order masuk
    print("\n=== SIMULASI 10 ORDER OJEK ONLINE (AUCTION MULTI AGENT 2 vs 2) ===\n")
    results = []
    for i in range(1, 11):
        order = Order(f"O{i}", random.randint(1, 20))
        print(f"--- ORDER {order.order_id} ---")
        # Kedua dispatcher kompetisi, siapa paling efisien bagi tugas di timnya?
        winner1 = dispatcher1.koordinasi_order(order)
        winner2 = dispatcher2.koordinasi_order(order)
        # Siapa overall winner?
        if winner1[0] < winner2[0]:
            print(f"*** Order {order.order_id} dimenangkan oleh {winner1[1].driver_id} dari {dispatcher1.dispatcher_id} (skor: {winner1[0]:.2f})\n")
            results.append((order.order_id, dispatcher1.dispatcher_id, winner1[1].driver_id, winner1[0]))
        else:
            print(f"*** Order {order.order_id} dimenangkan oleh {winner2[1].driver_id} dari {dispatcher2.dispatcher_id} (skor: {winner2[0]:.2f})\n")
            results.append((order.order_id, dispatcher2.dispatcher_id, winner2[1].driver_id, winner2[0]))

    print("\n=== Distribusi order antar tim ===")
    team_count = Counter([r[1] for r in results])
    print(dict(team_count), "\n")

    # Evaluasi tiap tim
    evaluasi_tim(dispatcher1, "Team 1")
    evaluasi_tim(dispatcher2, "Team 2")

    # Statistik lengkap driver
    print("=== Statistik Tiap Driver ===")
    statistik_driver(all_drivers)

    # Statistik/analisis global
    analisis_global(results, all_drivers)

    print("=== SIMULASI SELESAI ===\n")
