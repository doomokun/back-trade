import backtrader as bt

class MAcrossover(bt.Strategy):
    #移動平均參數
    params = (('pfast',20),('pslow',50),)
    def log(self, txt, dt=None):     
        dt = dt or self.datas[0].datetime.date(0)     
        # print('%s, %s' % (dt.isoformat(), txt))  # 執行策略優化時 可注釋掉此行
    def __init__(self):     
        self.dataclose = self.datas[0].close     
        # Order變量包含持倉數據與狀態
        self.order = None     
        # 初始化移動平均數據     
        self.slow_sma = bt.indicators.MovingAverageSimple(self.datas[0],                                       
                        period=self.params.pslow)     
        self.fast_sma = bt.indicators.MovingAverageSimple(self.datas[0], 
                        period=self.params.pfast)
        self.crossover = bt.indicators.CrossOver(self.slow_sma, self.fast_sma)
    def next(self):
        # 檢測是否有未完成訂單
        if self.order:
            return
        #驗證是否有持倉
        if not self.position:
        #如果沒有持倉，尋找開倉信號
            #SMA快線突破SMA慢線
            if self.crossover > 0: # Fast ma crosses above slow ma
                self.log('BUY CREATE, %.2f' % self.dataclose[0])
                #繼續追蹤已經創建的訂單，避免重複開倉
                self.order = self.buy()
                #如果SMA快線跌破SMA慢線
            elif self.crossover < 0: # Fast ma crosses below slow ma
                self.log('SELL CREATE, %.2f' % self.dataclose[0])
                #繼續追蹤已經創建的訂單，避免重複開倉
                self.order = self.sell()
        else:
            # 如果已有持倉，尋找平倉信號
            if len(self) >= (self.bar_executed + 5):
                self.log('CLOSE CREATE, %.2f' % self.dataclose[0])
                self.order = self.close()
    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            #主動買賣的訂單提交或接受時  - 不觸發
            return
        #驗證訂單是否完成
        #注意: 當現金不足時，券商可以拒絕訂單
        if order.status in [order.Completed]:
            if order.isbuy():
                self.log('BUY EXECUTED, %.2f' % order.executed.price)         
            elif order.issell():             
                self.log('SELL EXECUTED, %.2f' % order.executed.price)
            self.bar_executed = len(self)
        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log('Order Canceled/Margin/Rejected')     
        #重置訂單
        self.order = None