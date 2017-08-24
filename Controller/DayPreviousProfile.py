from ClickableProfile import ClickableProfile
from Data import Data
from Analysis import Analysis

class DayPreviousProfile(ClickableProfile):
    """
    Class responsible for representing and displaying the clickable profile of
    a company or stock.
    """
    
    def __init__ (self, title, viewInstance):
        """
        Adds information specific to this trading strategy to the trading logs.
        
        @type title: the title which the profile can be identified with
        @type viewInstance: the instance of View which created this profile
        @rtype: None
        """
        self.title = title
        self.viewInstance = viewInstance
        
        self.panelWidth = 0.065 * width
        self.panelHeight = 0.024 * height
        self.setupScreenPosition(viewInstance)
        self.data = Data.getInstance()


    def onProfileClicked(self):
        """
        Pulls the data from the day before the current day (if existent) and changes the chart.
        
        @rtype: None
        """
        # Google finance maintains data of only the past 14 days
        if (self.data.timeDays <= 14):
            self.data.timeDays += 1
            self.data.timeSinceRefresh = self.data.refreshFrequency - 1
    
    
    def setupScreenPosition(self, viewInstance):
        """
        Sets up the position that this profile will be displayed at on the screen. Called in
        __init__().
        
        @type viewInstance: View, the interface on which this stock will be displayed on
        @rtype: None
        """
        self.panelStartX = viewInstance.chartStartX + 0.68 * width
        self.panelStartY = viewInstance.chartStartY + viewInstance.chartHeight + 0.24 * height
        self.panelEndX = self.panelStartX + self.panelWidth
        self.panelEndY = self.panelStartY + self.panelHeight