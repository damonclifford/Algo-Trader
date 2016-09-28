import TechnicalMethods
from Data import Data
from Analysis import Analysis
from View import View
from TechnicalMethods import SimpleMovingAverage
from TradingStrategy import TradingStrategy

class SMACrossOverDelayed(TradingStrategy):
    """
    Class for the Simple Moving Average Crossover strategy, which involves maintaining
    two Simple Moving Average indicators and purchasing/selling based on when they cross
    each other. When the SMAs cross each other, it is implied that short term fluctuations
    are greater than long term fluctuations.
    
    The difference between this strategy and the standard SMA Crossover strategy is that
    in this strategy, the algorithm waits for a period of time after a crossover before
    making the buy or sell decision.
    
    Subclass of TradingStrategy.
    """
    
    def __init__(self):
        """
        Initializes a new SMACrossOverDelayed object.

        @rtype: None
        """
        # Note: Each candlestick represents 1 minute
        self.crossOverDurationShorter = 15      # SMA duration 1 (SHORTER)
        self.crossOverDurationLonger = 50       # SMA duration 2 (LONGER)
        
        self.baseLongPosition = 600             # base long position size
        self.baseShortPosition = 600            # base short position size
        self.crossOverDelayForLongTrades = 3    # number of crossover ticks before executing a long position
        self.crossOverDelayForShortTrades = 3   # number of crossover ticks before executing a long position
        self.analyzer = Analysis.getInstance()  # get the singleton instance of Analysis
        self.data = Data.getInstance()          # get the singleton instance of Data
        
        self.smaShorter = None                  # shorter-term SMA object
        self.smaShorterList = None              # list of shorter-term SMA values
        self.smaLonger = None                   # longer-term SMA object
        self.smaLongerList = None               # list of longer-term SMA values
        
        self.strategyName = "SMA Crossover(" + str(self.crossOverDurationShorter) + "," + \
                                           str(self.crossOverDurationLonger) + ")" + " D=" + \
                                           str(self.crossOverDelayForLongTrades)


    def signalViewToDrawIndicators(self):
        """
        Notifies the View to draw the technical indicator(s) used for this trading strategy.
        
        @rtype: None
        """
        View.getInstantiatedInstance().drawIndicatorDoubleSMA(self.crossOverDurationShorter, 
                                                                 self.crossOverDurationLonger)                
        
        
    def simulateStrategy(self):
        """
        Buys and sells stocks based on this trading strategy.
        
        @rtype: None
        """
        self.smaShorter = SimpleMovingAverage(self.crossOverDurationShorter)
        self.smaShorterList = self.smaShorter.getIndicators()
        self.smaLonger = SimpleMovingAverage(self.crossOverDurationLonger)
        self.smaLongerList = self.smaLonger.getIndicators()
        
        # Loops over every tick within the downloaded data
        for candleStickCount in range(len(self.data.stockData)):
            previousShortTermSMA = self.smaShorterList[candleStickCount - 1]
            previousLongTermSMA = self.smaLongerList[candleStickCount - 1]
            currentShortTermSMA = self.smaShorterList[candleStickCount]
            currentLongTermSMA = self.smaLongerList[candleStickCount]
            additionalLongIsInLimits = self.analyzer.checkLongIsInLimits(self.analyzer.positionSize, +\
                                                                         candleStickCount, self.baseLongPosition)
            additionalShortIsInLimits = self.analyzer.checkShortIsInLimits(self.analyzer.positionSize, +
                                                                           candleStickCount, self.baseShortPosition)
            
            # End of day liquidation
            if candleStickCount == 389:
                self.liquidateRemainingPosition(candleStickCount)
                
            # Checks if enough data to make purchase decision and is in limits
            elif candleStickCount > self.crossOverDurationLonger and additionalLongIsInLimits == 1:
                # Cross over has been true for crossOverDelay duration
                if TechnicalMethods.crossOverDelayForLongTradesPassed(self.crossOverDelayForLongTrades,
                                                                      candleStickCount, self.smaShorterList,
                                                                      self.smaLongerList) == 1:
                    # Buy
                    self.longStock(candleStickCount, self.baseLongPosition, 0)
            
            # Checks if enough data to make sell decision and is in limits
            elif candleStickCount > self.crossOverDurationLonger and additionalShortIsInLimits == 1:
                # Checks if should sell
                if previousShortTermSMA > previousLongTermSMA and currentShortTermSMA <= currentLongTermSMA:
                    # Sell
                    self.shortStock(candleStickCount, self.baseShortPosition, 0)
                
        
    def appendStrategySpecificInfo(self, trade, candleStickCount):
        """
        Adds information specific to this trading strategy to the trading logs.
        
        @type trade: list, the list of information pieces to be added to the trading log
        @type candleStickCount: int, the candlestick index at which this trade was made
        @rtype: None
        """
        shortTermSMA = self.smaLongerList[candleStickCount]
        longTermSMA = self.smaShorterList[candleStickCount]
        trade.append("long-term SMA=" + str(shortTermSMA) + ", short-term SMA=" + str(longTermSMA))
    