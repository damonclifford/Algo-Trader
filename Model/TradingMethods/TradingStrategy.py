import TechnicalMethods
import abc
from Data import Data
from Analysis import Analysis
from View import View
from TechnicalMethods import SimpleMovingAverage

class TradingStrategy:
    """
    The parent class of all trading strategy classes. Contains 3 abstract methods for its 
    child classes to implement.
    """
    
    def __init__(self):
        """
        Notifies the View to draw the technical indicator(s) used for this trading strategy.
        It is intended for this method to be overridden in most, but not all, of this class's
        subclasses.
        
        @rtype: None
        """
        # Note: Each candlestick represents 1 minute
        self.strategyName = None
        self.baseLongPosition = 600             # base long position size
        self.baseShortPosition = 600            # base short position size
        self.analyzer = Analysis.getInstance()  # get the singleton instance of Analysis
        self.data = Data.getInstance()          # get the singleton instance of Data
        self.dynamicTradingSizeLong = 0.8       # How much money to use per long trade
                                                # as a percentage of cash
        self.dynamicTradingSizeShort = 0.8      # How much money to use per short trade
                                                # as a percentage of cash
    
    
    def resizeTradingSize(self, candleStickCount):
        """
        Dynamically resizes the buying/selling share size, to be called throughout a
        simulation.
        
        @type candleStickCount: int, the current tick index in the dataset for the stock
        @rtype: None
        """
        sharePrice = self.data.stockData[candleStickCount][1]
        actualCurrentCash = self.analyzer.cash + self.analyzer.positionSize
        self.baseLongPosition = int(self.dynamicTradingSizeLong * 
                                    actualCurrentCash / sharePrice)
        self.baseShortPosition = int(self.dynamicTradingSizeShort * 
                                     actualCurrentCash / sharePrice)
        
    @abc.abstractmethod
    def signalViewToDrawIndicators(self):
        """
        Notifies the View to draw the technical indicator(s) used for this trading strategy.
        Abstract method.
        
        @rtype: None
        """
        return
    
    @abc.abstractmethod
    def simulateStrategy(self):
        """
        Buys and sells stocks based on this trading strategy. Abstract method.
        
        @rtype: None
        """
        return
            
    def liquidateRemainingPosition(self, candleStickCount):
        """
        Closes any open long/short positions, generally called at the end of a trading
        day.
        
        @type candleStickCount: int, the current tick index in the dataset for the stock
        @rtype: None
        """
        if (self.analyzer.position > 0):
            self.shortStock(candleStickCount, self.analyzer.position, 0)
        elif (self.analyzer.position < 0):
            self.longStock(candleStickCount, self.analyzer.position, 0)

    
    def longStock(self, candleStickCount, positionSizeInShares, indicatorVariables):
        """
        Opens/adds a long position in a stock (i.e. buy the stock).
        
        @type candleStickCount: int, the current tick index in the dataset for the stock
        @type positionSizeInShares: int, the number of shares to be traded
        @type indicatorVariables: list, additional variables used to communicate information
                                  about a trade, unused parameter in most strategies
        @rtype: None
        """
        self.performLongStockCalculations(candleStickCount, positionSizeInShares)
        
        # append long mark at candleStickCount in self.data.tradeSignals and add trade record
        self.data.tradeSignals.append([candleStickCount, 0])
        View.getInstantiatedInstance().updateChart()
        self.addLongRecord(candleStickCount, self.strategyName, "Long", positionSizeInShares)
        
        
    def performLongStockCalculations(self, candleStickCount, positionSizeInShares):
        sharePrice = self.data.stockData[candleStickCount][1]
        self.analyzer.cash = self.analyzer.cash - positionSizeInShares * sharePrice
        self.analyzer.positionSize += positionSizeInShares * sharePrice
        self.analyzer.position = self.analyzer.position + positionSizeInShares
        self.analyzer.commissionTotal += self.analyzer.commission
        
        
    def shortStock(self, candleStickCount, positionSizeInShares, indicatorVariables):
        """
        Opens/adds a short position in a stock (i.e. sell the stock, or borrow stocks to sell
        them now and buy them back later for a profit).
        
        @type candleStickCount: int, the current tick index in the dataset for the stock
        @type positionSizeInShares: int, the number of shares to be traded
        @type indicatorVariables: list, additional variables used to communicate information
                                  about a trade, unused parameter in most strategies
        @rtype: None
        """
        self.performShortStockCalculations(candleStickCount, positionSizeInShares)
            
        # append short mark at candleStickCount in self.data.tradeSignals and add trade record
        self.data.tradeSignals.append([candleStickCount, 1])
        View.getInstantiatedInstance().updateChart()
        self.addShortRecord(candleStickCount, self.strategyName, "Short", positionSizeInShares)
        
        
    def performShortStockCalculations(self, candleStickCount, positionSizeInShares):
        sharePrice = self.data.stockData[candleStickCount][1]
        self.analyzer.cash = self.analyzer.cash + positionSizeInShares * sharePrice
        self.analyzer.positionSize -= positionSizeInShares * sharePrice
        self.analyzer.position = self.analyzer.position - positionSizeInShares
        self.analyzer.commissionTotal += self.analyzer.commission
        
        
    def addLongRecord(self, candleStickCount, strategyName, positionType, positionSizeInShares):
        # trade record structure: Candlestick #, Strategy, Position type, Position size, 
        # Price per share, Total price, Indicator variables
        trade = []
        self.addDetailsToTrade(trade, candleStickCount, strategyName, positionType, 
                               positionSizeInShares);
        self.appendStrategySpecificInfo(trade, candleStickCount)
        self.data.tradeLog.append(trade)
        
    
    def addShortRecord(self, candleStickCount, strategyName, positionType, positionSizeInShares):
        # trade record structure: Candlestick #, Strategy, Position type, Position size,
        # Price per share, Total price, Indicator variables
        trade = []
        self.addDetailsToTrade(trade, candleStickCount, strategyName, positionType, positionSizeInShares);
        self.appendStrategySpecificInfo(trade, candleStickCount)
        self.data.tradeLog.append(trade)
      
      
    @abc.abstractmethod
    def appendStrategySpecificInfo(self, trade, candleStickCount):
        """
        Adds information specific to this trading strategy to the trading logs. Abstract method.
        
        @type trade: list, the list of information pieces to be added to the trading log
        @type candleStickCount: int, the candlestick index at which this trade was made
        @rtype: None
        """
        return
         
        
    def addDetailsToTrade(self, trade, candleStickCount, strategyName, positionType, positionSizeInShares):
        sharePrice = self.data.stockData[candleStickCount][1]
        trade.append(candleStickCount)                                                # Candlestick number
        trade.append(strategyName)                                                    # Strategy name
        trade.append(positionType)                                                    # Position type
        trade.append(positionSizeInShares)                                            # Position share
        trade.append(str(self.data.stockData[candleStickCount][1]))                        # Price/share
        trade.append(positionSizeInShares * sharePrice)                               # Cash spent/gained
        trade.append(self.analyzer.position * sharePrice)                             # Total position size