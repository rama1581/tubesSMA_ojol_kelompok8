from message import Message

class Auction_env:
    def __init__(self, auctioneer, bidders):
        self.auctioneer = auctioneer
        self.bidders = bidders

    def execute_auction(self):
        self.auctioneer.announce_order()

        # buat content: "base_price:distance:auction_type:protocol"
        # disini distance dan protocol dummy
        content = f"{self.auctioneer.base_price}:5:english:dutch"

        msg = Message(content, self.auctioneer.product_id, self.auctioneer, self.bidders, "message", None)
        bids = msg.communicate()

        # cari pemenang berdasarkan bid terendah
        valid_bids = [bid for bid in bids if bid[0] != float('inf')]
        if not valid_bids:
            print(f"No valid bids for order {self.auctioneer.product_id}")
            return

        winner_bid = min(valid_bids, key=lambda x: x[0])
        winning_price = winner_bid[0]
        winner_driver = winner_bid[1]

        print(f"Order {self.auctioneer.product_id} won by Driver {winner_driver.driver_id} with bid {winning_price}")

        # inform all bidders hasil
        inform_msg = Message(f"{winning_price}:::{'dutch'}", self.auctioneer.product_id, self.auctioneer, self.bidders, "broadcast")
        inform_msg.inform()

        # notify pemenang secara khusus
        winner_driver.notify_win(f"You won order {self.auctioneer.product_id} at price {winning_price}")
