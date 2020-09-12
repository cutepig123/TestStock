# https://www.backtrader.com/docu/quickstart/quickstart/

from __future__ import (absolute_import, division, print_function,
                        unicode_literals)
from datetime import datetime
import os.path  # To manage paths
import sys  # To find out the script name (in argv[0])

# Import the backtrader platform
import backtrader as bt

if __name__ == '__main__':
    # Create a cerebro entity
    cerebro = bt.Cerebro()

    # Create a Data Feed
    data = bt.feeds.YahooFinanceData(dataname='0522.HK', fromdate=datetime(2018, 1, 1),todate=datetime(2020, 9, 8))

    # Add the Data Feed to Cerebro
    cerebro.adddata(data)

    # Set our desired cash start
    cerebro.broker.setcash(100000.0)

    # Print out the starting conditions
    print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())

    # Run over everything
    cerebro.run()

    # Print out the final result
    print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())
