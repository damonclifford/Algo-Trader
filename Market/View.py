from Data import Data
from StockProfile import StockProfile
from TradingStrategyProfile import TradingStrategyProfile
from DayForwardProfile import DayForwardProfile
from DayPreviousProfile import DayPreviousProfile
from ModeProfile import ModeProfile
from TechnicalMethods import SimpleMovingAverage
from Analysis import Analysis

class View():
    """
    Handles all aspects of the View component of the program: drawing the chart, 
    trade history, and profiles.
    
    Class currently has too many responsibilities. TODO: Refactor into 3/4 different files.
    """
    # Singleton instance of View
    _instance = None
    
    @staticmethod
    def getInstance(width, height):
        """
        Returns the singleton instance of View. If it does not exist, create it and then
        return it.
    
        @rtype: View, the singleton instance of View
        """
        if View._instance == None:
            View._instance = View(width, height)
        return View._instance
    
    
    # Singleton getInstance with no variables, only to be called from non-Market classes.
    @staticmethod
    def getInstantiatedInstance():
        """
        Returns the singleton instance of View. Requires View to already have been instantiated,
        dealing with it this way since other files cannot access width and height.
    
        @rtype: View, the singleton instance of View
        """
        return View._instance
         
    
    def __init__ (self, width, height):
        """
        Initializes a new View. Should only be called by the singleton method.
        
        @type width: int, the width of the screen
        @type height: int, the height of the screen
        @rtype: None
        """
        # Mode in which the user is viewing
        self.mode = 0
        
        # Static standard font size
        View.stdTextSize = int(width / 116.364)
        
        # Declares starting area of the chart
        self.chartStartX = 0.03 * width
        self.chartStartY = 0.03 * height
        self.chartWidth = 0.94 * width
        self.chartHeight = 0.6 * height
        
        # Sets up the profiles for the stocks tracked
        self.profiles = []
        self._stockProfileCount = 0
        self._strategyProfileCount = 0
        self._modeProfileCount = 0
        self.setProfiles()
        
        # Fetch data instance and set highest and lowest prices on screen
        self._data = Data.getInstance()
        self._highestPrice = self._data.maxHighInData()
        self._lowestPrice = self._data.minLowInData()
        
        # Sets price:pixel density and variables for functions
        self._pixelDensity = 0.6 * height / (self._highestPrice - self._lowestPrice)
        self._candleStickWidth = 0.94 * width / (390 + 2)
        self._candleStickStartX = self.chartStartX + 0.0027 * width
        
        
    def drawMainScreen(self, tradingStrategy):
        """
        Draws the Main Screen of the program.
        
        @rtype: None
        """
        self.drawChart()
        self.drawBuySells()
        self.drawInfo()
        self.drawProfiles()
        tradingStrategy.signalViewToDrawIndicators()
        
        
    def drawHistoryScreen(self):
        """
        Draws the History Screen of the program.
        
        @rtype: None
        """
        self.drawTradeHistory()
        self.drawInfo()
        self.drawProfiles()
        
        
    def drawIndicatorDoubleSMA(self, crossOverDurationShorter, crossOverDurationLonger):
        """
        Draws two simple moving average indicators on the stock chart.
        
        @rtype: None
        """
        smaShort = SimpleMovingAverage(crossOverDurationShorter)
        smaShortList = smaShort.getIndicators()
        smaLong = SimpleMovingAverage(crossOverDurationLonger)
        smaLongList = smaLong.getIndicators()
        
        for candleStickCount in range(1, len(self.data.stockData)): #candleStickCount chart
            # draw short-term SMA
            colorGreen()
            lineX = self._candleStickStartX + 0.5 * self._candleStickWidth + candleStickCount * self._candleStickWidth
            lineY1 = self.chartStartY + self.chartHeight - (smaShortList[candleStickCount - 1] - self._lowestPrice) * self._pixelDensity
            lineY2 = self.chartStartY + self.chartHeight - (smaShortList[candleStickCount] - self._lowestPrice) * self._pixelDensity        
            line(lineX - self._candleStickWidth, lineY1, lineX, lineY2)
            
            # draw long-term SMA
            colorBlue()
            lineX = self._candleStickStartX + 0.5 * self._candleStickWidth + candleStickCount * self._candleStickWidth
            lineY1 = self.chartStartY + self.chartHeight - (smaLongList[candleStickCount - 1] - self._lowestPrice) * self._pixelDensity
            lineY2 = self.chartStartY + self.chartHeight - (smaLongList[candleStickCount] - self._lowestPrice) * self._pixelDensity        
            line(lineX - self._candleStickWidth, lineY1, lineX, lineY2)
            
        
    def updateChart(self):
        """
        Updates the stock's chart based on new input data from singleton classes.
        
        @rtype: None
        """
        self.data = Data.getInstance()
        self._tradeSignals = self._data.tradeSignals
        self._highestPrice = self._data.maxHighInData()
        self._lowestPrice = self._data.minLowInData()
        self._pixelDensity = 0.6 * height / (self._highestPrice - self._lowestPrice)
        
        
    def setProfiles(self):
        """
        Sets up the clickable profiles to display for the View.
        
        @rtype: None
        """
        self._setStockProfiles()
        self._setStrategyProfiles()
        self._setModeProfiles()
        self._setDayControlProfiles()
    
    
    def _setDayControlProfiles(self):
        """
        Sets up the clickable day-control profiles to display for the View. Helper.
        
        @rtype: None
        """
        self.profiles.append(DayForwardProfile("Next Day", self))
        self.profiles.append(DayPreviousProfile("Prev. Day", self))

    def _setModeProfiles(self):
        """
        Sets up the clickable mode profiles to display for the View. Helper.
        
        @rtype: None
        """
        self._addModeProfile("Main Screen", 0)
        self._addModeProfile("Trading History", 1)
        
        
    def _addModeProfile(self, name, modeIndex):
        """
        Adds a mode profile to the list of existing profiles. Helper.
        
        @rtype: None
        """
        self.profiles.append(ModeProfile(name, modeIndex, self._modeProfileCount, self))
        self._modeProfileCount += 1
        
    def _setStrategyProfiles(self):
        """
        Sets up the clickable trading strategy profiles to display for the View. Helper.
        
        @rtype: None
        """
        self._addTradingStrategyProfile("SMA Momentum (15, 5)", 0)
        self._addTradingStrategyProfile("SMA Crossover (15, 50)", 1)
        self._addTradingStrategyProfile("SMA Crossover (15, 5) Delay (3)", 2)
        

    def _addTradingStrategyProfile(self, name, strategyIndex):
        """
        Adds a trading strategy profile to the list of existing profiles. Helper.
        
        @rtype: None
        """
        self.profiles.append(TradingStrategyProfile(name, strategyIndex, self._strategyProfileCount, self))
        self._strategyProfileCount += 1
        
        
    def _setStockProfiles(self):
        """
        Sets up the clickable trading stock profiles to display for the View. Helper.
        
        @rtype: None
        """
        self._addStockProfile("GOOGL", "NASD")
        self._addStockProfile("FB", "NASD")
        self._addStockProfile("AMZN", "NASD")
        self._addStockProfile("MSFT", "NASD")
        self._addStockProfile("AAPL", "NASD")
        self._addStockProfile("TWTR", "NYSE")
        self._addStockProfile("EBAY", "NASD")
        self._addStockProfile("ORCL", "NASD")
        self._addStockProfile("CSCO", "NASD")
        self._addStockProfile("YHOO", "NASD")
        self._addStockProfile("BABA", "NASD")
        self._addStockProfile("HP", "NASD")
        self._addStockProfile("INTC", "NASD")
        self._addStockProfile("QCOM", "NASD")
        self._addStockProfile("IBM", "NYSE")
        self._addStockProfile("TXN", "NASD")
        self._addStockProfile("ADBE", "NASD")
        self._addStockProfile("SAP", "NASD")
        self._addStockProfile("AVGO", "NASD")
        self._addStockProfile("BIDU", "NASD")
        self._addStockProfile("CRM", "NYSE")
        self._addStockProfile("ADP", "NASD")
        self._addStockProfile("NVDA", "NASD")
        self._addStockProfile("NOK", "NASD")
        self._addStockProfile("VMW", "NASD")
        self._addStockProfile("NXPI", "NASD")
        self._addStockProfile("LNKD", "NASD")
        self._addStockProfile("EA", "NASD")
        self._addStockProfile("ADSK", "NASD")
        self._addStockProfile("RHT", "NASD")
        self._addStockProfile("NOW", "NYSE")
        self._addStockProfile("MBLY", "NYSE")
        
        
    def _addStockProfile(self, ticker, exchange):
        """
        Adds a stock profile to the list of existing profiles. Helper.
        
        @rtype: None
        """
        self.profiles.append(StockProfile(ticker, exchange, self._stockProfileCount, self))
        self._stockProfileCount += 1
        
        
    def drawProfiles(self):
        """
        Draws the profiles contained in this View.
        
        @rtype: None
        """
        for profile in self.profiles:
            profile.drawProfile()
        colorWhite()
        
    
    def drawChart(self):
        """
        Draws the stock chart and the candlesticks.
        
        @rtype: None
        """
        colorWhite()
        rect(self.chartStartX, self.chartStartY, self.chartWidth, self.chartHeight)
        
        for candleStickCount in range(len(self.data.stockData)): #candleStickCount chart
            # determine the color of the candlesticks
            if(self.data.stockData[candleStickCount][1] >= self.data.stockData[candleStickCount][4]):
                colorGreen()
            else:
                colorRed()
    
            # draw the upper and lower lines of the candlestick
            lineX = self._candleStickStartX + 0.5 * self._candleStickWidth + candleStickCount * self._candleStickWidth
            lineY1 = self.chartStartY + self.chartHeight - (self.data.stockData[candleStickCount][3] - self._lowestPrice) * self._pixelDensity
            lineY2 = self.chartStartY + self.chartHeight - (self.data.stockData[candleStickCount][2] - self._lowestPrice) * self._pixelDensity        
            line(lineX, lineY1, lineX, lineY2)

            # draw the body of the candleStickCount
            candleStickX = self._candleStickStartX + candleStickCount * self._candleStickWidth
            candleStickY = self.chartStartY + self.chartHeight - (self.data.stockData[candleStickCount][4] - self._lowestPrice) * self._pixelDensity
            candleStickHeight = -(self.data.stockData[candleStickCount][1] - self.data.stockData[candleStickCount][4]) * self._pixelDensity
            rect(candleStickX, candleStickY, self._candleStickWidth, candleStickHeight)
        
        # draw highest and lowest prices
        colorBlue()
        textSize(View.stdTextSize)
        text(self._highestPrice, 0.032 * width, 0.045 * height) #Highest price label
        text(self._lowestPrice, 0.032 * width, 0.625 * height) #Lowest price label
    
    
    def drawBuySells(self):
        """
        Draws the buy and sell arrows (signals) for the stock chart.
        
        @rtype: None
        """
        # draw arrows on chart for buy/sell signals
        for candleStickCount in range(len(self._tradeSignals)):
            if self._tradeSignals[candleStickCount][1] == 0:
                self.drawUpArrowForLong(candleStickCount)
            if self._tradeSignals[candleStickCount][1] == 1:
                self.drawDownArrowForShort(candleStickCount)
    
    
    def drawUpArrowForLong(self, candleStickCount):
        """
        Draws an upward arrow indicating a long (buy) signal at the position of a given
        candlestick.
        
        @type candleStickCount: int, index of the candlestick to draw at
        @rtype: None
        """
        colorGreen()
        actionBuySquareX = self._candleStickStartX + self._tradeSignals[candleStickCount][0] * self._candleStickWidth
        actionBuySquareY = self.chartStartY + self.chartHeight + 0.05 * height - (self.data.stockData[self._tradeSignals[candleStickCount][0]][3] - self._lowestPrice) * self._pixelDensity
        rect(actionBuySquareX, actionBuySquareY, self._candleStickWidth + 0.001 * width, 0.008 * height)
        
        triangleX1 = self._candleStickStartX - 0.0015 * width + self._tradeSignals[candleStickCount][0] * self._candleStickWidth
        triangleY1 = self.chartStartY + self.chartHeight + 0.05 * height - (self.data.stockData[self._tradeSignals[candleStickCount][0]][3] - self._lowestPrice) * self._pixelDensity
        triangleX2 = self._candleStickStartX + 0.005 * width + self._tradeSignals[candleStickCount][0] * self._candleStickWidth
        triangleY2 = triangleY1
        triangleX3 = self._candleStickStartX + 0.00175 * width + self._tradeSignals[candleStickCount][0] * self._candleStickWidth
        triangleY3 = self.chartStartY + self.chartHeight + 0.04 * height - (self.data.stockData[self._tradeSignals[candleStickCount][0]][3] - self._lowestPrice) * self._pixelDensity
        triangle(triangleX1, triangleY1, triangleX2, triangleY2, triangleX3, triangleY3)
        
        
    def drawDownArrowForShort(self, candleStickCount):
        """
        Draws an downward arrow indicating a short (sell) signal at the position of a given
        candlestick.
        
        @type candleStickCount: int, index of the candlestick to draw at
        @rtype: None
        """
        colorRed()
        actionSellSquareX = self._candleStickStartX + self._tradeSignals[candleStickCount][0] * self._candleStickWidth
        actionSellSquareY = self.chartStartY + self.chartHeight - 0.05 * height - (self.data.stockData[self._tradeSignals[candleStickCount][0]][2] - self._lowestPrice) * self._pixelDensity
        rect(actionSellSquareX, actionSellSquareY, self._candleStickWidth + 0.001 * width, -0.008 * height)
        
        triangleX1 = self._candleStickStartX - 0.0015 * width + self._tradeSignals[candleStickCount][0] * self._candleStickWidth
        triangleY1 = self.chartStartY + self.chartHeight - 0.05 * height - (self.data.stockData[self._tradeSignals[candleStickCount][0]][2] - self._lowestPrice) * self._pixelDensity
        triangleX2 = self._candleStickStartX + 0.005 * width + self._tradeSignals[candleStickCount][0] * self._candleStickWidth
        triangleY2 = triangleY1
        triangleX3 = self._candleStickStartX + 0.00175 * width + self._tradeSignals[candleStickCount][0] * self._candleStickWidth
        triangleY3 = self.chartStartY + self.chartHeight - 0.04 * height - (self.data.stockData[self._tradeSignals[candleStickCount][0]][2] - self._lowestPrice) * self._pixelDensity
        triangle(triangleX1, triangleY1, triangleX2, triangleY2, triangleX3, triangleY3)
        
    
    def drawInfo(self):
        """
        Displays the information and statistics for the information panel.
        
        The name and value for each item are shown in separate text() calls for
        alignment purposes.
        
        @rtype: None
        """
        analyzer = Analysis.getInstance()
        
        # sizes of the information panel
        infoStartX = 0.55 * width
        infoStartY = 0.66 * height
        infoWidth = 0.42 * width
        infoHeight = 0.25 * height
        
        colorWhite()
        
        # draw the rectangular panel
        rect(infoStartX, infoStartY, infoWidth, infoHeight)
        
        # draw information panel item separators
        line(infoStartX + 0.148 * width, infoStartY, infoStartX + 0.148 * width, infoStartY + infoHeight)
        line(infoStartX + 0.322 * width, infoStartY, infoStartX + 0.322 * width, infoStartY + infoHeight)
        
        colorBlack()
        
        # name and ticker of company
        textSize(int(View.stdTextSize * 1.2))
        
        infoItemTitleX = 0.56 * width
        infoItemValueX = 0.64 * width
        infoItemStartY = 0.68 * height
        
        # displays the statistics one-by-one
        text("TICKER:", infoItemTitleX, infoItemStartY + 0.005 * height)
        text(str(self._data.ticker), infoItemValueX, infoItemStartY + 0.005 * height)
        
        text("EXCHANGE:", infoItemTitleX, infoItemStartY + 0.025 * height)
        text(str(self._data.exchange), infoItemValueX, infoItemStartY + 0.025 * height)
        
        textSize(int(View.stdTextSize * 1.3))
        
        text("Simulation Results", infoItemTitleX + 0.015 * width, infoItemStartY + 0.052 * height)
        text("Trading Strategies", infoItemTitleX + 0.172 * width, infoItemStartY + 0.005 * height)
        text("Views", infoItemTitleX + 0.332 * width, infoItemStartY + 0.005 * height)
        
        textSize(int(View.stdTextSize))
        
        # the information shown in the bottom-right display area
        text("STARTING CASH:", infoItemTitleX, infoItemStartY + 0.075 * height)
        text(str(analyzer.cashInitial), infoItemValueX, infoItemStartY + 0.075 * height)
        
        text("CURRENT CASH:", infoItemTitleX, infoItemStartY + 0.095 * height)
        text(str(analyzer.cash), infoItemValueX, infoItemStartY + 0.095 * height)
        
        text("POSITION ($):", infoItemTitleX, infoItemStartY + 0.115 * height)
        text(str(analyzer.positionSize), infoItemValueX, infoItemStartY + 0.115 * height)
        
        text("POSITION (shares):", infoItemTitleX, infoItemStartY + 0.135 * height)
        text(str(analyzer.position), infoItemValueX, infoItemStartY + 0.135 * height)
        
        text("COMMISSION ($):", infoItemTitleX, infoItemStartY + 0.155 * height)
        text(str(analyzer.commissionTotal), infoItemValueX, infoItemStartY + 0.155 * height)
        
        text("P/L ($):", infoItemTitleX, infoItemStartY + 0.175 * height)
        text(str(analyzer.PL), infoItemValueX, infoItemStartY + 0.175 * height)
        
        text("DAYS AGO:", infoItemTitleX, infoItemStartY + 0.195 * height)
        text(str(self._data.timeDays), infoItemValueX, infoItemStartY + 0.195 * height)
        
        
    def checkProfilesClicked(self):
        """
        Checks if any of the profiles contained in this View were clicked.
        
        @rtype: int, 1 for true and 0 for false
        """
        for profile in self.profiles:
            if profile.checkProfileClicked() == 1:
                return 1
                break
        return 0
        
    
    def drawTradeHistory(self):
        """
        Draws the trade history for the simulation on the currently tracked stock
        
        @rtype: None
        """
        tradeLogStartY = self.chartStartY + 0.05 * height
        tradeLogHeight = self.chartHeight - 0.05 * height
        tradeLogTextStartX = self.chartStartX + 0.005 * width
        tradeLogTextStartY = tradeLogStartY + 0.05 * height
        tradeLogTextSize = int(View.stdTextSize * 1.3)
        tradeLogTitleY = tradeLogTextStartY - 0.03 * height
        
        # outer panel and line separators in the trading log
        colorWhite()
        rect(self.chartStartX, tradeLogStartY, self.chartWidth, tradeLogHeight) #Outer box
        line(self.chartStartX, tradeLogStartY + 0.03 * height, self.chartStartX + self.chartWidth, tradeLogStartY + 0.03 * height)
        line(self.chartStartX + 0.04 * self.chartWidth, tradeLogStartY, self.chartStartX + 0.04 * self.chartWidth, tradeLogStartY + tradeLogHeight)
        line(self.chartStartX + 0.20 * self.chartWidth, tradeLogStartY, self.chartStartX + 0.20 * self.chartWidth, tradeLogStartY + tradeLogHeight)
        line(self.chartStartX + 0.25 * self.chartWidth, tradeLogStartY, self.chartStartX + 0.25 * self.chartWidth, tradeLogStartY + tradeLogHeight)
        line(self.chartStartX + 0.30 * self.chartWidth, tradeLogStartY, self.chartStartX + 0.30 * self.chartWidth, tradeLogStartY + tradeLogHeight)
        line(self.chartStartX + 0.39 * self.chartWidth, tradeLogStartY, self.chartStartX + 0.39 * self.chartWidth, tradeLogStartY + tradeLogHeight)
        line(self.chartStartX + 0.48 * self.chartWidth, tradeLogStartY, self.chartStartX + 0.48 * self.chartWidth, tradeLogStartY + tradeLogHeight)
        line(self.chartStartX + 0.60 * self.chartWidth, tradeLogStartY, self.chartStartX + 0.60 * self.chartWidth, tradeLogStartY + tradeLogHeight)
        
        textSize(tradeLogTextSize)
        
        colorBlack()
        
        # titles and criteria in trading log
        text("Tick", tradeLogTextStartX, tradeLogTitleY)
        text("Trading Strategy", tradeLogTextStartX + 0.04 * self.chartWidth, tradeLogTitleY)
        text("Type", tradeLogTextStartX + 0.20 * self.chartWidth, tradeLogTitleY)
        text("Shares", tradeLogTextStartX + 0.25 * self.chartWidth, tradeLogTitleY)
        text("Share Price", tradeLogTextStartX + 0.30 * self.chartWidth, tradeLogTitleY)
        text("Trade Size", tradeLogTextStartX + 0.39 * self.chartWidth, tradeLogTitleY)
        text("Position Size", tradeLogTextStartX + 0.48 * self.chartWidth, tradeLogTitleY)
        text("Trading Strategy information", tradeLogTextStartX + 0.60 * self.chartWidth, tradeLogTitleY)
        
        # draw the title text
        textSize(tradeLogTextSize * 2)
        text("Trading Simulation History", width/2 - (7 * 2 * tradeLogTextSize), 0.05 * height)
        
        # draw the log text
        textSize(tradeLogTextSize)
        
        for tradeIndex in range(len(self._data.tradeLog)):
            if tradeIndex < 66:
                text(self._data.tradeLog[tradeIndex][0] + 1, tradeLogTextStartX, tradeLogTextStartY + tradeLogTextSize * 1.2 * tradeIndex)
                text(self._data.tradeLog[tradeIndex][1], tradeLogTextStartX + 0.04 * self.chartWidth, tradeLogTextStartY + tradeLogTextSize * 1.2 * tradeIndex)
                
                # alternate colors for position type column based on trading type
                if self._data.tradeLog[tradeIndex][2] == "Long":
                    colorGreen()
                elif self._data.tradeLog[tradeIndex][2] == "Short":
                    colorBlue()
                text(self._data.tradeLog[tradeIndex][2], tradeLogTextStartX + 0.20 * self.chartWidth, tradeLogTextStartY + tradeLogTextSize * 1.2 * tradeIndex)
                colorBlack()
                
                text(self._data.tradeLog[tradeIndex][3], tradeLogTextStartX + 0.25 * self.chartWidth, tradeLogTextStartY + tradeLogTextSize * 1.2 * tradeIndex)
                text(self._data.tradeLog[tradeIndex][4], tradeLogTextStartX + 0.30 * self.chartWidth, tradeLogTextStartY + tradeLogTextSize * 1.2 * tradeIndex)
                text(self._data.tradeLog[tradeIndex][5], tradeLogTextStartX + 0.39 * self.chartWidth, tradeLogTextStartY + tradeLogTextSize * 1.2 * tradeIndex)
                text(self._data.tradeLog[tradeIndex][6], tradeLogTextStartX + 0.48 * self.chartWidth, tradeLogTextStartY + tradeLogTextSize * 1.2 * tradeIndex)
                text(self._data.tradeLog[tradeIndex][7], tradeLogTextStartX + 0.60 * self.chartWidth, tradeLogTextStartY + tradeLogTextSize * 1.2 * tradeIndex)
                
    
    def drawBackground(self):
        """
        Fills the background of the screen.
        
        @rtype: None
        """
        fill(220, 220, 220)
        rect(0, 0, width, height)
        colorBlack()
        

def colorWhite():
    fill(255,255,255)
    
def colorGreen():
    fill(0, 255, 0)
    
def colorRed():
    fill(255, 0, 0)
    
def colorBlue():
    fill(0, 0, 255)
    
def colorBlack():
    fill(0, 0, 0)