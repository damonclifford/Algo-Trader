import abc
from Data import Data

class ClickableProfile():
    """
    Clickable profile class which is the parent class for all clickable elements
    in the program.
    """
    
    @abc.abstractmethod
    def __init__ (self):
        """
        Initializes the profile. Abstract method.
        """
        self.title = None
        return;
  
  
    def checkProfileClicked(self):
        """
        Returns whether this profile has been clicked.
        
        @rtype: None
        """
        if (self.panelStartX < mouseX and mouseX < self.panelEndX and 
                self.panelStartY < mouseY and mouseY < self.panelEndY):
            self.onProfileClicked()
            return 1
        return 0


    @abc.abstractmethod
    def onProfileClicked(self):
        """
        Handler for when this profile is clicked. Abstract method.
        
        @rtype: None
        """
        return;
        
    
    @abc.abstractmethod
    def setupScreenPosition(self, viewInstance):
        """
        Sets up the position that this stock will be displayed at on the screen. Called in
        __init__(). Abstract method.
        
        @type viewInstance: View, the interface on which this stock will be displayed on
        @rtype: None
        """
        self.panelStartX = None
        self.panelStartY = None
        self.panelWidth = None
        self.panelHeight = None
        self.panelEndX = self.panelStartX + self.panelWidth
        self.panelEndY = self.panelStartY + self.panelHeight
        return;
            
            
    def drawProfile(self):
        """
        Draws this profile on the screen.
        
        @rtype: None
        """
        if self.mousedOver() == 1:
            fill(150, 255, 150)
        else:
            fill(255, 255, 255)
        rect(self.panelStartX, self.panelStartY, self.panelWidth, self.panelHeight)
        
        fill(0, 0, 0)
        textX = self.panelStartX + 0.003 * width
        textY = self.panelStartY + 0.015 * height
        text(self.title, textX, textY)
        
        
    def mousedOver(self):
        """
        Returns whether a mouse pointer is hovering over this Profile.
        
        @rtype: None
        """
        if (self.panelStartX < mouseX and mouseX < self.panelEndX and 
                self.panelStartY < mouseY and mouseY < self.panelEndY):
            return 1
        return 0