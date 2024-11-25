from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import RSI, EMA
from surmount.logging import log

class TradingStrategy(Strategy):
    def __init__(self):
        # Focusing on QQQ for tech sector performance
        self.ticker = "QQQ"

    @property
    def assets(self):
        return [self.ticker]

    @property
    def interval(self):
        return "1day"  # Using daily data for analysis

    def run(self, data):
        # Initialize allocation to 0
        allocation = {self.ticker: 0}
        
        # Getting the last 15 days of data for RSI and EMA calculation
        ohlcv_data = data["ohlcv"][-15:]
        
        # Calculating the RSI for the last 14 days, expect a list back
        rsi_values = RSI(self.ticker, ohlcv_data, length=14)
        
        # Short term EMA calculation over the last 10 days
        ema_values = EMA(self.ticker, ohlcv_data, length=10)
        
        if len(rsi_values) > 0 and len(ema_values) > 0:
            latest_rsi = rsi_values[-1]
            latest_ema = ema_values[-1]
            latest_close_price = ohlcv_data[-1][self.ticker]["close"]
            
            # Checking if RSI below 30 and starts rising & price above short-term EMA
            if latest_rsi < 30 and latest_close_price > latest_ema:
                log("RSI is below 30 and price crossed above EMA10, considering buying")
                allocation[self.ticker] = 0.9  # allocating 90% to QQQ, leaving room for adjustments
                
        return TargetAllocation(allocation)