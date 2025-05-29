from auction_env import Auction_env
from auctioneer import Auctioneer
from bidder import Bidder
import threading

def setup_drivers(order_id, driver_params):
    drivers = []
    for params in driver_params:
        drivers.append(Bidder(order_id, params[0], params[1], params[2]))
    return drivers

# 2 orders (auctioneer) dan 2 driver (bidders) tiap order — model 2 vs 2

auctioneer1 = Auctioneer('order1', 1000)
auctioneer2 = Auctioneer('order2', 1000)

drivers_order1 = [
    (1200, 2000, 3),  # driver 1
    (1300, 2000, 4)   # driver 2
]

drivers_order2 = [
    (1100, 1900, 2),  # driver 3
    (1250, 2100, 3)   # driver 4
]

bidders1 = setup_drivers('order1', drivers_order1)
bidders2 = setup_drivers('order2', drivers_order2)

auction1 = Auction_env(auctioneer1, bidders1)
auction2 = Auction_env(auctioneer2, bidders2)

def run_auction(auction_env):
    print(f"Starting auction for {auction_env.auctioneer.product_id} ...")
    auction_env.execute_auction()
    print(f"Auction for {auction_env.auctioneer.product_id} finished.\n")

t1 = threading.Thread(target=run_auction, args=(auction1,))
t2 = threading.Thread(target=run_auction, args=(auction2,))

t1.start()
t2.start()

t1.join()
t2.join()

print("All OJOL auctions completed.")
