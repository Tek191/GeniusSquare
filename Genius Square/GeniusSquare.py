""" 
GUI implementation of the Genius Square
This includes functions to:
-Print a grid
-Intialize a grid with blockers
-Generate blockers from a seed
-Validate a move
-Place a piece
-Remove a piece
-Solve a grid
"""
#TODO Check functions for missing parameters, using globals instead currently

import pygame
import sys
import GeniusSquareSolver as ggs
from copy import deepcopy 

#CONSTANTS
X_AXIS_LABELS = ("1", "2", "3", "4", "5", "6")
Y_AXIS_LABELS = ("A", "B", "C", "D", "E", "F")

WORD_PLAY = ("P", "L", "A", "Y")
WORD_SEED = ("S", "E", "E", "D")
WORD_QUIT = ("Q", "U", "I", "T")
WORD_LOADING = ("L", "O", "A", "D", "I", "N", "G")
WORD_TIME = ("T", "I", "M", "E")

FPS = 60

#COLOURS
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREY = (107, 107, 107)
GREEN = (80, 200, 120)
GREEN_LIME = (122, 255, 0)
YELLOW = (248, 255, 0)
DARK_GREEN = (0, 100, 0)
ORANGE_RED = (255, 69, 0)
CYAN = (0, 228, 255)
LIGHT_GREEN =  (152, 251, 152)
CRIMSON_RED = (220, 20, 60)
ORANGE = (255, 95, 31)
NAVY_BLUE = (0, 0, 128)
BRIGHT_BLUE = (0, 150, 255)
VIOLET = (183, 92, 255)

HOVERED = GREEN_LIME
DEFAULT = GREEN
ACTIVE = DARK_GREEN
ERROR = ORANGE_RED

""" 
Default values for the look up table for each default pieces coordinates
dict[int, tuple[int]]
"""
DEFAULT_PLAYER_PIECE_COORDINATES = {
        ggs.SMALL_SQUARE_PIECE_ID: [(1, 9)],
        ggs.BIG_SQUARE_PIECE_ID: [(5, 9), (6, 9), (5, 10), (6, 10)],
        ggs.SHORT_BAR_PIECE_ID: [(2, 9), (2, 10)],
        ggs.BAR_PIECE_ID: [(3, 9), (3, 10), (3, 11)],
        ggs.LONG_BAR_PIECE_ID: [(4, 9), (4, 10), (4, 11), (4, 12)],
        ggs.L_PIECE_ID: [(3, 14), (3, 15), (3, 16), (2, 16)], 
        ggs.T_PIECE_ID: [(1, 14), (1, 15), (1, 16), (2, 15)],
        ggs.Z_PIECE_ID: [(4, 14), (4, 15), (5, 15), (5, 16)],
        ggs.ARROW_PIECE_ID: [(5, 14), (6, 14), (6, 15)]
} 

""" 
Default values for the look up table for each default pieces config
dict[int, int]
"""
DEFAULT_PLAYER_PIECE_CONFIG = {
        ggs.SMALL_SQUARE_PIECE_ID: 0,
        ggs.BIG_SQUARE_PIECE_ID: 0,
        ggs.SHORT_BAR_PIECE_ID: 1,
        ggs.BAR_PIECE_ID: 1,
        ggs.LONG_BAR_PIECE_ID: 1,
        ggs.L_PIECE_ID: 3, 
        ggs.T_PIECE_ID: 4,
        ggs.Z_PIECE_ID: 5,
        ggs.ARROW_PIECE_ID: 7    
}

""" 
Default values for the look up table for each default pieces
dict[int, dict]
"""
DEFAULT_PLAYER_PIECES = {
    ggs.SMALL_SQUARE_PIECE_ID : {
        "ID" : ggs.SMALL_SQUARE_PIECE_ID,
        "coordinates" : DEFAULT_PLAYER_PIECE_COORDINATES[ggs.SMALL_SQUARE_PIECE_ID],
        "config" : DEFAULT_PLAYER_PIECE_CONFIG[ggs.SMALL_SQUARE_PIECE_ID],
        "hoverConfig" : 0,
        "colour" : BRIGHT_BLUE,
        "isSelected" : False,
        "isHovered": False,
        "isPlaced" : False
    },

    ggs.BIG_SQUARE_PIECE_ID : {
        "ID" : ggs.BIG_SQUARE_PIECE_ID,
        "coordinates" : DEFAULT_PLAYER_PIECE_COORDINATES[ggs.BIG_SQUARE_PIECE_ID],
        "config" : DEFAULT_PLAYER_PIECE_CONFIG[ggs.BIG_SQUARE_PIECE_ID],
        "hoverConfig" : 0,
        "colour" : LIGHT_GREEN,
        "isSelected" : False,
        "isHovered": False,
        "isPlaced" : False
    },
    
    ggs.SHORT_BAR_PIECE_ID : {
        "ID" : ggs.SHORT_BAR_PIECE_ID,
        "coordinates" : DEFAULT_PLAYER_PIECE_COORDINATES[ggs.SHORT_BAR_PIECE_ID],
        "config" : DEFAULT_PLAYER_PIECE_CONFIG[ggs.SHORT_BAR_PIECE_ID],
        "hoverConfig" : 0,
        "colour" : CRIMSON_RED,
        "isSelected" : False,
        "isHovered": False,
        "isPlaced" : False
    },
    
    ggs.BAR_PIECE_ID : {
        "ID" : ggs.BAR_PIECE_ID,
        "coordinates" : DEFAULT_PLAYER_PIECE_COORDINATES[ggs.BAR_PIECE_ID],
        "config" : DEFAULT_PLAYER_PIECE_CONFIG[ggs.BAR_PIECE_ID],
        "hoverConfig" : 0,
        "colour" : ORANGE,
        "isSelected" : False,
        "isHovered": False,
        "isPlaced" : False
    },

    ggs.LONG_BAR_PIECE_ID : {
        "ID" : ggs.LONG_BAR_PIECE_ID,
        "coordinates" : DEFAULT_PLAYER_PIECE_COORDINATES[ggs.LONG_BAR_PIECE_ID],
        "config" : DEFAULT_PLAYER_PIECE_CONFIG[ggs.LONG_BAR_PIECE_ID],
        "hoverConfig" : 0,
        "colour" : NAVY_BLUE,
        "isSelected" : False,
        "isHovered": False,
        "isPlaced" : False
    },

    ggs.T_PIECE_ID : {
        "ID" : ggs.T_PIECE_ID,
        "coordinates" : DEFAULT_PLAYER_PIECE_COORDINATES[ggs.T_PIECE_ID],
        "config" : DEFAULT_PLAYER_PIECE_CONFIG[ggs.T_PIECE_ID],
        "hoverConfig" : 0,
        "colour" : YELLOW,
        "isSelected" : False,
        "isHovered": False,
        "isPlaced" : False
    },


    ggs.L_PIECE_ID : {
        "ID" : ggs.L_PIECE_ID,
        "coordinates" : DEFAULT_PLAYER_PIECE_COORDINATES[ggs.L_PIECE_ID],
        "config" : DEFAULT_PLAYER_PIECE_CONFIG[ggs.L_PIECE_ID],
        "hoverConfig" : 0,
        "colour" : CYAN, 
        "isSelected" : False,
        "isHovered": False,
        "isPlaced" : False    
    },
    
    ggs.Z_PIECE_ID : {
        "ID" : ggs.Z_PIECE_ID,
        "coordinates" : DEFAULT_PLAYER_PIECE_COORDINATES[ggs.Z_PIECE_ID],
        "config" : DEFAULT_PLAYER_PIECE_CONFIG[ggs.Z_PIECE_ID],
        "hoverConfig" : 0,
        "colour" : RED, 
        "isSelected" : False,
        "isHovered": False,
        "isPlaced" : False    
    },  

    ggs.ARROW_PIECE_ID : {
        "ID" : ggs.ARROW_PIECE_ID,
        "coordinates" : DEFAULT_PLAYER_PIECE_COORDINATES[ggs.ARROW_PIECE_ID],
        "config" : DEFAULT_PLAYER_PIECE_CONFIG[ggs.ARROW_PIECE_ID],
        "hoverConfig" : 0,
        "colour" : VIOLET, 
        "isSelected" : False,
        "isHovered": False,
        "isPlaced" : False    
    }     
}

def drawRectangleWithBorder(surface: pygame.Surface, colour: tuple[int], x: int, y: int, width: int, height: int, borderWidth: int) -> None:
    """ 
    Four separate rectangles are drawn to achieve the border in the order Top, Bottom, Left, Right 

    Parameters:
        pygame.Surface surface
        TUPLE<INT> colour
        INT x
        INT y
        INT width
        INT height
        INT borderWidth

    Returns:
        None
    """
    pygame.draw.rect(surface, colour, (x, y, width, borderWidth)) 
    pygame.draw.rect(surface, colour, (x, y + height - borderWidth, width, borderWidth))  
    pygame.draw.rect(surface, colour, (x, y, borderWidth, height))  
    pygame.draw.rect(surface, colour, (x + width - borderWidth, y, borderWidth, height)) 

def renderTextInSquare(surface: pygame.Surface, text: str, font: pygame.font, colour: tuple[int], x: int, y: int, squareSize: int) -> None:
    """ 
    Up to two characters can fit in one square

    Parameters:
        pygame.Surface surface
        STRING text
        pygame.font font
        TUPLE<INT> colour
        INT x
        INT y
        INT squareSize

    Returns:
        None
    """
    textSurface = font.render(text, True, colour)
    textRect = textSurface.get_rect(center = (x + squareSize // 2, y + squareSize // 2))
    surface.blit(textSurface, textRect)

def drawFilledSquareWithBorder(surface: pygame.Surface, colour: tuple[int], x: int, y: int, width: int, height: int, borderWidth: int) -> None:
    """ 
    Parameters:
        pygame.Surface surface
        TUPLE<INT> colour
        INT x
        INT y
        INT width
        INT height
        INT borderWidth

    Returns:
        None
    """
    pygame.draw.rect(surface, colour, (x + borderWidth, y + borderWidth, width - 2 * borderWidth, height - 2 * borderWidth))

def drawSideBars(surface: pygame.Surface, colour: tuple[int], width: int, height: int) -> None: 
    """ 
    Draws rectangles either side of the main grid drawn in drawMainGrid

    Parameters:
        pygame.Surface surface
        TUPLE<INT> colour
        INT width
        INT height

    Returns:
        None
    """
    leftRect = pygame.Rect(0, 0, (width - GRID_WIDTH) // 2, height)
    rightRect = pygame.Rect((width + GRID_WIDTH) // 2, 0, (width - GRID_WIDTH) // 2, height)
    pygame.draw.rect(surface, colour, leftRect)
    pygame.draw.rect(surface, colour, rightRect)

def getSquareCoordinates() -> list[list[tuple[int]]]:
    """ 
    Calculates the top left coordinate of each square in the center grid.
    Returns a 2D list of tuples containing an X and Y coordinate.

    Parameters:
        None

    Returns:
        LIST<LIST<TUPLE<INT, INT>>> allSquares
    """
    allSquares = [] 
    for y in range(TOTAL_SQUARES): 
        allSquares.append([])
        for x in range(TOTAL_SQUARES): 
            xCoordinate = ((width - GRID_WIDTH) // 2) + (y * SQUARE_SIZE)
            yCoordinate = ((height - GRID_WIDTH) // 2) + (x * SQUARE_SIZE)
            allSquares[y].append((xCoordinate, yCoordinate))
            
    return allSquares

def drawMainGrid(surface: pygame.Surface, colour: tuple[int], allSquares: list[list[tuple[int, int]]]) -> None:
    """ 
    Draws the center grid

    Parameters:
        pygame.Surface surface
        TUPLE<INT> colour
        LIST<LIST<TUPLE<INT, INT>>> allSquares

    Returns:
        None
    """
    for y in range(TOTAL_SQUARES):  
        for x in range(TOTAL_SQUARES):  
            drawRectangleWithBorder(surface, colour, allSquares[x][y][0], allSquares[x][y][1], SQUARE_SIZE, SQUARE_SIZE, BORDER_WIDTH)  

def drawDividerLines(surface: pygame.Surface, allSquares: list[list[tuple[int, int]]]) -> None:
    """ 
    Draws two vertical lines down the middle of the center grid

    Parameters:
        pygame.Surface surface
        LIST<LIST<TUPLE<INT, INT>>> allSquares

    Returns:
        None
    """
    for y in range(0, TOTAL_SQUARES): 
        drawFilledSquareWithBorder(surface, GREEN, allSquares[8][0][0], allSquares[8][y][1], SQUARE_SIZE, SQUARE_SIZE, BORDER_WIDTH)   
        drawFilledSquareWithBorder(surface, GREEN, allSquares[9][0][0], allSquares[9][y][1], SQUARE_SIZE, SQUARE_SIZE, BORDER_WIDTH)   

def drawTimer(surface: pygame.Surface, allSquares: list[list[tuple[int, int]]], time: int) -> None:
    """ 
    Draws the timer above the player grid

    Parameters:
        pygame.Surface surface
        LIST<LIST<TUPLE<INT, INT>>> allSquares

    Returns:
        None
    """
    for i in range(0, 4):
        renderTextInSquare(surface, WORD_TIME[i], font, GREEN,  allSquares[i][0][0], allSquares[i][0][1], SQUARE_SIZE)  
    renderTextInSquare(surface, ":", font, GREEN,  allSquares[i + 1][0][0], allSquares[i + 1][0][1], SQUARE_SIZE)  

    strTime = str(time)
    for j in range(len(strTime)):
        renderTextInSquare(surface, strTime[j], font, GREEN,  allSquares[j + 5][0][0], allSquares[j + 5][0][1], SQUARE_SIZE)
    
def drawGameBoardGrid(surface: pygame.Surface, allSquares: list[list[tuple[int, int]]]) -> None:
    """ 
    Draws both the players' and the Computer's grids

    Parameters:
        pygame.Surface surface
        LIST<LIST<TUPLE<INT, INT>>> allSquares

    Returns:
        None
    """
    for x in range(0, 6): 
        for y in range (0, 6): 
            drawRectangleWithBorder(surface, WHITE, allSquares[x + 1][1][0], allSquares[0][y + 2][1], SQUARE_SIZE, SQUARE_SIZE, BORDER_WIDTH) 
            drawRectangleWithBorder(surface, WHITE, allSquares[x + 11][1][0], allSquares[16][y + 2][1], SQUARE_SIZE, SQUARE_SIZE, BORDER_WIDTH) 

def drawGameBoardGridMainMenu(surface: pygame.Surface, allSquares: list[list[tuple[int, int]]]) -> None:
    """ 
    Draws a grid on the right handside of the center grid

    Parameters:
        pygame.Surface surface
        LIST<LIST<TUPLE<INT, INT>>> allSquares

    Returns:
        None
    """
    for x in range(0, 6): 
        for y in range (0, 6): 
            drawRectangleWithBorder(surface, WHITE, allSquares[x + 11][1][0], allSquares[16][y + 2][1], SQUARE_SIZE, SQUARE_SIZE, BORDER_WIDTH) 
 
def drawGameBoardGridLoadingScreen(surface: pygame.Surface, allSquares: list[list[tuple[int, int]]]) -> None:
    """ 
    Draws the grid in the center of the center grid

    Parameters:
        pygame.Surface surface
        LIST<LIST<TUPLE<INT, INT>>> allSquares

    Returns:
        None
    """
    for x in range(0, 6): 
        for y in range (0, 6): 
            drawRectangleWithBorder(surface, WHITE, allSquares[x + 6][1][0], allSquares[9][y + 2][1], SQUARE_SIZE, SQUARE_SIZE, BORDER_WIDTH) 

def drawGameBoardGridLabels(surface: pygame.Surface, allSquares: list[list[tuple[int, int]]]) -> None:
    """ 
    Labels the coordinates, numeric X and alphabetical Y for both the player and computer

    Parameters:
        pygame.Surface surface
        LIST<LIST<TUPLE<INT, INT>>> allSquares

    Returns:
        None
    """
    for i in range(0, 6):
        renderTextInSquare(surface,  X_AXIS_LABELS[i], font, WHITE, allSquares[i + 1][1][0], allSquares[i + 1][1][1], SQUARE_SIZE)
        renderTextInSquare(surface, Y_AXIS_LABELS[i], font, WHITE, allSquares[0][i + 2][0], allSquares[0][i + 2][1], SQUARE_SIZE)
        
        renderTextInSquare(surface,  X_AXIS_LABELS[-i - 1], font, WHITE, allSquares[i + 11][1][0], allSquares[i + 11][1][1], SQUARE_SIZE)
        renderTextInSquare(surface, Y_AXIS_LABELS[i], font, WHITE, allSquares[17][i + 2][0], allSquares[17][i + 2][1], SQUARE_SIZE)

def drawGameBoardGridLabelsMainMenu(surface: pygame.Surface, allSquares: list[list[tuple[int, int]]]) -> None:
    """ 
    Labels the coordinates, numeric X and alphabetical Y for the right handside grid in the center grid

    Parameters:
        pygame.Surface surface
        LIST<LIST<TUPLE<INT, INT>>> allSquares

    Returns:
        None
    """
    for i in range(0, 6):
        renderTextInSquare(surface, X_AXIS_LABELS[i], font, WHITE, allSquares[i + 11][1][0], allSquares[i + 11][1][1], SQUARE_SIZE)
        renderTextInSquare(surface, Y_AXIS_LABELS[i], font, WHITE, allSquares[10][i + 2][0], allSquares[10][i + 2][1], SQUARE_SIZE)

def drawGameBoardGridLabelsLoadingScreen(surface: pygame.Surface, allSquares: list[list[tuple[int, int]]]) -> None:
    """ 
    Labels the coordinates, numeric X and alphabetical Y for the center grid

    Parameters:
        pygame.Surface surface
        LIST<LIST<TUPLE<INT, INT>>> allSquares

    Returns:
        None
    """
    for i in range(0, 6):
        renderTextInSquare(surface, X_AXIS_LABELS[i], font, WHITE, allSquares[i + 6][1][0], allSquares[i + 6][1][1], SQUARE_SIZE)
        renderTextInSquare(surface, Y_AXIS_LABELS[i], font, WHITE, allSquares[5][i + 2][0], allSquares[5][i + 2][1], SQUARE_SIZE)

def isWithinArea(pos: tuple[int, int], x: int, y: int, width: int, height: int) -> bool:
    """ 
    Defined by the top left point of a square, checks if mouse cursor is present within square.

    Parameters:
        TUPLE<INT, INT> pos 
        INT x
        INT y
        INT width
        INT height
        
    Returns:
        BOOL
    """
    return x <= pos[0] <= x + width and y <= pos[1] <= y + height

def getClipboardAsAlphaNumericText() -> str: 
    """ 
    Gets clipboard input and removes all characters not a-z, A-Z or 0-9.
    Extra space character at the end of the clipboard output requires manual remove via [:-1]

    Parameters:
        None

    Returns:
        STRING, if string exists
        None, otherwise
    """
    clipboardText = pygame.scrap.get(pygame.SCRAP_TEXT)
    if clipboardText:     
        clipboardText = clipboardText.decode("utf-8").replace('\x00', ' ')[:-1] #Remove extra character at the end
        if clipboardText.isalnum(): 
            return clipboardText
        
    return None  

def handleTextBoxClipboardInput(text: str, maxLength: int) -> str:
    """
    Collects and validates clipboard input

    Parameters:
        STRING text
        INT maxLength

    Returns:
        STRING text
    """
    clipboardText = getClipboardAsAlphaNumericText()
    if clipboardText:
        if len(text) + len(clipboardText) <= maxLength:
            text += clipboardText
    return text

def handleQuitButton(surface: pygame.Surface, allSquares: list[list[tuple[int, int]]], mousePos: tuple[int, int], stateLeftClick: bool) -> bool:
    """ 
    The quit button can be:
    Hovered
    Clicked

    When clicked it returns a bool for the running variable to exit the program

    Parameters:
        pygame.Surface surface
        LIST<LIST<TUPLE<INT, INT>>> allSquares    
        TUPLE<INT, INT> mousePos
        BOOL stateLeftClick

    Returns:
        BOOL
    """
    isHoveringQuit = False
    for i in range(0, 4):
        if isWithinArea(mousePos, allSquares[i + 7][16][0], allSquares[i + 7][16][1], SQUARE_SIZE, SQUARE_SIZE):
            isHoveringQuit = True 
            break
    
    if stateLeftClick and isHoveringQuit:
        return False
    
    for j in range(0, 4):
        renderTextInSquare(surface, WORD_QUIT[j], font, WHITE,  allSquares[j + 7][15][0], allSquares[j + 7][15][1], SQUARE_SIZE)
        
        if isHoveringQuit:
            drawFilledSquareWithBorder(surface, HOVERED, allSquares[j + 7][16][0], allSquares[j + 7][16][1], SQUARE_SIZE, SQUARE_SIZE, BORDER_WIDTH)
        else:
            drawFilledSquareWithBorder(surface, DEFAULT, allSquares[j + 7][16][0], allSquares[j + 7][16][1], SQUARE_SIZE, SQUARE_SIZE, BORDER_WIDTH)
    
    return True

def handleSeedTextBox(surface: pygame.Surface, allSquares: list[list[tuple[int, int]]], mousePos: tuple[int, int], isMainMenuSeedTextBoxActive: bool, mainMenuSeedTextBoxString: str, inputChar: str, validDieFaces: list[tuple[bool, int]]) -> tuple[str, str]:
    """ 
    The seed text box can be:
    Hovered
    Clicked
    Collect keyboard input
    Collect Clipboard input

    Parameters:
        pygame.Surface surface
        LIST<LIST<TUPLE<INT, INT>>> allSquares    
        TUPLE<INT, INT> mousePos
        BOOL isMainMenuSeedTextBoxActive
        STRING mainMenuSeedTextBoxString
        STRING inputChar
        LIST<TUPLE<BOOL, INT>> validDieFaces

    Returns:
        TUPLE<BOOL isMainMenuSeedTextBoxActive, STR mainMenuSeedTextBoxString>
    """
    isHoveringSeed = False 
    for k in range(0, 14):
        if isWithinArea(mousePos, allSquares[k + 2][14][0], allSquares[k + 2][14][1], SQUARE_SIZE, SQUARE_SIZE):
            isHoveringSeed = True 
            break               
    
    if not isMainMenuSeedTextBoxActive and stateLeftClick and isHoveringSeed:
        isMainMenuSeedTextBoxActive = True
    elif isMainMenuSeedTextBoxActive and stateLeftClick and not isHoveringSeed:
        isMainMenuSeedTextBoxActive = False
    
    if isMainMenuSeedTextBoxActive and isinstance(inputChar, str) and len(mainMenuSeedTextBoxString) < 14:
        mainMenuSeedTextBoxString += inputChar.upper()
    
    for i in range(0, 4):
        renderTextInSquare(surface, WORD_SEED[i], font, WHITE,  allSquares[i + 7][13][0], allSquares[i + 7][13][1], SQUARE_SIZE)
    
    for j in range(0, 14):
        if not isMainMenuSeedTextBoxActive and isHoveringSeed:
            drawFilledSquareWithBorder(surface, HOVERED, allSquares[j + 2][14][0], allSquares[j + 2][14][1], SQUARE_SIZE, SQUARE_SIZE, BORDER_WIDTH)
        elif isMainMenuSeedTextBoxActive:
            drawFilledSquareWithBorder(surface, ACTIVE, allSquares[j + 2][14][0], allSquares[j + 2][14][1], SQUARE_SIZE, SQUARE_SIZE, BORDER_WIDTH) 
        else:
            drawFilledSquareWithBorder(surface, DEFAULT, allSquares[j + 2][14][0], allSquares[j + 2][14][1], SQUARE_SIZE, SQUARE_SIZE, BORDER_WIDTH)    
            
        if len(mainMenuSeedTextBoxString) != 0 and j < len(mainMenuSeedTextBoxString):
            if not validDieFaces[j // 2][0]:
                renderTextInSquare(surface, mainMenuSeedTextBoxString[j], font, ORANGE_RED, allSquares[j + 2][14][0], allSquares[j + 2][14][1], SQUARE_SIZE)
            else:
                renderTextInSquare(surface, mainMenuSeedTextBoxString[j], font, WHITE, allSquares[j + 2][14][0], allSquares[j + 2][14][1], SQUARE_SIZE)
    
    return isMainMenuSeedTextBoxActive, mainMenuSeedTextBoxString

def handlePlayButton(surface: pygame.Surface, allSquares: list[list[tuple[int, int]]], seed: str, isSeedValueValid: bool, mousePos: tuple[int, int], stateLeftClick: bool) -> tuple[int, bool]:
    """ 
    The play button can be:
    Hovered
    Clicked

    The button changes colour depending on whether the seed is valid or not.

    Parameters:
        pygame.Surface surface
        LIST<LIST<TUPLE<INT, INT>>> allSquares    
        STRING seed
        BOOL isSeedValueValid
        TUPLE<INT, INT> mousePos
        BOOL stateLeftClick

    Returns:
        TUPLE<INT, BOOL>
    """
    isHoveringPlay = False
    for i in range(0, 4):
        if isWithinArea(mousePos, allSquares[i + 7][10][0], allSquares[i + 7][10][1], SQUARE_SIZE, SQUARE_SIZE):
            isHoveringPlay = True 
            break
    
    if seed == "" or isSeedValid(seed):
        isSeedValueValid = True 
    else:
        isSeedValueValid = False
    
    for i in range(0, 4):
        renderTextInSquare(surface, WORD_PLAY[i], font, WHITE,  allSquares[i + 7][9][0], allSquares[i + 7][9][1], SQUARE_SIZE)
        if isHoveringPlay and isSeedValueValid:
            drawFilledSquareWithBorder(surface, HOVERED, allSquares[i + 7][10][0], allSquares[i + 7][10][1], SQUARE_SIZE, SQUARE_SIZE, BORDER_WIDTH)
        elif isSeedValueValid:
            drawFilledSquareWithBorder(surface, DEFAULT, allSquares[i + 7][10][0], allSquares[i + 7][10][1], SQUARE_SIZE, SQUARE_SIZE, BORDER_WIDTH)
        else:
            drawFilledSquareWithBorder(surface, ERROR, allSquares[i + 7][10][0], allSquares[i + 7][10][1], SQUARE_SIZE, SQUARE_SIZE, BORDER_WIDTH)
            
    if stateLeftClick and isHoveringPlay:
        if isSeedValueValid:
            return 1, True      
    
    return 0, isSeedValueValid

def handleTimeButton(surface: pygame.Surface, allSquares: list[list[tuple[int, int]]], timeState: int, mousePos: tuple[int, int], stateLeftClick: bool, isSafeToToggleTime: bool) -> tuple[int, bool]:
    """ 
    The time button can be:
    Hovered
    Clicked

    The button changes the time when it is clicked.
    0 - 180
    1 -  90
    2 -  45

    Parameters:
        pygame.Surface surface
        LIST<LIST<TUPLE<INT, INT>>> allSquares    
        INT timeState
        TUPLE<INT, INT> mousePos
        BOOL stateLeftClick
        BOOL isSafeToToggleTime

    Returns:
        TUPLE<INT, BOOL>
    """
    for i in range(0, 4):
        renderTextInSquare(surface, WORD_TIME[i], font, WHITE,  allSquares[i + 7][11][0], allSquares[i + 7][11][1], SQUARE_SIZE)    

    isHoveringTime = False 
    for j in range(0, 4):
        if isWithinArea(mousePos, allSquares[j + 7][12][0], allSquares[j + 7][12][1], SQUARE_SIZE, SQUARE_SIZE):
            isHoveringTime = True 
            break 
    
    if stateLeftClick and isHoveringTime and isSafeToToggleTime:
        match timeState:
            case 0:
                timeState = 1
            case 1:
                timeState = 2
            case 2:
                timeState = 0
                
        isSafeToToggleTime = False
    
    for k in range(0, 4):
        if isHoveringTime:
            drawFilledSquareWithBorder(surface, HOVERED, allSquares[k + 7][12][0], allSquares[k + 7][12][1], SQUARE_SIZE, SQUARE_SIZE, BORDER_WIDTH)
        else:
            drawFilledSquareWithBorder(surface, DEFAULT, allSquares[k + 7][12][0], allSquares[k + 7][12][1], SQUARE_SIZE, SQUARE_SIZE, BORDER_WIDTH)

    match timeState:
        case 0:
            renderTextInSquare(surface, "1", font, WHITE,  allSquares[7][12][0], allSquares[7][12][1], SQUARE_SIZE) 
            renderTextInSquare(surface, "8", font, WHITE,  allSquares[8][12][0], allSquares[8][12][1], SQUARE_SIZE) 
            renderTextInSquare(surface, "0", font, WHITE,  allSquares[9][12][0], allSquares[9][12][1], SQUARE_SIZE) 
        case 1:
            renderTextInSquare(surface, "9", font, WHITE,  allSquares[8][12][0], allSquares[8][12][1], SQUARE_SIZE) 
            renderTextInSquare(surface, "0", font, WHITE,  allSquares[9][12][0], allSquares[9][12][1], SQUARE_SIZE) 
        case 2:
            renderTextInSquare(surface, "4", font, WHITE,  allSquares[8][12][0], allSquares[8][12][1], SQUARE_SIZE) 
            renderTextInSquare(surface, "5", font, WHITE,  allSquares[9][12][0], allSquares[9][12][1], SQUARE_SIZE) 
                        
    return timeState, isSafeToToggleTime

def isSeedValid(seed: str) -> bool:
    """ 
    Checks if a seed 
    Exists
    Is a string
    Matches A-F followed by 1-6, 7 times
    Each die faces matches respective die

    Parameters:
        STRING seed

    Returns:
        BOOL
    """
    if (seed is None or not isinstance(seed, str) or not ggs.re.match(r'^([A-F][1-6]){7}$', seed)):
        return False

    for i in range(0, 14, 2):
        if seed[i] + seed[i + 1] not in ggs.ALL_DICE[i // 2]:
            return False 
    
    return True

def drawDieFaces(surface: pygame.Surface, allSquares: list[list[tuple[int, int]]], seed: str, validDieFaces: list[tuple[bool, int]]) -> None: 
    """ 
    Draws each die face in the left grid of the center grid.
    The valid seed values are green instead of white to highlight them.

    Parameters:
        pygame.Surface surface
        LIST<LIST<TUPLE<INT, INT>>> allSquares
        STRING seed
        LIST<TUPLE<BOOL, INT>> validDieFaces

    Returns:
        None
    """
    for j in range(0, 7):
        renderTextInSquare(surface, "D" + str(j + 1), font, GREEN, allSquares[j + 1][1][0], allSquares[j + 1][1][1], SQUARE_SIZE)
        for i in range(0, 6):
            if (j * 2) + 1 < len(seed) and validDieFaces[j][0] and validDieFaces[j][1] == i:
                renderTextInSquare(surface, ggs.ALL_DICE[j][i], font, GREEN_LIME, allSquares[j + 1][i + 2][0], allSquares[j + 1][i + 2][1], SQUARE_SIZE)
            else:
                renderTextInSquare(surface, ggs.ALL_DICE[j][i], font, WHITE, allSquares[j + 1][i + 2][0], allSquares[j + 1][i + 2][1], SQUARE_SIZE)
         
def getValidDieFaces(seed: str) -> list[tuple[bool, int]]:
    """ 
    Checks which seed values are valid

    Parameters:
        STRING seed

    Returns:
        None
    """  
    if len(seed) < 2:
        return [(False, 0), (False, 0), (False, 0), (False, 0), (False, 0), (False, 0), (False, 0)] 

    dieFaceStates = [(False, 0), (False, 0), (False, 0), (False, 0), (False, 0), (False, 0), (False, 0)] 
    for i in range(0, len(seed), 2): 
        if i + 1 < len(seed) and seed[i] + seed[i + 1] in ggs.ALL_DICE[i // 2]:
            dieFaceStates[i // 2] = (True, ggs.ALL_DICE[i // 2].index(seed[i] + seed[i + 1]))
    
    return dieFaceStates

def drawMainMenuBlockers(surface: pygame.Surface, allSquares: list[list[tuple[int, int]]], validDieFaces: list[tuple[bool, int]]) -> None:
    """ 
    Draws the blockers on the grid on the right handside of the center grid

    Parameters:
        pygame.Surface surface
        LIST<LIST<TUPLE<INT, INT>>> allSquares
        STRING seed
        LIST<TUPLE<BOOL, INT>> validDieFaces

    Returns:
        None
    """ 
    for i in range(0, 7):
        if validDieFaces[i][0]:
            j = validDieFaces[i][1]
            x, y = ggs.getDieFaceCoordinates(ggs.ALL_DICE[i][j])
            renderTextInSquare(surface, "O", font, ORANGE_RED, allSquares[x + 11][y + 2][0], allSquares[x + 11][y + 2][1], SQUARE_SIZE)  

def drawLoadingScreenBlockers(surface: pygame.Surface, allSquares: list[list[tuple[int, int]]], validDieFaces: list[tuple[bool, int]]) -> None:
    """ 
    Draws the blockers on the grid in the center grid of the center grid

    Parameters:
        pygame.Surface surface
        LIST<LIST<TUPLE<INT, INT>>> allSquares
        LIST<TUPLE<BOOL, INT>> validDieFaces

    Returns:
        None
    """ 
    for i in range(0, 7):
        if validDieFaces[i][0]:
            j = validDieFaces[i][1]
            x, y = ggs.getDieFaceCoordinates(ggs.ALL_DICE[i][j])
            renderTextInSquare(surface, "O", font, ORANGE_RED, allSquares[x + 6][y + 2][0], allSquares[x + 6][y + 2][1], SQUARE_SIZE)  

def drawLoadingScreen(surface: pygame.Surface, allSquares: list[list[tuple[int, int]]], seed: str) -> None:
    """ 
    Handles drawing the text and squares for the loading screen.

    Parameters:
        pygame.Surface surface
        LIST<LIST<TUPLE<INT, INT>>> allSquares
        STRING seed

    Returns:
        None
    """
    for i in range(0, 7):
        renderTextInSquare(surface, WORD_LOADING[i], font, WHITE,  allSquares[i + 5][9][0], allSquares[i + 5][9][1], SQUARE_SIZE)
    renderTextInSquare(surface, "!", font, WHITE,  allSquares[i + 6][9][0], allSquares[i + 6][9][1], SQUARE_SIZE)   
            
    for j in range(0, 14):
        renderTextInSquare(surface, seed[j], font, GREEN, allSquares[j + 2][12][0], allSquares[j + 2][12][1], SQUARE_SIZE)
    
    for k in range(0, 4):
        renderTextInSquare(surface, WORD_SEED[k], font, WHITE,  allSquares[k + 7][11][0], allSquares[k + 7][11][1], SQUARE_SIZE)

def drawGameBoardBlockers(surface: pygame.Surface, allSquares: list[list[tuple[int, int]]], validDieFaces: list[tuple[bool, int]]) -> None:
    """ 
    Draws the blockers on both the players' and computer's grids on the center grid

    Parameters:
        pygame.Surface surface
        LIST<LIST<TUPLE<INT, INT>>> allSquares
        LIST<TUPLE<BOOL, INT>> validDieFaces

    Returns:
        None
    """
    for i in range(0, 7):
        if validDieFaces[i][0]:
            j = validDieFaces[i][1]
            x, y = ggs.getDieFaceCoordinates(ggs.ALL_DICE[i][j])
            renderTextInSquare(surface, "O", font, ORANGE_RED, allSquares[x + 1][1][0], allSquares[0][y + 2][1], SQUARE_SIZE)      
            renderTextInSquare(surface, "O", font, ORANGE_RED, allSquares[16 - x][1][0], allSquares[16][y + 2][1], SQUARE_SIZE)      

def updatePieceRotation(pieceID: int, config: int) -> int: 
    """ 
    Takes the current configuration of a piece and returns the configuration after a single 90 degree clockwise rotation

    Parameters:
    INT pieceID
    INT config 

    Returns:
        int config
        int
    """
    match pieceID:
        case 0:
            return config
        case 1:
            return config
        case 2:
            match config:
                case 0:
                    return 1
                case 1:
                    return 0
        case 3:
            match config:
                case 0:
                    return 1
                case 1:
                    return 0
        case 4:
            match config:
                case 0:
                    return 1
                case 1:
                    return 0
        case 5:
            match config:
                case 3:
                    return 4
                case 4:
                    return 9
                case 9:
                    return 12
                case 12:
                    return 3
                case 16:
                    return 20
                case 20:
                    return 24
                case 24:
                    return 29
                case 29:
                    return 16
        case 6:
            match config:
                case 4:
                    return 9
                case 9:
                    return 14
                case 14:
                    return 0
                case 0:
                    return 4
        case 7:
            match config:
                case 5:
                    return 13
                case 13:
                    return 5
                case 1:
                    return 9
                case 9:
                    return 1
        case 8:
            match config:
                case 7:
                    return 10
                case 10:
                    return 0
                case 0:
                    return 4
                case 4:
                    return 7 

def updatePieceReflection(pieceID: int, config: int) -> int: 
    """ 
    Takes the current configuration of a piece and returns the configuration after a reflection in the y axis

    Parameters:
    INT pieceID
    INT config 

    Returns:
        int config
        int
    """
    match pieceID:
        case 0:
            return config
        case 1:
            return config
        case 2:
            return config
        case 3:
            return config
        case 4:
            return config
        case 5:
            match config:
                case 3:
                    return 16
                case 4:
                    return 20
                case 9:
                    return 24
                case 12:
                    return 29
                case 16:
                    return 3
                case 20:
                    return 4
                case 24:
                    return 9
                case 29:
                    return 12         
        case 6:
            match config:
                case 4:
                    return 14
                case 9:
                    return 9
                case 14:
                    return 4
                case 0:
                    return 0
        case 7:
            match config:
                case 5:
                    return 1
                case 13:
                    return 9
                case 1:
                    return 5 
                case 9:
                    return 13
        case 8:
            match config:
                case 7:
                    return 4
                case 10:
                    return 0
                case 0:
                    return 10
                case 4:
                    return 7 

def isWithinPlayerGrid(mousePos: tuple[int, int], allSquares: list[list[tuple[int, int]]]) -> bool: 
    """ 
    Uses isWithinArea and is no different other than hard coding the values to make the code easier to read

    Parameters:
    TUPLE<INT, INT> mousePos
    LIST<LIST<TUPLE<INT, INT>>> allSquares    

    Returns:
        bool
    """
    return isWithinArea(mousePos, allSquares[1][2][0], allSquares[1][2][1], allSquares[7][8][0] - allSquares[1][2][0], allSquares[7][8][1] - allSquares[1][2][1])

def updatePieceOrientation(piece: dict, rotate: bool, reflect: bool) -> int: 
    """ 
    Updates a piece's configuration after a rotation and reflection.

    Parameters:
    DICT piece
    BOOL rotate
    BOOL reflect    

    Returns:
        int piece["config"]
    """    
    if rotate:
        piece["config"] = updatePieceRotation(piece["ID"], piece["config"])

    if reflect:
        piece["config"] = updatePieceReflection(piece["ID"], piece["config"])    
    
    return piece["config"]

def getMouseCoordinatesOnMainGrid(mousePos: tuple[int, int], width: int, height: int) -> tuple[int, int]: 
    """ 
    Translates the raw mouse coordinates into the coordinates on the center grid

    Parameters:
    TUPLE<INT, INT> mousePos
    INT width
    INT height
    
    Returns:
        TUPLE<INT, INT> (x, y)
    """  
    x = (mousePos[0] - ((width - GRID_WIDTH) // 2)) // SQUARE_SIZE 
    y = (mousePos[1] - ((height - GRID_WIDTH) // 2)) // SQUARE_SIZE 
    return x, y

def drawPiece(piece: dict, pieceCoordinates: dict[int, tuple[int, int]]) -> None: 
    """ 
    Renders a given piece based on its configuration

    Parameters:
    DICT piece
    DICT<INT TUPLE<INT, INT>> pieceCoordinates
    
    Returns:
        None
    """     
    if piece["isSelected"]:
        colour = ACTIVE 
    elif piece["isHovered"]:
        colour = HOVERED
    else:
        colour = piece["colour"]
    
    yOffset = 0
    xOffset = 0
    if piece["isPlaced"]:
        allCoordinates = pieceCoordinates[piece["ID"]]
        yOffset = 2
        xOffset = 1
    else:
        allCoordinates = DEFAULT_PLAYER_PIECE_COORDINATES[piece["ID"]]
        
    for coordinates in allCoordinates:
        drawFilledSquareWithBorder(screen, colour, allSquares[coordinates[0] + xOffset][coordinates[1] + xOffset][0], allSquares[coordinates[0] + yOffset][coordinates[1] + yOffset][1], SQUARE_SIZE, SQUARE_SIZE, BORDER_WIDTH)

def drawPieceHover(piece: dict, pieceCoordinates: dict[int, tuple[int, int]], grid: list[list[int, int]], x: int, y: int) -> None: 
    """ 
    Renders a given piece hovering at a specific coordinate based on its configuration 

    Parameters:
    DICT piece
    DICT<INT TUPLE<INT, INT>> pieceCoordinates
    LIST<LIST<INT, INT>> grid
    INT x
    INT y
    
    
    Returns:
        None
    """     
    copyGrid = deepcopy(grid)
    copyPieceCoordinates = deepcopy(pieceCoordinates)
    copyPiece = deepcopy(piece)
    copyGrid, copyPieceCoordinates = ggs.placePieceOnGrid(copyGrid, copyPieceCoordinates, copyPiece["ID"], x, y, copyPiece["hoverConfig"])
    copyPiece["isPlaced"] = True
    copyPiece["isHovered"] = True
    copyPiece["isSelected"] = False
    drawPiece(copyPiece, copyPieceCoordinates)

def drawPieceAI(piece: dict, pieceCoordinates: dict[int, tuple[int, int]]) -> None: 
    """ 
    Draws a piece for the AIs grid

    Parameters:
    DICT piece
    DICT<INT TUPLE<INT, INT>> pieceCoordinates
    
    Returns:
        None
    """   
    colour = piece["colour"]
    yOffset = 0
    xOffset = 0
    if piece["isPlaced"]:
        allCoordinates = pieceCoordinates[piece["ID"]]
        yOffset = 2
        xOffset = 11 #1 + 10, 10 translated onto AI grid
    else:
        allCoordinates = DEFAULT_PLAYER_PIECE_COORDINATES[piece["ID"]]

    for coordinates in allCoordinates:
        drawFilledSquareWithBorder(screen, colour, allSquares[coordinates[0] + xOffset][coordinates[1] + xOffset][0], allSquares[coordinates[0] + yOffset][coordinates[1] + yOffset][1], SQUARE_SIZE, SQUARE_SIZE, BORDER_WIDTH)

def isWithinPiece(mousePos: tuple[int, int], piece: dict, pieceCoordinates: dict[int, tuple[int, int]]) -> bool: 
    """ 
    Checks if the mouse is within any square of a given piece

    Parameters:
        TUPLE<INT, INT> mousePos 
        DICT piece
        DICT<INT TUPLE<INT, INT>> pieceCoordinates
        
    Returns:
        BOOL
    """
    yOffset = 0
    xOffset = 0
    if piece["isPlaced"]:
        allCoordinates = pieceCoordinates[piece["ID"]]
        yOffset = 2
        xOffset = 1
    else:
        allCoordinates = DEFAULT_PLAYER_PIECE_COORDINATES[piece["ID"]]
    
    for coordinates in allCoordinates:
        if isWithinArea(mousePos, allSquares[coordinates[0] + xOffset][coordinates[1] + xOffset][0], allSquares[coordinates[0] + yOffset][coordinates[1] + yOffset][1], SQUARE_SIZE, SQUARE_SIZE):
            return True

    return False

def handlePieceInteraction(grid: list[list[int, int]], pieceCoordinates: dict[int, tuple[int, int]], piece: dict, isRotatingPiece: bool, isReflectingPiece: bool, isRemovingPiece: bool, width: int, height: int) -> tuple[list[list[int, int]], dict[int, tuple[int, int]], dict]:
    """ 
    1: Change the orientation of piece
    2: Check if the piece is hovered over the player grid and either place or hover the piece
    3: 2 but for already placed piece
    4: Handle piece removal
    5: Handle logic behind selection/hovering of a piece
    6: Draw the piece

    Parameters:
        LIST<LIST<INT, INT>> grid
        DICT<INT TUPLE<INT, INT>> pieceCoordinates
        DICT piece
        BOOL isRotatingPiece
        BOOL isReflectingPiece
        BOOL isRemovingPiece
        INT width
        INT height
        
    Returns:
        TUPLE<LIST<LIST<INT, INT>> grid, DICT<INT TUPLE<INT, INT>> pieceCoordinates, DICT piece>
    """
    #1
    if piece["isSelected"]:
        piece["hoverConfig"] = updatePieceOrientation(piece, isRotatingPiece, isReflectingPiece)
          
    #2
    if not piece["isPlaced"] and piece["isSelected"] and isWithinPlayerGrid(mousePos, allSquares):
        x, y = getMouseCoordinatesOnMainGrid(mousePos, width, height)
        yPlayerGrid = y - 2
        xPlayerGrid = x - 1
        
        if ggs.isMoveValid(grid, piece["ID"], xPlayerGrid, yPlayerGrid, piece["hoverConfig"]):
            if stateLeftClick: #Place Piece
                grid, pieceCoordinates = ggs.placePieceOnGrid(grid, pieceCoordinates, piece["ID"], xPlayerGrid, yPlayerGrid, piece["hoverConfig"])
                piece["coordinates"] = pieceCoordinates[piece["ID"]]
                piece["isPlaced"] = True
                piece["config"] = piece["hoverConfig"]
            else: #Hover Piece
                drawPieceHover(piece, pieceCoordinates, grid, xPlayerGrid, yPlayerGrid)
    #3
    if piece["isPlaced"] and piece["isSelected"]:
        if isWithinPlayerGrid(mousePos, allSquares):
            x, y = getMouseCoordinatesOnMainGrid(mousePos, width, height)
            yPlayerGrid = y - 2
            xPlayerGrid = x - 1
            
            copyGrid = deepcopy(grid)
            copyGrid = ggs.removePieceFromGrid(copyGrid, pieceCoordinates, piece["ID"])  
            if ggs.isMoveValid(copyGrid, piece["ID"], xPlayerGrid, yPlayerGrid, piece["hoverConfig"]): #Hover Piece when already placed
                drawPieceHover(piece, pieceCoordinates, grid, xPlayerGrid, yPlayerGrid)            
            
            if stateLeftClick and ggs.isMoveValid(copyGrid, piece["ID"], xPlayerGrid, yPlayerGrid, piece["hoverConfig"]):
                #Place piece when already placed          
                grid = ggs.removePieceFromGrid(grid, pieceCoordinates, piece["ID"])
                pieceCoordinates[piece["ID"]] = None  
                #piece["isPlaced"] = True #Piece already placed
                grid, pieceCoordinates = ggs.placePieceOnGrid(grid, pieceCoordinates, piece["ID"], xPlayerGrid, yPlayerGrid, piece["hoverConfig"])    
                piece["coordinates"] = pieceCoordinates[piece["ID"]]         
                piece["config"] = piece["hoverConfig"]            
        if isRemovingPiece:
            #4 Remove Piece (when already placed)
            grid = ggs.removePieceFromGrid(grid, pieceCoordinates, piece["ID"])
            pieceCoordinates[piece["ID"]] = None  
            piece["coordinates"] = DEFAULT_PLAYER_PIECE_COORDINATES[piece["ID"]]
            piece["config"] = DEFAULT_PLAYER_PIECE_CONFIG[piece["ID"]]
            piece["isPlaced"] = False
    
    #5
    if isWithinPiece(mousePos, piece, pieceCoordinates):
        piece["isHovered"] = True 
    else:
        piece["isHovered"] = False

    if isWithinPiece(mousePos, piece, pieceCoordinates) and stateLeftClick:
        piece["isSelected"] = True 
    elif stateLeftClick:         
        piece["isSelected"] = False     
        piece["hoverConfig"] = piece["config"]
      
    #6
    drawPiece(piece, pieceCoordinates)    
       
    return grid, pieceCoordinates, piece           

def convertSeedIntoString(seed: list[tuple[int, int]]) -> str: 
    """ 
    Convert list of coordinates for the blockers into a string

    Parameters:
        LIST<TUPLE<INT, INT>> seed 
        
    Returns:
        STRING convertedSeed    
    """
    convertedSeed = ""
    for i in range(0, 7):
        match seed[i][1]:
            case 0:
                convertedSeed += "A"
            case 1:
                convertedSeed += "B"
            case 2:
                convertedSeed += "C"
            case 3:
                convertedSeed += "D"
            case 4:
                convertedSeed += "E"
            case 5: 
                convertedSeed += "F"
        convertedSeed += str(seed[i][0] + 1)
    
    return convertedSeed

def tryFindSolution(grid: list[list[int, int]], pieceCoordinates: dict[int, tuple[int, int]], unusedPiecesID: list[int]) -> int:
    """ 
    Current:
    Tries to remove one piece from the board to find a solution, tries all pieces present on the board
    
    Not implemented:
    Should try all pieces present on the board, one at a time. Then if nothing is returned it should try remove all pieces,
    one at a time, and recursively find a way that leads to a solution. Returning a piece that would have to be removed
    to approach that solution.

    Parameters:
        LIST<LIST<INT, INT>> grid
        DICT<INT TUPLE<INT, INT>> pieceCoordinates
        LIST<INT> unusedPiecesID
        
    Returns:
        INT pieceID     
    """
    #Works for one piece removal
    #Due to time restraints it will not reattempt piece removal
    hintGrid = deepcopy(grid)
    hintPieceCoordinates = deepcopy(pieceCoordinates)
    hintUnusedPieces = deepcopy(unusedPiecesID)   
    for pieceID in filter(lambda x: x not in unusedPiecesID, ggs.ALL_PIECE_IDS): #Placed pieces
        hintGrid = ggs.removePieceFromGrid(hintGrid, hintPieceCoordinates, pieceID)
        hintPieceCoordinates[pieceID] = None
        hintUnusedPieces.append(pieceID)
        hintSolution = ggs.findSolution(hintGrid, hintPieceCoordinates, hintUnusedPieces) 
        
        if hintSolution:
            return pieceID
        else:
            hintGrid = deepcopy(grid)
            hintPieceCoordinates = deepcopy(pieceCoordinates)
            hintUnusedPieces = deepcopy(unusedPiecesID)  
        
    return None
            
def getHint(grid: list[list[int, int]], pieceCoordinates: dict[int, tuple[int, int]], unusedPiecesID: list[int]) -> tuple[int, int]: 
    """ 
    Gets one of three possible hints based on the current grid configuration.
    There is no solution -> Attempt piece removal
    There is a solution -> Nothing removed

    Parameters:
        LIST<LIST<INT, INT>> grid
        DICT<INT TUPLE<INT, INT>> pieceCoordinates
        LIST<INT> unusedPiecesID
        
    Returns:
        TUPLE<INT, INT> (-1, None): No hint found
        TUPLE<INT, INT> (0, hint): Piece to remove
        TUPLE<INT, BOOL> (1, hintSolution): No piece requires removal to acquire solution
    """
    hintGrid = deepcopy(grid)
    hintPieceCoordinates = deepcopy(pieceCoordinates)
    hintUnusedPieces = deepcopy(unusedPiecesID)   
    
    hintSolution = ggs.findSolution(hintGrid, hintPieceCoordinates, hintUnusedPieces) 
    
    if not hintSolution: #Bad Grid, try remove piece
        hint = tryFindSolution(hintGrid, hintPieceCoordinates, hintUnusedPieces)
        if hint is None:
            return (-1, None)
        else:
            return (0, hint)
    else: #Pick a piece or square to highlight #TODO Not finished
        return (1, hintSolution)

if __name__ == "__main__":
    pygame.init()

    #REFRESH RATE
    clock = pygame.time.Clock()

    #SCREEN DIMENSIONS
    width, height = pygame.display.Info().current_w, pygame.display.Info().current_h
    screen = pygame.display.set_mode((width, height), pygame.NOFRAME | pygame.FULLSCREEN)
    pygame.display.set_caption("Genius Square")

    #CLIPBOARD
    pygame.scrap.init()
    pygame.scrap.set_mode(pygame.SCRAP_CLIPBOARD)
    
    #INITIAL VALUES
    TOTAL_SQUARES = 18
    SQUARE_SIZE = min(width // TOTAL_SQUARES, height // TOTAL_SQUARES) #Ensure squares fit within the screen
    GRID_WIDTH = TOTAL_SQUARES * SQUARE_SIZE
    BORDER_WIDTH = 2

    FONT_SIZE = min(width, height) // 20 
    font = pygame.font.Font(None, FONT_SIZE)
    
    isMainMenuSeedTextBoxActive = False 
    mainMenuSeedTextBoxString = "" #Stored as uppercase letters
    isMainMenuSeedTextBoxValueValid = True 
    inputChar = None #Used in Seed entry text box

    isSafeToToggleTime = True #Used to prevent time button from flickering

    #Remove/Rotate/Reflect selected piece
    isRemovingPiece = False
    isRotatingPiece = False
    isReflectingPiece = False 

    isRequestingHint = False

    copyGrid = ggs.EMPTY_GRID #Used to simulate main grid for hovering piece already placed

    hasWon = False

    currentHint = None 

    """ 
    State machine for the different scenes.
    Note three was not implemented
    0 - Main Menu 
    1 - Loading Screen
    2 - Game 
    3 - End screen
    0 -> 1 - > 2 -> 3 -> 0
    """
    currentState = 0

    """ 
    States for the timer: Seconds
    0 - 180
    1 - 90
    2 - 45
    0 -> 1 -> 2 -> 0
    """  
    timeState = 0

    grid = deepcopy(ggs.EMPTY_GRID)
    pieceCoordinates = deepcopy(ggs.DEFAULT_PIECE_COORDINATES)
    unusedPiecesID = deepcopy(ggs.ALL_PIECE_IDS)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.VIDEORESIZE:
                width, height = event.w, event.h
                screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
            elif event.type == pygame.KEYDOWN:
                #MANAGE KEYBOARD INPUT
                if currentState == 0 and isMainMenuSeedTextBoxActive and event.key == pygame.K_v and pygame.key.get_mods() & pygame.KMOD_CTRL:
                    #MANAGE CLIPBOARD PASTING
                    mainMenuSeedTextBoxString = handleTextBoxClipboardInput(mainMenuSeedTextBoxString, 14)
                elif currentState == 0 and isMainMenuSeedTextBoxActive and event.key in range(pygame.K_a, pygame.K_z + 1):
                    #MANAGE SEED TEXT BOX INPUT
                    inputChar = chr(event.key)
                elif currentState == 0 and isMainMenuSeedTextBoxActive and event.key in range(pygame.K_0, pygame.K_9 + 1):
                    inputChar = chr(event.key)
                elif currentState == 0 and isMainMenuSeedTextBoxActive and event.key == pygame.K_BACKSPACE:
                    mainMenuSeedTextBoxString = mainMenuSeedTextBoxString[:-1]    
                elif currentState == 2 and event.key == pygame.K_w:
                    #MANAGE PIECE CONFIGURATION AND HINT SYSTEM
                    isRemovingPiece = True
                elif currentState == 2 and event.key == pygame.K_e:
                    isRotatingPiece = True 
                elif currentState == 2 and event.key == pygame.K_r:
                    isReflectingPiece = True
                elif currentState == 2 and event.key == pygame.K_h:
                    isRequestingHint = True
                    
        screen.fill(BLACK)
        
        mousePos = pygame.mouse.get_pos()
        stateLeftClick = pygame.mouse.get_pressed()[0]
        match currentState:
            case 0:
                allSquares = getSquareCoordinates()
                drawSideBars(screen, BLACK, width, height)
                drawMainGrid(screen, GREY, allSquares)
                drawGameBoardGridMainMenu(screen, allSquares)
                drawGameBoardGridLabelsMainMenu(screen, allSquares)
                
                validDieFaces = getValidDieFaces(mainMenuSeedTextBoxString)
                drawDieFaces(screen, allSquares, mainMenuSeedTextBoxString, validDieFaces)
                drawMainMenuBlockers(screen, allSquares, validDieFaces)
                
                currentState, isMainMenuSeedTextBoxValueValid = handlePlayButton(screen, allSquares, mainMenuSeedTextBoxString, isMainMenuSeedTextBoxValueValid, mousePos, stateLeftClick)                 
                            
                timeState, isSafeToToggleTime = handleTimeButton(screen, allSquares, timeState, mousePos, stateLeftClick, isSafeToToggleTime)     
                if not isSafeToToggleTime and not stateLeftClick:
                    isSafeToToggleTime = True
                    
                isMainMenuSeedTextBoxActive, mainMenuSeedTextBoxString = handleSeedTextBox(screen, allSquares, mousePos, isMainMenuSeedTextBoxActive, mainMenuSeedTextBoxString, inputChar, validDieFaces)
                inputChar = None   
                
                running = handleQuitButton(screen, allSquares, mousePos, stateLeftClick)
                
                if currentState == 1:
                    if mainMenuSeedTextBoxString == "":
                        seed = ggs.getDiceRolls()
                        seed = convertSeedIntoString(seed)
                        validDieFaces = getValidDieFaces(seed)
                    else:
                        seed = mainMenuSeedTextBoxString

                    grid = deepcopy(ggs.EMPTY_GRID)
                    pieceCoordinates = deepcopy(ggs.DEFAULT_PIECE_COORDINATES)
                    unusedPiecesID = deepcopy(ggs.ALL_PIECE_IDS)
                    
                    #Uses main grid coordinates not player or computer grid coordinates!
                    allPieces = deepcopy(DEFAULT_PLAYER_PIECES)
                    diceRoll = ggs.getDiceRolls(seed)
                    grid = ggs.initaliseBlockers(grid, diceRoll)
                            
                    match timeState:
                        case 0:
                            timer = 180
                        case 1:
                            timer = 90
                        case 2:
                            timer = 45 
                        
            case 1:
                allSquares = getSquareCoordinates()            
                drawSideBars(screen, BLACK, width, height)
                drawMainGrid(screen, GREY, allSquares)
                drawLoadingScreen(screen, allSquares, seed)
                drawGameBoardGridLoadingScreen(screen, allSquares)
                drawGameBoardGridLabelsLoadingScreen(screen, allSquares)
                drawLoadingScreenBlockers(screen, allSquares, validDieFaces)
                pygame.display.flip() #Force pygame to update screen 
                
                executionStart = pygame.time.get_ticks()
                aiGrid = deepcopy(grid)
                aiPieceCoordinates = deepcopy(pieceCoordinates)
                aiUnusedPiecesID =  deepcopy(unusedPiecesID)
                solution = ggs.findSolution(aiGrid, aiPieceCoordinates, aiUnusedPiecesID)
                aiTimeIntervals = [0, 0, 0, 0, 0, 0, 0, 0, timer]
                aiPiecesPlaced = 0
                aiUnusedPiecesID = deepcopy(ggs.ALL_PIECE_IDS) #Reset post solution
                aiAllPieces = deepcopy(allPieces)
                tempGrid = deepcopy(grid)
                reversedAiGrid = [row[::-1] for row in tempGrid] #Mirror grid
                aiGrid = deepcopy(reversedAiGrid)

                reversedAiPieceCoordinates = {}
                for key, value in aiPieceCoordinates.items():
                    reversedAiPieceCoordinates[key] = [(len(tempGrid[0]) - 1 - x, y) for x, y in value]

                aiPieceCoordinates = deepcopy(reversedAiPieceCoordinates) #Mirror grid coordinates
                
                interval = timer // 9
                for i in range(0, 8):
                    aiTimeIntervals[i] = (i * interval) + ggs.random.randint(0, interval - 1)

                executionTime = pygame.time.get_ticks() - executionStart #3 second Loading Screen minimum
                if executionTime < 3000:
                    pygame.time.wait(3000 - executionTime)

                currentState = 2
                startTicks = pygame.time.get_ticks()
                
            case 2:
                allSquares = getSquareCoordinates()
                drawSideBars(screen, BLACK, width, height)
                drawMainGrid(screen, GREY, allSquares)
                drawDividerLines(screen, allSquares)
                drawGameBoardGrid(screen, allSquares)
                drawGameBoardGridLabels(screen, allSquares)
                drawGameBoardBlockers(screen, allSquares, validDieFaces)
                elapsedTime = pygame.time.get_ticks() - startTicks
                remainingTime = max(0, timer - elapsedTime // 1000)  #Convert milliseconds to seconds
                drawTimer(screen, allSquares, remainingTime)
                
                for piece in allPieces.keys():
                    grid, pieceCoordinates, allPieces[piece] = handlePieceInteraction(grid, pieceCoordinates, allPieces[piece], isRotatingPiece, isReflectingPiece, isRemovingPiece, width, height)
                isRemovingPiece = False 
                isRotatingPiece = False 
                isReflectingPiece = False  
                
                if isRequestingHint:
                    isRequestingHint = False
                    currentHint = getHint(grid, pieceCoordinates, unusedPiecesID)
                    
                if currentHint is not None:
                    if currentHint[0] == -1: #No hint
                        drawFilledSquareWithBorder(screen, VIOLET, allSquares[7][8][0], allSquares[7][8][1], SQUARE_SIZE, SQUARE_SIZE, BORDER_WIDTH) 
                        renderTextInSquare(screen, "X", font, WHITE, allSquares[7][8][0], allSquares[7][8][1], SQUARE_SIZE)
                    elif currentHint[0] == 0: #Piece to remove
                        drawFilledSquareWithBorder(screen, GREEN_LIME, allSquares[7][8][0], allSquares[7][8][1], SQUARE_SIZE, SQUARE_SIZE, BORDER_WIDTH)
                        match currentHint[1]:
                            case 0:
                                hintText = "SS"
                            case 1:
                                hintText = "BS"
                            case 2:
                                hintText = "SB"
                            case 3:
                                hintText = "B"
                            case 4:
                                hintText = "LB"
                            case 5:
                                hintText = "L"
                            case 6:
                                hintText = "T"
                            case 7:
                                hintText = "Z"
                            case 8:
                                hintText = "A"
                        renderTextInSquare(screen, hintText, font, WHITE, allSquares[7][8][0], allSquares[7][8][1], SQUARE_SIZE)
                    else: #1 TODO Not implemented
                        drawFilledSquareWithBorder(screen, VIOLET, allSquares[7][8][0], allSquares[7][8][1], SQUARE_SIZE, SQUARE_SIZE, BORDER_WIDTH) 
                        renderTextInSquare(screen, "X", font, WHITE, allSquares[7][8][0], allSquares[7][8][1], SQUARE_SIZE)
                
                placedPieces = 0
                unusedPiecesID = deepcopy(ggs.ALL_PIECE_IDS)
                for piece in allPieces.keys():
                    if allPieces[piece]["isPlaced"]:
                        placedPieces += 1
                        unusedPiecesID.remove(allPieces[piece]["ID"])
                
                for piece in aiAllPieces.keys(): 
                    if aiAllPieces[piece]["isPlaced"]:
                        drawPieceAI(aiAllPieces[piece], aiPieceCoordinates)
                        continue
                
                if len(aiUnusedPiecesID) != 0 and aiTimeIntervals[aiPiecesPlaced] == timer - remainingTime:
                    nextPiece = ggs.random.choice(aiUnusedPiecesID)
                    aiUnusedPiecesID.remove(nextPiece)
                    aiAllPieces[nextPiece]["isPlaced"] = True 
                    aiPiecesPlaced += 1
                    
                elif remainingTime < 1:
                    hasWon = False 
                    pygame.display.flip() #Force pygame to update screen 
                    pygame.time.wait(3000)
                    currentState = 0
                
                if placedPieces == len(allPieces.keys()):
                    hasWon = True
                    pygame.display.flip() #Force pygame to update screen 
                    pygame.time.wait(3000)
                    currentState = 0
                    
            #case 3: NOT IMPLEMENTED
                    
        pygame.display.flip() 
        clock.tick(FPS)

    pygame.quit()
    sys.exit()