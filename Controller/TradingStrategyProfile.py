from ClickableProfile import ClickableProfile
from Data import Data
from Analysis import Analysis

class TradingStrategyProfile(ClickableProfile):
    """
    Class responsible for representing and displaying the clickable profile of
    a company or stock.
    """
    
    def __init__ (self, title, strategyIndex, itemCount, viewInstance):
        """
        Adds information specific to this trading strategy to the trading logs.
        
        @type title: the title which the trading strategy can be identified with
        @type strategyIndex: index of this trading strategy in Analysis
        @type count: this item is the count-th of its profile type in the View
        @type viewInstance: the instance of View which created this profile
        @rtype: None
        """
        self.title = title
        self.count = itemCount
        self.viewInstance = viewInstance
        self.strategyIndex = strategyIndex
        
        self.panelWidth = 0.145 * width
        self.panelHeight = 0.024 * height
        self.setupScreenPosition(viewInstance)
        self.data = Data.getInstance()


    def onProfileClicked(self):
        """
        Sets the strategy used in the simulator to the strategy with this
        profile's strategyIndex.
        
        @rtype: None
        """
        analyzer = Analysis.getInstance()
        analyzer.strategy = self.strategyIndex
        data = Data.getInstance()
        data.setDataTimerToReset()
        
    
    def setupScreenPosition(self, viewInstance):
        """
        Sets up the position that this profile will be displayed at on the screen. Called in
        __init__().
        
        @type viewInstance: View, the interface on which this stock will be displayed on
        @rtype: None
        """
        self.panelStartX = viewInstance.chartStartX + 0.68 * width
        self.panelStartY = viewInstance.chartStartY + viewInstance.chartHeight + 0.073 * height + self.count * 0.038 * height
        self.panelEndX = self.panelStartX + self.panelWidth
        self.panelEndY = self.panelStartY + self.panelHeight