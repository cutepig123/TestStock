

class SMA:
    def __init__(self, period, data):
        self.period = period
        self.data = data

    # Follow pyhton convension
    # [-1] the last element
    def __getitem__(self, i):
        key = i
        if isinstance(key, slice):
            # Get the start, stop, and step from the slice
            return [self[ii] for ii in range(*key.indices(len(self)))]

        n = len(self.data)
        idx = i
        if idx < 0:
            idx = len(self) + idx
        if idx < 0 or idx >= len(self):
            raise IndexError("array index (%d) out of range [0, %d)" %(idx, len(self)))
        
        p2 = idx+1
        p1 = max(p2-self.period, 0)
        return sum(self.data[p1:p2])/self.period

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
        key = i
        if isinstance(key, slice):
            # Get the start, stop, and step from the slice
            return [self[ii] for ii in range(*key.indices(len(self)))]

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

def is_equ(f1, f2):
    return abs(f1-f2)<0.001

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

        n = len(self.data)
        idx = i
        if idx < 0:
            idx = len(self) + idx
        if idx < 0 or idx >= len(self):
            raise IndexError("array index (%d) out of range [0, %d)" %(idx, len(self)))
        
        if idx in self.data:
            return self.data[idx]

        #["2020-09-17", "0.660", "0.650", "0.660", "0.640", "1200500.000", {}, "0.000", "77.361"]
        ## [日期, 今开, 今收, 最高, 最低, 成交量 ]
        t = (self.raw_data[idx][self.idx])
        if self.isNum:
            t = float(t)
        self.data[i] = t
        return t

    def __len__(self):
        return len(self.raw_data)
