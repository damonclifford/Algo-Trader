import urllib2

class Data():
    """
    Class responsible for downloading and managing the stock data.
    """
    
    # Singleton instances of Data
    _instance = None
    
    @staticmethod
    def getInstance():
        """
        Returns the singleton instance of Data. If it does not exist, create it and then
        return it.
    
        @rtype: Data, the singleton instance of Data
        """
        if Data._instance == None:
            Data._instance = Data()
        return Data._instance
    
    def __init__(self):
        """
        Initializes a new Data object. Singleton, should only be called by getInstance().

        @rtype: None
        """
        self.stockData = []         # the dataset for a stock, represented as a list of ticks
        self.tradeLog = []          # log of position entry/exit, time, and which methodology
        self.tradeSignals = []      # marks by algorithm to signify long/short positions on chart,
                                    # stock data at each index organized in order: 
                                    # date, close, high, low, open, volume, cDays
                                    
        self.ticker = "AAPL"        # stock ticker name
        self.exchange = "NASD"      # stock exchange name
        self.timeDays = 0           # the day this data is from, expressed as number of days prior to
                                    # current day
                                    
        # used for timing and refreshing the data
        self.refreshFrequency = 300
        self.timeSinceRefresh = self.refreshFrequency
    
    
    def setDataTimerToReset(self):
        self.timeSinceRefresh = 299
        
        
    def refreshAndReset(self):
        data.refreshStockData()
        analyzer.preAnalysisCalculations()
        tradingStrategy.simulateStrategy()
        analyzer.postAnalysisCalculations()
        data.timeSinceRefresh = 0
        
        
    def popList(self, ls): #pops everything in list
        """
        Pops a list of data. Used since clear() is not compatible with the current version of
        Proessing.
    
        @rtype: None
        """
        lsLength = len(ls)
        for i in range(lsLength):
            ls.pop()
    
    
    def refreshStockData(self):
        """
        Downloads and refreshes the data for the stock being tracked.
        To adjust interval, set i = 60(minute), 3600(hour), etc.
        
        @rtype: None
        """
        URL = str("http://www.google.com/finance/getprices?q=" + self.ticker + "&candleStickCount=" +\
                   self.exchange + "&i=60&p=" + str(self.timeDays + 1) +\
                    "d&f=d,c,v,k,o,h,l&df=cpct&auto=0&ei=Ef6XUYDfCqSTiAKEMg")
        
        # Pop stockData, tradeLogs, and tradeSignals
        self.popList(self.stockData)
        self.popList(self.tradeLog)       
        self.popList(self.tradeSignals)
        
        response = urllib2.urlopen(URL)
        
        # Note: first 8 indices are other data
        data2 = response.read().split()
        for line in data2[8:398]:
            self.stockData.append([float(t) for t in line.split(',') ])
            
        
    def minLowInData(self):
        """
        Finds the minimum candlestick low of all candlesticks in the stock currently
        being tracked.
        
        @rtype: float
        """
        minPrice = 200000000
        for candleStickCount in range(len(self.stockData)):
            if self.stockData[candleStickCount][3] < minPrice:
                minPrice = self.stockData[candleStickCount][3]
        return minPrice
    
    
    def maxHighInData(self): 
        """
        Finds the maximum candlestick high of all candlesticks in the stock currently
        being tracked.
        
        @rtype: float
        """
        maxPrice = 0
        for candleStickCount in range(len(self.stockData)):
            if self.stockData[candleStickCount][2] > maxPrice:
                maxPrice = self.stockData[candleStickCount][2]
        return maxPrice