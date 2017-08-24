from Data import Data

class SimpleMovingAverage:
    """
    Class responsible for calculating the Simple Moving Average for every
    ticker in a stock dataset.
    """
    
    def __init__(self, duration):
        """
        Initializes a new SimpleMovingAverage.
    
        @type duration: int, the duration of the simple moving average
        @rtype: None
        """
        self.duration = duration
    
    
    def getIndicators(self):
        """
        Computes and returns the simple moving average for every tick in the
        stock currently being tracked.
    
        @type duration: int, the duration of the simple moving average
        @rtype: list, the list of all simple moving average values of the given
                duration for all ticks in the stock being tracked in Data
        """
        sum = 0
        tail = 0
        head = 0
        returnList = []
        data = Data.getInstance()
        for i in range (len(data.stockData)):
            if i < self.duration - 1:
                # before enough data exists for indicator
                sum += data.stockData[i][1]
                returnList.append(sum/(i+1))
            elif i == self.duration - 1:
                # when enough data exists for indicator, set head & tail
                tail = data.stockData[i - self.duration][1]
                head = data.stockData[i][1]
                sum += data.stockData[i][1]
                returnList.append(sum/self.duration)
            else:
                # after enough data exists for indicator, remove tail
                # and add head to sums
                sum -= tail
                head = data.stockData[i][1]
                sum += head
                tail = data.stockData[i - self.duration][1]
                returnList.append(sum/self.duration)
        return returnList
    
    
def valuesRisingInListForInterval(duration, index, ls):
    """
    Returns whether the previous (duration) values to (index) in a list have
    been strictly increasing.

    @type duration: int, the number of previous values to check
    @type index: int, the index in the list to check backwards from
    @type ls: list, the list of values to check
    @rtype: int, whether the values in the list have been rising for the given
            duration
    """
    passed = 1
    if index - duration < 0:
        duration = index
        
    for i in range (index - duration + 1, index):
        if ls[i] >= ls[i+1]:
            passed = 0
    return passed


def valuesFallingInListForInterval(duration, index, ls):
    """
    Returns whether the previous (duration) values to (index) in a list have
    been strictly decreasing.

    @type duration: int, the number of previous values to check
    @type index: int, the index in the list to check backwards from
    @type ls: list, the list of values to check
    @rtype: int, whether the values in the list have been falling for the given
            duration
    """
    passed = 1
    if index - duration < 0:
        duration = index
        
    for i in range (index - duration + 1, index):
        if ls[i] <= ls[i+1]:
            passed = 0
    return passed


def crossOverDelayForLongTradesPassed(crossOverDelayLong, candlestickCount, smaShortList, smaLongList): 
    """
    Returns whether, from index (candleStickCount), the previous (crossOverDelayLong) 
    values of the shorter-term simple moving average (smaShortList) are all greater 
    than the previous (crossOverDelayLong) values of the longer-term simple moving
    average (smaLongList).

    @type crossOverDelayLong: int, the number of previous values to check
    @type candleStickCount: int, the index in the lists to compare backwards from
    @type smaShortList: list, containing the SMA values of the shorter-term SMA
    @type smaLongList: list, containing the SMA values of the longer-term SMA
    @rtype: int, whether the the compared values in smaShortList are all greater
            than the compared values in smaLongList
    """
    passed = 1
    for ticksAgo in range (crossOverDelayLong):
        shortCrossOverCountTicksAgo = smaShortList[candlestickCount - ticksAgo]
        longCrossOverCountTicksAgo = smaLongList[candlestickCount - ticksAgo]
        if shortCrossOverCountTicksAgo < longCrossOverCountTicksAgo:
            passed = 0
    return passed


def crossOverDelayForShortTradesPassed(crossOverDelayLong, candlestickCount, smaShortList, smaLongList):
    """
    Returns whether, from index (candleStickCount), the previous (crossOverDelayLong) 
    values of the shorter-term simple moving average (smaShortList) are all lesser 
    than the previous (crossOverDelayLong) values of the longer-term simple moving
    average (smaLongList).

    @type crossOverDelayLong: int, the number of previous values to check
    @type candleStickCount: int, the index in the lists to compare backwards from
    @type smaShortList: list, containing the SMA values of the shorter-term SMA
    @type smaLongList: list, containing the SMA values of the longer-term SMA
    @rtype: int, whether the the compared values in smaShortList are all lesser
            than the compared values in smaLongList
    """ 
    passed = 1
    for ticksAgo in range (crossOverDelayLong):
        shortCrossOverCountTicksAgo = smaShortList[candlestickCount - ticksAgo]
        longCrossOverCountTicksAgo = smaLongList[candlestickCount - ticksAgo]
        if shortCrossOverCountTicksAgo > longCrossOverCountTicksAgo:
            passed = 0
    return passed