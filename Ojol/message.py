class Message:
    def __init__(self, content, order_id, auctioneer, bidders, messageType, FCLprototype=None):
        self.content = content
        self.order_id = order_id
        self.auctioneer = auctioneer
        self.bidders = bidders
        self.messageType = messageType
        self.FCLprototype = FCLprototype

    def communicate(self):
        if self.messageType == "broadcast":
            print(f"({self.order_id}) broadcasting message...")
        elif self.messageType == "message":
            print(f"({self.order_id}) sending message...")

        bids = []

        contentSplit = self.content.split(":")
        price = contentSplit[0]
        distance = contentSplit[1]
        auction_type = contentSplit[2]
        fipa_protocol = contentSplit[3]

        if self.messageType == "message":
            print(f"Sending bid info --> {self.content}")

        for bidder in self.bidders:
            bid_response = bidder.interact(self.content, auction_type, price, fipa_protocol)
            bids.append(bid_response)

        return bids

    def inform(self):
        if self.messageType == "broadcast":
            print(f"({self.order_id}) broadcasting auction result...")

        contentSplit = self.content.split(":")
        highest_bid = contentSplit[0]
        fipa_protocol = contentSplit[3]

        for bidder in self.bidders:
            bidder.interact(self.content, "eng/dutch", highest_bid, fipa_protocol)

    def request(self, agent_id):
        if self.messageType == "message":
            print(f"({self.order_id}) sending request message...")

        contentSplit = self.content.split(":")
        highest_bid = contentSplit[0]
        fipa_protocol = contentSplit[3]

        self.bidders[agent_id].interact(self.content, "eng/dutch", highest_bid, fipa_protocol, agent_id)
