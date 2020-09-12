from pandas_datareader import DataReader
from datetime import datetime

aapl = DataReader('APPL',  'yahoo', datetime(2015,7,1), datetime(2015,7,1))
print(aapl['Adj Close'][0])