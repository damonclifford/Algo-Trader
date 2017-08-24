from Data import Data

class Analysis():
    """
    Class responsible for managing share trading simulations.
    """
    
    # Singleton instance of Analysis
    _instance = None
    
    @staticmethod
    def getInstance():
        """
        Returns the singleton instance of Analysis. If it does not exist, create it and then
        return it.
    
        @rtype: Analysis, the singleton instance of Analysis
        """
        if Analysis._instance == None:
            Analysis._instance = Analysis()
        return Analysis._instance
    
    
    def __init__ (self):
        """
        Initializes a new Analysis object. Singleton, should only be called by getInstance().

        @rtype: None
        """
        self.cashInitial = 100000              # starting cash ($)
        self.cash = self.cashInitial           # 'current' cash variable throughout simulation ($)
    
        self.positionInitial = 0               # original position of assets in (shares)
        self.position = self.positionInitial   # position variable modified in backtest (shares)
    
        self.positionSize = 0                  # position in assets ($)
        self.commission = 10                   # commision paid per trade ($)
        self.commissionTotal = 0               # total commission paid ($)
        self.cashUsed = 0                      # cash used in trades ($)
        self.PL = 0                            # profit/loss ($)
    
        self.maxLongPosition = self.cashInitial    # maximum long position allowed
        self.maxShortPosition = -self.cashInitial  # maximum short position possible
        
        self.strategy = 1                      # trading strategy used
        
        
    def preAnalysisCalculations(self):
        """
        Makes the calculations and sets statistics prior to a trading simulation.

        @rtype: None
        """
        self.cash = self.cashInitial
        self.position = self.positionInitial
        self.commissionTotal = 0
        
        
    def postAnalysisCalculations(self):
        """
        Makes the calculations and sets statistics following a trading simulation.

        @rtype: None
        """
        data = Data.getInstance()
        self.positionSize = self.position * data.stockData[len(data.stockData) - 1][1]
        self.cash = self.cash - self.commissionTotal
        self.PL = self.cash - self.cashInitial + self.positionSize
        
        
    def checkShortIsInLimits(self, currentPositionInCash, candleStickCount, additionalPositionInShares):
        """
        Checks whether, following a potential new short position, the total cash position of the shorted
        shares is within the predefined limits.

        @type currentPositionInCash: float, the current amount of shares owned in terms of cash
        @type candleStickCount: int, the candlestick on which the current analysis is being run
        @type additionalPositionInShares: int, the amount of additional shares which would be added
        @rtype: None
        """
        data = Data.getInstance()
        if currentPositionInCash - additionalPositionInShares * data.stockData[candleStickCount][1] < self.maxShortPosition:
            return 0
        return 1
    
    
    def checkLongIsInLimits(self, currentPositionInCash, candleStickCount, additionalPositionInShares):
        """
        Checks whether, following a potential new long position, the total cash position of the shorted
        shares is within the predefined limits.

        @type currentPositionInCash: float, the current amount of shares owned in terms of cash
        @type candleStickCount: int, the candlestick on which the current analysis is being run
        @type additionalPositionInShares: int, the amount of additional shares which would be added
        @rtype: None
        """
        data = Data.getInstance()
        if currentPositionInCash + additionalPositionInShares * data.stockData[candleStickCount][1] > self.maxLongPosition:
            return 0
        return 1