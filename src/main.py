from ticker import Ticker
from strategy import MovingAverageCrossover

apple = Ticker(ticker="AAPL", start_date='2020-01-01', end_date='2023-01-01')
mac = MovingAverageCrossover( data = apple.data , short_window= 40, long_window= 100)

mac.create_signals()

print("Signals:")
print(mac.data['signal'].value_counts())

profits = mac.test_signals()
print( profits )

mac.run_backtrader()