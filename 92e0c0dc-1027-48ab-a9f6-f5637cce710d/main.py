from surmount.base_class import Strategy, TargetAllocation
from surmount.data import SocialSentiment, InsiderTrading

class TradingStrategy(Strategy):
    def __init__(self):
        # Define the ticker symbol for the asset you're interested in
        self.ticker = "AAPL"
        # Add SocialSentiment and InsiderTrading to the data list
        self.data_list = [SocialSentiment(self.ticker), InsiderTrading(self.ticker)]
    
    @property
    def assets(self):
        # Return a list of asset tickers
        return [self.ticker]


    def interval(self):
        # Define the interval for data fetching
        return "1day"
    
    def run(self, data):
        # Initial allocation is set to 0,
        allocationself.ticker: 0}
        # Processing social        social_data = data.get(("social_sentiment", self.ticker))
        if social_data and len) > 0:
            most_recent_sentiment = social_data[-1]["twitterSentiment"]
            # If the most recent Twitter sentiment data is above 0.5, it's considered positive
            if most_recent_sentiment > 0.5:
                allocation_dict[self.ticker] += 0.5
                
        # Processing insider trading data
        insider_data = data.get(("insider_trading", self.ticker))
        if insider_data and len(insider_data) > 0:
            most_recent_transaction = insider_data[-1]["transactionType"]
            # If the most recent transaction was a sale, it might indicate insiders are bearish
            if "Sale" in most_recent_transaction:
                allocation_dict[self.ticker] = 0  # Zero out allocation due to insider selling
        
        # Ensure the final allocation does not exceed 1
        if allocation_dict[self.ticker] > 1:
            allocation_dict[self.ticker] = 1
        
        return TargetAllocation(allocation_dict)