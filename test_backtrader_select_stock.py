import easyquotation
import json

quotation = easyquotation.use("daykline")


def save_stock_info(stock_id):
    try:
        # print(stock_id)
        data = quotation.real(['%.5d' % stock_id])
        s = json.dumps(data)
        with open('%.5d.txt' % stock_id, 'w') as f:
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


class Open:
    def __init__(self, data):
        self.raw_data = data
        self.data = {}

    def __getitem__(self, i):
        key = i
        if isinstance(key, slice):
            # Get the start, stop, and step from the slice
            return [self[ii] for ii in range(*key.indices(len(self)))]

        if i in self.data:
            return self.data[i]
        t = float(self.raw_data[i][1])
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

def test(stock_id, printer):
    s = open('%.5d.txt' % stock_id, 'r').read()
    data1 = json.loads(s)
    data = get_first_value(data1)
    if len(data) < 100:
        return
    if data[-1][0].find("2020-09") < 0:
        # print (data[-1][0])
        return
    data_open = Open(data)
    data_sma1 = SMA(5, data_open)
    data_sma2 = SMA(30, data_open)
    daysbefore = -2
    is_last_week_less = data_sma1[daysbefore] < data_sma2[daysbefore]
    is_today_more = data_sma1[-1] > data_sma2[-1]
    deal = float(data[-1][-1])
    is_deal_enough = deal > 10
    if is_last_week_less and is_today_more and is_deal_enough:
        printer.print(
            stock_id='%d'%stock_id,
            sma1_old='%.2f'%(data_sma1[daysbefore]),
            sma2_old='%.2f'%(data_sma2[daysbefore]),
            sma1_now='%.2f'%(data_sma1[-1]),
            sma2_now='%.2f'%(data_sma2[-1]),
            sma1_slope='%.2f'%(slope(data_sma1[-1], data_sma1[daysbefore])),
            sma2_slope='%.2f'%(slope(data_sma2[-1], data_sma2[daysbefore])),
            deal='%.2f'%deal)

# save_all_stock_info()

printer = MyPrinter()
test(136, printer)
for i in range(9999):
    # print(i)
    #save_stock_info(i)
    test(i, printer)