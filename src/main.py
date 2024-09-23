from ticker import Ticker
from strategy import MovingAverageCrossover, MeanReversion

# YFinance Data
apple = Ticker(ticker="AAPL", start_date='2020-01-01', end_date='2023-01-01')

# -- Perform Backtrading -- #
mac = MovingAverageCrossover( data = apple.data , short_window= 40, long_window= 100)
mac.run_backtrader()

mrs = MeanReversion( data= apple.data, window=30, num_std=2)
mrs.run_backtrader()