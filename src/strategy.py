import numpy as np
import backtrader as bt

class MovingAverageCrossover:
    def __init__(self, data, short_window, long_window):
        self.data = data
        self.cash = 1000
        self.short_window = short_window
        self.long_window = long_window

    def create_signals(self) -> None:
        # Manual Signal Creation

        # Calculate moving averages
        self.data['short_mavg'] = self.data['Close'].rolling(window=self.short_window, min_periods=1).mean()
        self.data['long_mavg'] = self.data['Close'].rolling(window=self.long_window, min_periods=1).mean()

        # Signal Value
        # 1.0 is Buy
        # -1.0 is Sell
        self.data['signal'] = 0.0
        self.data.iloc[self.short_window:, self.data.columns.get_loc('signal')] = np.where(
            self.data['short_mavg'][self.short_window:] > self.data['long_mavg'][self.short_window:], 1.0, 0.0
        )
        self.data.iloc[self.short_window:, self.data.columns.get_loc('signal')] = np.where(
            self.data['short_mavg'][self.short_window:] < self.data['long_mavg'][self.short_window:], -1.0, self.data['signal'][self.short_window:]
        )
        self.data['positions'] = self.data['signal'].diff()

    def test_signals(self) -> int:
        initial_cash = self.cash
        cash = initial_cash
        position = 0
        buy_price = 0.0
        profits = []

        for index, row in self.data.iterrows():
            if row['signal'] == 1.0:  # Buy signal
                if cash > 0:
                    buy_price = row['Close']
                    position += cash / buy_price
                    cash = 0
                    profits.append((index, 'Buy', buy_price, position))
            
            elif row['signal'] == -1.0:  # Sell signal
                if position > 0:
                    sell_price = row['Close']
                    cash += position * sell_price
                    profits.append((index, 'Sell', sell_price, 0))
                    position = 0

        # Calculate total profit
        return cash - initial_cash

    def run_backtrader(self):
        class Strategy(bt.Strategy):
            params = (
                ('short_window', self.short_window),
                ('long_window', self.long_window),
            )

            def __init__(self):
                self.short_mavg = bt.indicators.SimpleMovingAverage(self.data.close, period=self.params.short_window)
                self.long_mavg = bt.indicators.SimpleMovingAverage(self.data.close, period=self.params.long_window)

            def next(self):
                if not self.position:
                    if self.short_mavg[0] > self.long_mavg[0]:
                        self.buy()
                else:
                    if self.short_mavg[0] < self.long_mavg[0]:
                        self.sell()

        # Set up Backtrader
        cerebro = bt.Cerebro()
        cerebro.addstrategy(Strategy)

        # Create data feed
        data_feed = bt.feeds.PandasData(dataname=self.data)

        cerebro.adddata(data_feed)
        cerebro.broker.setcash(self.cash)

        # Run the Backtrader engine
        cerebro.run()
        print(f'Final Portfolio Value: {cerebro.broker.getvalue()}')

