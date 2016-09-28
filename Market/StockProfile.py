from ClickableProfile import ClickableProfile
from Data import Data

class StockProfile(ClickableProfile):
    """
    Class responsible for representing and displaying the clickable profile of
    a company or stock.
    """
    
    def __init__ (self, title, exchange, count, viewInstance):
        """
        Adds information specific to this trading strategy to the trading logs.
        
        @type title: the ticker which the stock can be identified with
        @type exchange: the exchange on which the stock is traded
        @type count: this item is the count-th of its profile type in the View
        @type viewInstance: the instance of View which created this profile
        @rtype: None
        """
        self.title = title
        self.exchange = exchange
        self.count = count
        self.viewInstance = viewInstance
        
        self.panelWidth = 0.052 * width
        self.panelHeight = 0.04 * height
        self.setupScreenPosition(viewInstance)
        self.data = Data.getInstance()


    def onProfileClicked(self):
        """
        Handler for when this profile is clicked.
        
        @rtype: None
        """
        self.data.ticker = self.title
        self.data.exchange = self.exchange
        self.data.setDataTimerToReset()
        
    
    def setupScreenPosition(self, viewInstance):
        """
        Sets up the position that this profile will be displayed at on the screen. Called in
        __init__().
        
        @type viewInstance: View, the interface on which this stock will be displayed on
        @rtype: None
        """
        if self.count < 8: 
            # On 1st row of stock ticker panels
            self.panelStartX = viewInstance.chartStartX + self.count * 0.062 * width
            self.panelStartY = viewInstance.chartStartY + viewInstance.chartHeight + 0.03 * height
        elif self.count < 16:
            # On 2nd row of stock ticker panels
            self.panelStartX = viewInstance.chartStartX + (self.count - 8) * 0.062 * width
            self.panelStartY = viewInstance.chartStartY + viewInstance.chartHeight + 0.09 * height
        elif self.count < 24:
            # On 3rd row of stock ticker panels
            self.panelStartX = viewInstance.chartStartX + (self.count - 16) * 0.062 * width
            self.panelStartY = viewInstance.chartStartY + viewInstance.chartHeight + 0.15 * height
        elif self.count < 32:
            # On 4th row of stock ticker panels
            self.panelStartX = viewInstance.chartStartX + (self.count - 24) * 0.062 * width
            self.panelStartY = viewInstance.chartStartY + viewInstance.chartHeight + 0.21 * height
            
        self.panelEndX = self.panelStartX + self.panelWidth
        self.panelEndY = self.panelStartY + self.panelHeight