# Pls use G:\sw\Python35-32-temp
from datetime import datetime
import backtrader as bt
import numpy

# 均值回歸策略，發現效果并不好
class SmaCross(bt.SignalStrategy):
    def __init__(self):
        self.dataclose = self.datas[0].close
        sma1, sma2 = bt.ind.SMA(period=7), bt.ind.SMA(period=30)
        self.sma1 = sma1
        self.sma2 = sma2
        self.crossover = bt.ind.CrossOver(sma1, sma2)
        #self.signal_add(bt.SIGNAL_LONG, crossover)

    def next(self):
        arr = numpy.array(self.dataclose.get(0, 10))
        avg_prce = numpy.mean(arr)
        sd_prce = numpy.std(arr)
        margin = 3
        lb = avg_prce - margin
        ub = avg_prce + margin
        if not self.position:
            if self.dataclose[0] < lb:
                self.safety_level = self.dataclose[0]*.9
                self.buy()

        else:
            if self.dataclose[0] > ub or self.dataclose[0] < self.safety_level:
                self.close()

    def log(self, txt, dt=None):
        ''' Logging function fot this strategy'''
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))

    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            # Buy/Sell order submitted/accepted to/by broker - Nothing to do
            return

        # Check if an order has been completed
        # Attention: broker could reject order if not enough cash
        if order.status in [order.Completed]:
            if order.isbuy():
                self.log(
                    'BUY EXECUTED, Price: %.2f, Cost: %.2f, Comm %.2f' %
                    (order.executed.price,
                     order.executed.value,
                     order.executed.comm))

                self.buyprice = order.executed.price
                self.buycomm = order.executed.comm
            else:  # Sell
                self.log('SELL EXECUTED, Price: %.2f, Cost: %.2f, Comm %.2f' %
                         (order.executed.price,
                          order.executed.value,
                          order.executed.comm))

            self.bar_executed = len(self)

        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log('Order Canceled/Margin/Rejected')

        self.order = None

    def notify_trade(self, trade):
        if not trade.isclosed:
            return

        self.log('OPERATION PROFIT, GROSS %.2f, NET %.2f' %
                 (trade.pnl, trade.pnlcomm))


cerebro = bt.Cerebro()
cerebro.addstrategy(SmaCross)

data0 = bt.feeds.YahooFinanceData(dataname='0522.HK', fromdate=datetime(2017, 9, 1),
                                  todate=datetime(2020, 9, 8))
cerebro.adddata(data0)

cerebro.broker.setcommission(commission=0.003)
cerebro.broker.setcash(100000)
cerebro.addsizer(bt.sizers.SizerFix, stake=100)

print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())
cerebro.run()
print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())

cerebro.plot()
