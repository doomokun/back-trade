from __future__ import (absolute_import, division, print_function,
                        unicode_literals)
import datetime  # For datetime objects
import os.path  # To manage paths
import sys  # To find out the script name (in argv[0])
# Import the backtrader platform
import backtrader as bt
from strategies import *
from indicators import *

isSingleTest = True

# Create a cerebro entity
cerebro = bt.Cerebro(optreturn=False)
# cerebro = bt.Cerebro()

# Datas are in a subfolder of the samples. Need to find where the script is
# because it could have been called from anywhere
# modpath = os.path.dirname(os.path.abspath(sys.argv[0]))
# datapath = os.path.join(modpath, 'data/XAUR-USD.csv')

# Create a Data Feed
data = bt.feeds.YahooFinanceCSVData(
    # dataname=datapath,
    dataname='data/XAUR-USD.csv',
    # Do not pass values before this date
    fromdate=datetime.datetime(2017, 1, 1),
    # Do not pass values after this date
    todate=datetime.datetime(2018, 12, 31),
    reverse=False)

# Add the Data Feed to Cerebro
cerebro.adddata(data)

cerebro.addanalyzer(bt.analyzers.SharpeRatio, _name='sharpe_ratio')

if isSingleTest == True:
    cerebro.addstrategy(MAcrossover)
else:
    cerebro.optstrategy(MAcrossover, pfast=range(5, 20), pslow=range(50, 100))

#默認頭寸大小
cerebro.addsizer(bt.sizers.SizerFix, stake=3)

# Set our desired cash start
cerebro.broker.setcash(100000.0)

if __name__ == '__main__':  
    if isSingleTest == True:
        start_portfolio_value = cerebro.broker.getvalue()
        cerebro.run()
        end_portfolio_value = cerebro.broker.getvalue()
        pnl = end_portfolio_value - start_portfolio_value 
        print('Starting Portfolio Value: %.2f' % start_portfolio_value) 
        print('Final Portfolio Value: %.2f' % end_portfolio_value) 
        print('PnL: %.2f' % pnl)  
    else:
        optimized_runs = cerebro.run()

        final_results_list = []
        for run in optimized_runs:
            for strategy in run:
                PnL = round(strategy.broker.get_value() - 10000, 2)
                sharpe = strategy.analyzers.sharpe_ratio.get_analysis()
                final_results_list.append([strategy.params.pfast, 
                    strategy.params.pslow, PnL, sharpe['sharperatio']])

        sort_by_sharpe = sorted(final_results_list, key=lambda x: x[3], 
                                reverse=True)
        for line in sort_by_sharpe[:5]:
            print(line)