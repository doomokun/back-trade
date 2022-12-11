import backtrader as bt

class MyIndicator(bt.Strategy):

    def log(self, txt, dt=None):
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt)) #列印收盤價格和日期

    def __init__(self):
        #引用data[0]中的收盤價格數據
        self.dataclose = self.datas[0].close
        self.datahigh = self.datas[0].high
        self.datalow = self.datas[0].low

    def next(self):
        day_range_total = 0
        for i in range(-13, 1):
            day_range = self.datahigh[i] - self.datalow[i]
            day_range_total += day_range
        M_Indicator = day_range_total / 14

        self.log('Close: %.2f, M_Indicator: %.4f' % (self.dataclose[0], M_Indicator))