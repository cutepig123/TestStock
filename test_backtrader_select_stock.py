import easyquotation
import json
from datetime import date
import os
import collections

quotation = easyquotation.use("daykline")

FOLDER = r'temp\\%s'%(date.today().strftime("%Y%m%d"))
FOLDER = r'temp\\20200927'
FILE_FORMAT = FOLDER + '\\%.5d.txt'

def is_equ(f1, f2):
    return abs(f1-f2)<0.001

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
        return sum(self.data[(n+i-self.period+1):(n+i+1)])/self.period

    def __len__(self):
        return len(self.data)

assert SMA(5,range(10))[-1]==sum(range(10)[-5:])/5

class RSI:
    def __init__(self, period, data):
        self.period = period
        self.data = data

    # Follow pyhton convension
    # [-1] the last element
    def __getitem__(self, i):
        n = len(self.data)
        inc = 0
        dec = 0
        for j in range((n+i-self.period+1), (n+i+1)):
            diff = self.data[j] - self.data[j-1]
            if diff>0:
                inc = inc + diff
            else:
                dec = dec - diff
        rs = inc/(dec+0.00000001)
        rsi = 100*rs/(1+rs)
        return rsi

    def __len__(self):
        return len(self.data)

def test_equ(a, b):
    assert is_equ(a, b), a

test_equ(RSI(6,range(10))[-1],100)
test_equ(RSI(6,range(10,0,-1))[-1],0)
test_equ(RSI(6,[10, 12, 14, 12, 14, 18, 16])[-1],71.428)

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

    def print(self, d, **kwargs):
        if not self.is_head_printed:
            for k, v in d.items():
                print("%15s"%(str(k)), end='')

            for key, value in kwargs.items():
                print("%15s"%(key), end='')
            print()
            self.is_head_printed = True

        for k, v in d.items():
            print("%15s"%(str(v)), end='')
        for key, value in kwargs.items():
            print("%15s"%(value), end='')
        print()

def grow_rate(yesterday, today):
    return 2.0*(today-yesterday)/(today+yesterday+0.00000001)

def grow_rates(data):
    n = len(data)
    rates = []
    for i in range(n-1):
        rate = grow_rate(data[i], data[i+1])
        rates.append(rate)
    return rates
    

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
        
def is_lowest_these_days(days1, days2, data_close ):
    assert(days1>=1)
    assert(days2>=1)
    grow_rate_tol_grow = 0.005
    grow_rate_tol_dec = 0.001
    
    # rates_near = grow_rates(data_close[-days1:])
    # rates_far = grow_rates(data_close[(-days2-days1):(-days1)])
    # is_ctus_grow = all([x>grow_rate_tol_grow for x in rates_near])
    # is_ctus_decrease = all([x<-grow_rate_tol_dec for x in rates_far])
    is_ctus_grow = all([grow_rate(data_close[i-1],data_close[i])>grow_rate_tol_grow for i in range(-1, -days1-1, -1)])
    is_ctus_decrease = all([grow_rate(data_close[i-1],data_close[i])<-grow_rate_tol_dec for i in range(-days1-1, -days1-days2-1, -1)])
    is_stg2_pass = is_ctus_grow and is_ctus_decrease
    return is_stg2_pass

assert is_lowest_these_days(2,3,[4,3,2,1,2,3])        
assert not is_lowest_these_days(3,3,[5,4,3,2,1,2,3])        
assert is_lowest_these_days(3,3,[4,3,2,1,2,3,4])        

def is_SMA_pass(sma1_period, sma2_period, data_close):
    daysbefore = -3
    data_sma1 = SMA(sma1_period, data_close)
    data_sma2 = SMA(sma2_period, data_close)
    is_last_week_less = data_sma1[daysbefore] < data_sma2[daysbefore]
    is_today_more = data_sma1[-1] > data_sma2[-1]
    return is_last_week_less and is_today_more
    

def test_strategy(stock_id, printer):
    data_lines = GetDatalines(stock_id)
    if not data_lines: return
    
    data_close = data_lines.data_close
    data_date = data_lines.data_date
    data_deal = data_lines.data_deal_money
    data_deal_num = data_lines.data_deal_num

    rsi1 = RSI(6, data_close)
    rsi2 = RSI(12, data_close)
    # stragety 1: MA相交綫策略(感覺本質上是追漲策略)
    deal = float(data_deal[-1])
    is_deal_enough = deal > 10
    is_sma530 = is_SMA_pass(5, 30, data_close) and is_deal_enough
    is_sma330 = is_SMA_pass(3, 30, data_close) and is_deal_enough

    # 最近三天有一天的deal大於最近15天的平均值的1.5倍
    deal_num_max_3days = max(data_deal_num[-3:])
    deal_num_mean_15_days = sum(data_deal_num[-15:])/15
    is_deal_num_ratio_pass = deal_num_max_3days > deal_num_mean_15_days*1.5

    # stragety 2: 連續幾天紐跌為升（抄底策略）
    # Days 1: recent

    is_low3 = is_lowest_these_days(3,3,data_close)
    is_low2 = is_lowest_these_days(2,3,data_close)
    is_low1 = is_lowest_these_days(1,3,data_close)
    is_rsi = is_lowest_these_days(1, 3, rsi1) and rsi1[-1]>=50 and  rsi1[-1]<70
    d=collections.OrderedDict()
    d['sma530'] = int(is_sma530)
    #d['sma330'] = int(is_sma330)
    d['is_low3'] = int(is_low3)
    d['is_low2'] = int(is_low2)
    #d['is_low1'] = int(is_low1)
    d['is_rsi'] = int(is_rsi)
    #d['grow_today'] = int(grow_rate(data_close[-2],data_close[-1])>0.04)
    if any([x for x in d.values()]):
        printer.print(
            d,
            stock_id='%d'%stock_id,
            deal='%.3f'%deal,
            deal_num = '%d'%is_deal_num_ratio_pass,
            rsi1 = '%.2f'%rsi1[-1] )

# save_all_stock_info()

printer = MyPrinter()
bGetData = int(input('Turn on Get Data 1/0?'))
if bGetData==1:
    os.system('md %s'%FOLDER)

for i in range(9999):
    if bGetData==1:
        save_stock_info(i)
    test_strategy(i, printer)
