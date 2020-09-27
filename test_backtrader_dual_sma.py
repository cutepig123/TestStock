# Pls use G:\sw\Python35-32-temp
from datetime import datetime
import backtrader as bt

Shortperiod=7
Longperiod=30

YEAR = 2018
NYEAR = 2
MY_stake = 100*5
STOCKNAME='1810.HK'

sma1_slope_threshold = -100

if 1:
    YEAR = 2018
    NYEAR = 2
    MY_stake = 100
    STOCKNAME='0522.HK'
    #Shortperiod=5
    sma1_slope_threshold = 0.0
if 0:
    YEAR = 2018
    NYEAR = 2
    MY_stake = 30
    STOCKNAME='0700.HK'
    #Shortperiod=5
    #Longperiod=10
if 0:
    YEAR = 2018
    NYEAR = 2
    MY_stake = 1000
    STOCKNAME='0992.HK'    

if 0:
    YEAR = 2018
    NYEAR = 2
    MY_stake = 10000
    STOCKNAME='0732.HK'  

if 0:
    YEAR = 2018
    NYEAR = 2
    MY_stake = 100
    STOCKNAME='2382.HK'      

class SmaCross(bt.SignalStrategy):
    def __init__(self):
        self.dataclose = self.datas[0].close
        self.sma1, self.sma2 = bt.ind.SMA(period=Shortperiod), bt.ind.SMA(period=Longperiod)

        # TODO: 這些變量其實不是真正的數字，那麽他們的比較，加減是怎麽做的呢？
        self.crossover = bt.ind.CrossOver(self.sma1, self.sma2)
        #self.signal_add(bt.SIGNAL_LONG, self.crossover)

    def next(self):
        sma1_slope = self.sma1[0] - self.sma1[-1]
        if not self.position:
            if self.crossover > 0 and sma1_slope>sma1_slope_threshold:
                self.buy()

        elif self.crossover < 0:
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

data0 = bt.feeds.YahooFinanceData(dataname=STOCKNAME, fromdate=datetime(YEAR, 1, 1),
                                  todate=datetime(YEAR + NYEAR, 1, 1))
cerebro.adddata(data0)

cerebro.broker.setcommission(commission=0.003)
cerebro.broker.setcash(20000)
cerebro.addsizer(bt.sizers.SizerFix, stake=MY_stake)

print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())
cerebro.run()
print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())

cerebro.plot()
