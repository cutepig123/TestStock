import easyquotation
import json
from datetime import date
import os
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime

quotation = easyquotation.use("daykline")

FOLDER = r'temp\\%s'%(date.today().strftime("%Y%m%d"))
FOLDER = r'temp\data20200917'
FILE_FORMAT = FOLDER + '\\%.5d.txt'

def save_stock_info(stock_id):
    try:
        # print(stock_id)
        # http://sqt.gtimg.cn/utf8/q=r_hk00700
        data = quotation.real(['%.5d' % stock_id])
        s = json.dumps(data)
        with open(FILE_FORMAT % stock_id, 'w') as f:
            f.write(s)
    except e:
        print(e)


class SMA:
    def __init__(self, period, data):
        self.period = period
        self.data = data

    # Follow pyhton convension
    # [-1] the last element
    def __getitem__(self, i):
        n = len(self.data)
        return sum(self.data[(n+i-self.period):(n+i)])/self.period

    def __len__(self):
        return len(self.data)

class Slice:
    def __init__(self, data, begin, end):
        self.begin = begin
        self.end = end
        self.data = data

    # Follow pyhton convension
    # [-1] the last element
    def __getitem__(self, i):
        n = len(self)
        assert i<n and i>=-n
        if i>=0:
            return self.data[self.begin+i]

        return self.data[self.end+i]

    def __len__(self):
        return self.end - self.begin

myslice = Slice([0, 1,2,3,4], 1, 3)
assert myslice[0]==1
assert myslice[1]==2
assert myslice[-1]==2
assert myslice[-2]==1

class DateTimeForPlot:
    def __init__(self, data):
        self.data = data

    # Follow pyhton convension
    # [-1] the last element
    def __getitem__(self, i):
        return matplotlib.dates.date2num(datetime.strptime(self.data[i], '%Y-%m-%d'))

    def __len__(self):
        return len(self.data)

class DataLines:
    # ## [日期, 今开, 今收, 最高, 最低, 成交量 ]
    def __init__(self, data):
        self.data_date = DataLine(data, 0, False)
        self.data_open = DataLine(data, 1, True)
        self.data_close = DataLine(data, 2, True)
        self.data_max = DataLine(data, 3, True)
        self.data_min = DataLine(data, 4, True)
        self.data_deal_num = DataLine(data, 5, True)
        self.data_deal_money = DataLine(data, 8, True)
    
    def myslice(self, begin, end):
        dataLines = DataLines([])
        dataLines.data_date = Slice(self.data_date, begin, end)
        dataLines.data_open = Slice(self.data_open, begin, end)
        dataLines.data_close = Slice(self.data_close, begin, end)
        dataLines.data_max = Slice(self.data_max, begin, end)
        dataLines.data_min = Slice(self.data_min, begin, end)
        dataLines.data_deal_num = Slice(self.data_deal_num, begin, end)
        dataLines.data_deal_money = Slice(self.data_deal_money, begin, end)
        return dataLines

    def __len__(self):
        return  len(self.data_date)

class DataLine:
    def __init__(self, data, idx, isNum):
        self.raw_data = data
        self.data = {}
        self.idx = idx
        self.isNum = isNum

    def __getitem__(self, i):
        key = i
        if isinstance(key, slice):
            # Get the start, stop, and step from the slice
            return [self[ii] for ii in range(*key.indices(len(self)))]

        if i in self.data:
            return self.data[i]

        #["2020-09-17", "0.660", "0.650", "0.660", "0.640", "1200500.000", {}, "0.000", "77.361"]
        ## [日期, 今开, 今收, 最高, 最低, 成交量 ]
        t = (self.raw_data[i][self.idx])
        if self.isNum:
            t = float(t)
        self.data[i] = t
        return t

    def __len__(self):
        return len(self.raw_data)
def get_first_value(mydict):
    return next(iter(mydict.values()))
    # or list(my_dict.values())[0]


def slope(a, b):
    return (a-b)/(a+b)

class MyPrinter:
    def __init__(self):
        self.is_head_printed = False

    def print(self, **kwargs):
        if not self.is_head_printed:
            for key, value in kwargs.items():
                print("%15s"%(key), end='')
            print()
            self.is_head_printed = True

        for key, value in kwargs.items():
            print("%15s"%(value), end='')
        print()

def grow_rate(yesterday, today):
    return 2.0*(today-yesterday)/(today+yesterday)

def grow_rates(data):
    n = len(data)
    rates = []
    for i in range(n-1):
        rate = grow_rate(data[i], data[i+1])
        rates.append(rate)
    return rates
    
def is_equ(f1, f2):
    return abs(f1-f2)<0.001

def ctus_grow_in_n_days(data, grow_rate_tol):
    rates = grow_rates(data)
    is_ctus_grow = all([x>grow_rate_tol for x in rates])
    return is_ctus_grow
    
assert is_equ(grow_rate(0, 1), 2), grow_rate(0, 1)
assert(ctus_grow_in_n_days([0,1,2,3], 0.1))
assert(not ctus_grow_in_n_days([0,1,1.001,3], 0.1))

def GetDatalines(stock_id):
    s = open(FILE_FORMAT % stock_id, 'r').read()
    data1 = json.loads(s)
    data = get_first_value(data1)
    if len(data) < 100:
        return None
    if data[-1][0].find("2020-09") < 0:
        # print (data[-1][0])
        return None
    return DataLines(data)
        
def test_strategy(stock_id, printer):
    data_lines = GetDatalines(stock_id)
    if not data_lines: return
    
    data_close = data_lines.data_close
    data_date = data_lines.data_date
    data_deal = data_lines.data_deal_money

    data_sma1 = SMA(5, data_close)
    data_sma2 = SMA(30, data_close)

    # stragety 1: MA相交綫策略(感覺本質上是追漲策略)
    daysbefore = -2
    is_last_week_less = data_sma1[daysbefore] < data_sma2[daysbefore]
    is_today_more = data_sma1[-1] > data_sma2[-1]
    deal = float(data_deal[-1])
    is_deal_enough = deal > 10
    is_stg1_pass = is_last_week_less and is_today_more and is_deal_enough
    
    # stragety 2: 連續幾天紐跌為升（抄底策略）
    grow_rate_tol_grow = 0.005
    grow_rate_tol_dec = 0.001
    
    days1 = 3
    days2 = 3
    assert(days1>1)
    assert(days2>1)
    rates_near = grow_rates(data_close[-days1:])
    rates_far = grow_rates(data_close[(-days2-days1):(-days1)])
    is_ctus_grow = all([x>grow_rate_tol_grow for x in rates_near])
    is_ctus_decrease = all([x<-grow_rate_tol_dec for x in rates_far])
    is_stg2_pass = is_ctus_grow and is_ctus_decrease
    if is_stg1_pass or is_stg2_pass:
        printer.print(
            stock_id='%d'%stock_id,
            sma1_old='%.3f'%(data_sma1[daysbefore]),
            sma2_old='%.3f'%(data_sma2[daysbefore]),
            sma1_now='%.3f'%(data_sma1[-1]),
            sma2_now='%.3f'%(data_sma2[-1]),
            sma1_slope='%.3f'%(slope(data_sma1[-1], data_sma1[daysbefore])),
            sma2_slope='%.3f'%(slope(data_sma2[-1], data_sma2[daysbefore])),
            deal='%.3f'%deal,
            #rates_near = '%s'%rates_near,
            #rates_far = '%s'%rates_far,
            is_stg1_pass = '%d'%is_stg1_pass,
            is_ctus_grow = '%d'%is_ctus_grow,
            is_ctus_decrease = '%d'%is_ctus_decrease)

# save_all_stock_info()
def select_stock():
    printer = MyPrinter()
    bGetData = int(input('Turn on Get Data 1/0?'))
    if bGetData==1:
        os.system('md %s'%FOLDER)

    for i in range(9999):
        if bGetData==1:
            save_stock_info(i)
        test_strategy(i, printer)

class Broker:
    def __init__(self, data_lines):
        self.data_lines = data_lines
        self.strategy = None
        self.money_init = 10000
        # charge = stock_hkd * fee_rate + fee_fixed
        self.fee_rate = 0.002
        self.fee_fixed = 15
    
    def setStrategy(self, strategy):
        self.strategy = strategy
        strategy.broker = self

    def test(self):
        self.money_now = self.money_init
        self.stock_num = 0
        self.is_position = False
        for i in range(1, len(self.data_lines)):
            data_lines = self.data_lines.myslice(0, i)
            
            data_close = data_lines.data_close
            data_date = data_lines.data_date
            data_deal = data_lines.data_deal_money

            # Handle signals
            if self.strategy.is_buy_signal:
                # charge = stock_hkd * fee_rate + fee_fixed
                # money_now = charge + stock_hkd = stock_hkd*(1+fee_rate) + fee_fixed
                # stock_hkd = (money_now - fee_fixed) / (1+fee_rate)
                stock_hkd = (self.money_now - self.fee_fixed) / (1+self.fee_rate)

                self.stock_num = stock_hkd / data_close[-1]
                self.money_now = 0

                self.is_position = True
                self.strategy.is_buy_signal = False
            elif self.strategy.is_sell_signal:
                stock_hkd = self.stock_num * data_close[-1]
                charge = stock_hkd * self.fee_rate + self.fee_fixed
                
                self.money_now = stock_hkd - charge
                self.stock_num = 0
                self.is_position = False
                self.strategy.is_sell_signal = False

            self.strategy.next(data_lines)

            money = self.money_now + self.stock_num * data_close[-1]
            print(data_date[-1], money)

class StrategyBase:
    def __init__(self):
        self.is_buy_signal = False
        self.is_sell_signal = False

    def buy(self):
        self.is_buy_signal = True
    
    def sell(self):
        self.is_sell_signal = True

    def is_position(self):
        return self.broker.is_position
    
class MyStrategy(StrategyBase):
    def __init__(self):
        super().__init__()

    def next(self, data_lines):
        data_close = data_lines.data_close
        data_date = data_lines.data_date
        data_deal = data_lines.data_deal_money
        if self.is_position():
            self.sell()
        else:
            self.buy()

def plot_stock(data_date, data_close):
    fig, ax = plt.subplots()
    ax.xaxis.set_major_locator(matplotlib.dates.YearLocator())
    ax.xaxis.set_major_formatter(matplotlib.dates.DateFormatter('%Y'))
    ax.plot(DateTimeForPlot(data_date), data_close)
    plt.show()

def test_back_trace():
    printer = MyPrinter()
    stock_id = 522
    data_lines = GetDatalines(stock_id)
    if not data_lines: return
    
    broker = Broker(data_lines)
    strategy = MyStrategy()
    broker.setStrategy(strategy)
    broker.test()

    data_close = data_lines.data_close
    data_date = data_lines.data_date
    data_deal = data_lines.data_deal_money

    plot_stock(data_date, data_close)

test_back_trace()
