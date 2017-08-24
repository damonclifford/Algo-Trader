from ClickableProfile import ClickableProfile
from Data import Data

class ModeProfile(ClickableProfile):
    """
    Class responsible for representing and displaying the clickable profile of
    a company or stock.
    """
    
    def __init__ (self, title, modeIndex, itemCount, viewInstance):
        """
        Adds information specific to this trading strategy to the trading logs.
        
        @type title: the title which the mode can be identified with
        @type strategyIndex: index of this trading strategy in Analysis
        @type count: this item is the count-th of its profile type in the View
        @type viewInstance: the instance of View which created this profile
        @rtype: None
        """
        self.title = title
        self.count = itemCount
        self.viewInstance = viewInstance
        self.modeIndex = modeIndex
        
        self.panelWidth = 0.0825 * width
        self.panelHeight = 0.0825 * height
        self.setupScreenPosition(viewInstance)
        self.data = Data.getInstance()


    def onProfileClicked(self):
        """
        Sets the strategy used in the simulator to the strategy with this
        profile's strategyIndex.
        
        @rtype: None
        """
        self.viewInstance.mode = self.modeIndex
        self.data.setDataTimerToReset()
        
    
    def setupScreenPosition(self, viewInstance):
        """
        Sets up the position that this profile will be displayed at on the screen. Called in
        __init__().
        
        @type viewInstance: View, the interface on which this stock will be displayed on
        @rtype: None
        """
        self.panelStartX = viewInstance.chartStartX + 0.85 * width
        self.panelStartY = viewInstance.chartStartY + viewInstance.chartHeight + 0.073 * height + self.count * 0.095 * height
        self.panelEndX = self.panelStartX + self.panelWidth
        self.panelEndY = self.panelStartY + self.panelHeight