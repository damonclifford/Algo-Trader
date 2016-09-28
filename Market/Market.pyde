import View
from Data import Data
from View import View
from Analysis import Analysis
from SMACrossOverDelayed import SMACrossOverDelayed
from SMACrossOver import SMACrossOver
from SimpleMomentum import SimpleMomentum


def setup():
    """
    Sets up the display for the project.
    
    @rtype: None
    """
    size(1200, 800);
    
        
def draw():
    """
    Repeatedly called to draw the elements of the project. 
    (Think update() in Unity). Serves as the driver of the game as the
    only continuously called function.
    
    @rtype: None
    """
    # get instances of singleton classes
    data = Data.getInstance()
    interface = View.getInstance(width, height)
    analyzer = Analysis.getInstance()
    
    # update interface chart and draw grey background
    interface.updateChart()
    interface.drawBackground()
    
    # selects the strategy
    if analyzer.strategy == 0:   tradingStrategy = SimpleMomentum()
    elif analyzer.strategy == 1: tradingStrategy = SMACrossOver()
    elif analyzer.strategy == 2: tradingStrategy = SMACrossOverDelayed()
        
    # times data refreshes
    while data.timeSinceRefresh == data.refreshFrequency:
        # refresh the stock data and do calculations
        data.refreshStockData()
        analyzer.preAnalysisCalculations()
        tradingStrategy.simulateStrategy()
        analyzer.postAnalysisCalculations()
        data.timeSinceRefresh = 0
    data.timeSinceRefresh += 1
    
    # Mode 1 - show candlestick chart & stock selection interface
    # Mode 2 - show history of simulated trades for current selected stock
    if interface.mode == 0:     interface.drawMainScreen(tradingStrategy)  
    elif interface.mode == 1:   interface.drawHistoryScreen()
        
    # Checks if any cickable profiles are clicked   
    if (mousePressed):
        if interface.checkProfilesClicked() == 1:
            data.timeSinceRefresh = data.refreshFrequency - 1
        