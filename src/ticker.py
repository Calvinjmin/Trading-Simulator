import yfinance

class Ticker:
    def __init__(self, ticker: str, start_date: str, end_date: str ):
        self.ticker = ticker
        self.data = yfinance.download(self.ticker, start=start_date, end=end_date)
    
