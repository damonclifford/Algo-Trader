import TechnicalMethods
from Data import Data
from Analysis import Analysis
from View import View
from TechnicalMethods import SimpleMovingAverage
from TradingStrategy import TradingStrategy

class SimpleMomentum(TradingStrategy):
    """
    Class for the Simple Moving Average momentum strategy, which involves buying and selling
    based on whether or not the Simple Moving Average indicator has been consecutively
    increasing (or decreasing) for a past interval of time.
    
    Subclass of TradingStrategy.
    """
    
    def __init__(self):
        """
        Initializes a new SimpleMomentum object.

        @rtype: None
        """
        # Note: Each candlestick represents 1 minute
        self.durationForBuy = 15                # SMA duration 1 (SHORTER)
        self.durationForSell = 5                # SMA duration 2 (LONGER)
        
        self.baseLongPosition = 600             # base long position size
        self.baseShortPosition = 600            # base short position size
        self.analyzer = Analysis.getInstance()  # get the singleton instance of Analysis
        self.data = Data.getInstance()          # get the singleton instance of Data
        
        self.smaBuy = None                      # buy decision SMA object
        self.smaBuyList = None                  # list of buy decision SMA values
        self.smaSell = None                     # sell decision SMA object
        self.smaSellList = None                 # list of sell decision SMA values
        
        self.strategyName = "Simple Momentum (" + str(self.durationForBuy) + ", " +\
                                             str(self.durationForSell) + ")"


    def signalViewToDrawIndicators(self):
        """
        Notifies the View to draw the technical indicator(s) used for this trading strategy.
        
        @rtype: None
        """
        View.getInstantiatedInstance().drawIndicatorDoubleSMA(self.durationForBuy, 
                                                                 self.durationForSell)                
        
    # when refactoring, replace analysis with new class name
    def simulateStrategy(self):
        """
        Buys and sells stocks based on this trading strategy.
        
        @rtype: None
        """
        self.smaBuy = SimpleMovingAverage(self.durationForBuy)
        self.smaBuyList = self.smaBuy.getIndicators()
        self.smaSell = SimpleMovingAverage(self.durationForSell)
        self.smaSellList = self.smaBuy.getIndicators()
        
        # Loops over every tick within the downloaded data
        for candleStickCount in range(len(self.data.stockData)):
            additionalLongIsInLimits = self.analyzer.checkLongIsInLimits(self.analyzer.positionSize, 
                                                                         candleStickCount, self.baseLongPosition)
            additionalShortIsInLimits = self.analyzer.checkShortIsInLimits(self.analyzer.positionSize, 
                                                                           candleStickCount, self.baseShortPosition)
            
            # End of day liquidation
            if candleStickCount == 389:
                self.liquidateRemainingPosition(candleStickCount)
                
            # Checks if enough data to make purchase decision and is in limits
            elif candleStickCount > self.durationForBuy and additionalLongIsInLimits == 1:
                # Checks if SMA values have been rising for self.durationForBuy
                if TechnicalMethods.valuesRisingInListForInterval(self.durationForBuy, candleStickCount, self.smaBuyList):
                    # Buy
                    self.longStock(candleStickCount, self.baseLongPosition, 0)
            
            # Checks if enough data to make sell decision and is in limits
            elif candleStickCount > self.durationForSell and additionalShortIsInLimits == 1:
                # Checks if SMA values have been falling for self.durationForBuy
                if TechnicalMethods.valuesFallingInListForInterval(self.durationForSell, candleStickCount, self.smaSellList):
                    # Sell
                    self.shortStock(candleStickCount, self.baseShortPosition, 0)  
                
        
    def appendStrategySpecificInfo(self, trade, candleStickCount):
        """
        Adds information specific to this trading strategy to the trading logs.
        
        @type trade: list, the list of information pieces to be added to the trading log
        @type candleStickCount: int, the candlestick index at which this trade was made
        @rtype: None
        """
        buySmaValue = self.smaBuyList[candleStickCount]
        sellSmaValue = self.smaSellList[candleStickCount]
        trade.append("Long(Buy) SMA=" + str(buySmaValue) + ", Short(Sell) SMA=" + str(sellSmaValue))
    