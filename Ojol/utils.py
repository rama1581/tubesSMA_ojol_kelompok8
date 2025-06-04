from collections import Counter

def evaluasi_tim(dispatcher, nama_tim):
    """
    Fungsi evaluasi performa tim (dispatcher).
    Menampilkan:
      - total order didapat
      - rata-rata skor penawaran
      - rata-rata waktu respon
      - order-log detail per order
    """
    total_order = len(dispatcher.order_log)
    if total_order == 0:
        return
    avg_skor = sum(log['skor'] for log in dispatcher.order_log) / total_order
    avg_waktu = sum(log['waktu_respon'] for log in dispatcher.order_log) / total_order
    print(f"=== Evaluasi {nama_tim} ===")
    print(f"Total order yang didapat: {total_order}")
    print(f"Rata-rata skor penawaran: {avg_skor:.2f}")
    print(f"Rata-rata waktu respon: {avg_waktu:.2f}")
    print("Order-log detail:")
    for log in dispatcher.order_log:
        print(f"  Order {log['order_id']}: Driver {log['driver_id']} (skor: {log['skor']:.2f}, jarak: {log['jarak']}, beban: {log['beban']}, waktu_respon: {log['waktu_respon']})")
    print()

def statistik_driver(drivers):
    """
    Menampilkan statistik lengkap tiap driver:
      - total order didapat
      - rata-rata skor penawaran
      - rata-rata waktu respon
      - detail log order
    """
    for driver in drivers:
        if driver.total_order == 0:
            avg_skor = avg_waktu = 0
        else:
            avg_skor = driver.total_skor / driver.total_order
            avg_waktu = driver.total_waktu_respon / driver.total_order
        print(f"Driver {driver.driver_id} ({driver.team}):")
        print(f"  Total order: {driver.total_order}")
        print(f"  Rata-rata skor penawaran: {avg_skor:.2f}")
        print(f"  Rata-rata waktu respon: {avg_waktu:.2f}")
        print(f"  Riwayat order:")
        for log in driver.log_order:
            print(f"    - Order {log['order_id']}: skor={log['skor']:.2f}, jarak={log['jarak']}, beban={log['beban']}, waktu_respon={log['waktu_respon']}")
        print()

def analisis_global(results, drivers):
    """
    Analisis statistik global seluruh simulasi.
    - Persentase kemenangan tim
    - Driver paling efisien (skor rata-rata terendah)
    - Order terbanyak per driver
    """
    print("=== Statistik Global ===")
    team_count = Counter([r[1] for r in results])
    total = sum(team_count.values())
    for tim in team_count:
        persen = team_count[tim] / total * 100
        print(f"Tim {tim}: {team_count[tim]} kemenangan ({persen:.1f}%)")
    print()
    driver_count = Counter([r[2] for r in results])
    max_order = max(driver_count.values())
    top_driver = [d for d, c in driver_count.items() if c == max_order]
    print(f"Driver dengan order terbanyak: {', '.join(top_driver)} ({max_order} order)\n")
    eff_driver = sorted(
        [(d.driver_id, d.total_order, d.total_skor/d.total_order if d.total_order > 0 else float('inf')) for d in drivers if d.total_order > 0],
        key=lambda x: x[2]
    )
    if eff_driver:
        print(f"Driver paling efisien (skor rata-rata terendah): {eff_driver[0][0]} (skor rata-rata: {eff_driver[0][2]:.2f})\n")
    else:
        print("Belum ada driver menerima order!\n")
