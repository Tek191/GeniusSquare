""" 
Solver for the Genius Square
This includes functions to:
-Print a grid
-Intialize a grid with blockers
-Generate blockers from a seed
-Validate a move
-Place a piece
-Remove a piece
-Solve a grid
"""

import random
import re #match vs match in 3.10+ Python, hence full import
from copy import deepcopy 

""" 
Grid element IDs
"""
BLOCKER_ID = -2
EMPTY_ID = -1
SMALL_SQUARE_PIECE_ID = 0
BIG_SQUARE_PIECE_ID = 1
SHORT_BAR_PIECE_ID = 2
BAR_PIECE_ID = 3
LONG_BAR_PIECE_ID = 4
L_PIECE_ID = 5
T_PIECE_ID = 6
Z_PIECE_ID = 7
ARROW_PIECE_ID = 8

""" 
Dice and their respective faces - note first character is Y coordinate and second is X coordinate -> (X, Y).
Also note that the numbers range from [1, 5] while they are represented as [0, 4] in code.
"""
DICE_ONE   = ("A1", "C1", "D1", "D2", "E2", "F3")
DICE_TWO   = ("A2", "B2", "C2", "A3", "B1", "B3")
DICE_THREE = ("C3", "D3", "E3", "B4", "C4", "D4")
DICE_FOUR  = ("E1", "F2", "F2", "B6", "A5", "A5")
DICE_FIVE  = ("A4", "B5", "C6", "C5", "D6", "F6")
DICE_SIX   = ("E4", "F4", "E5", "F5", "D5", "E6")
DICE_SEVEN = ("F1", "F1", "F1", "A6", "A6", "A6")
ALL_DICE =  [DICE_ONE, DICE_TWO, DICE_THREE, DICE_FOUR, DICE_FIVE, DICE_SIX, DICE_SEVEN]

"""
Look up table for every configuration for each piece.
dict[int, int]
PIECE_ID: CONFIG
"""
PIECE_CONFIGURATIONS = {
    SMALL_SQUARE_PIECE_ID: [0],
    BIG_SQUARE_PIECE_ID: [0, 1, 2, 3],
    SHORT_BAR_PIECE_ID: [0, 1, 2, 3],
    BAR_PIECE_ID: [0, 1, 2, 3, 4, 5],
    LONG_BAR_PIECE_ID: [0, 1, 2, 3, 4, 5, 6, 7],
    L_PIECE_ID: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31],
    T_PIECE_ID: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15],
    Z_PIECE_ID: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15],
    ARROW_PIECE_ID: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
}

EMPTY_GRID = [
        [EMPTY_ID, EMPTY_ID, EMPTY_ID, EMPTY_ID, EMPTY_ID, EMPTY_ID],
        [EMPTY_ID, EMPTY_ID, EMPTY_ID, EMPTY_ID, EMPTY_ID, EMPTY_ID],
        [EMPTY_ID, EMPTY_ID, EMPTY_ID, EMPTY_ID, EMPTY_ID, EMPTY_ID],
        [EMPTY_ID, EMPTY_ID, EMPTY_ID, EMPTY_ID, EMPTY_ID, EMPTY_ID],
        [EMPTY_ID, EMPTY_ID, EMPTY_ID, EMPTY_ID, EMPTY_ID, EMPTY_ID],
        [EMPTY_ID, EMPTY_ID, EMPTY_ID, EMPTY_ID, EMPTY_ID, EMPTY_ID]
    ] 

ALL_PIECE_IDS = [SMALL_SQUARE_PIECE_ID, BIG_SQUARE_PIECE_ID, SHORT_BAR_PIECE_ID, BAR_PIECE_ID, LONG_BAR_PIECE_ID, L_PIECE_ID, T_PIECE_ID, Z_PIECE_ID, ARROW_PIECE_ID]

""" 
Default values for the look up table for each pieces coordinates
dict[int, tuple[int]]
"""
DEFAULT_PIECE_COORDINATES = {
        SMALL_SQUARE_PIECE_ID: None,
        BIG_SQUARE_PIECE_ID: None,
        SHORT_BAR_PIECE_ID: None,
        BAR_PIECE_ID: None,
        LONG_BAR_PIECE_ID: None,
        L_PIECE_ID: None,
        T_PIECE_ID: None,
        Z_PIECE_ID: None,
        ARROW_PIECE_ID: None
} 

def getDieFaceCoordinates(dieFace: str) -> tuple[int, int]:
    """
    Returns the x and y coordinates converted from a given die face.
    getDiceRolls() checks whether dieFace is valid.
    
    Parameters:
        STRING dieFace
        
    Returns:
        TUPLE<INT, INT>
    """ 
    match dieFace[0]:
        case 'A':
            return (int(dieFace[1]) - 1, 0)
        case 'B':
            return (int(dieFace[1]) - 1, 1)
        case 'C':
            return (int(dieFace[1]) - 1, 2)
        case 'D':
            return (int(dieFace[1]) - 1, 3)
        case 'E':
            return (int(dieFace[1]) - 1, 4)
        case 'F': 
            return (int(dieFace[1]) - 1, 5)
    
def getDiceRolls(seed: str = None) -> list[tuple[int, int]]:
    """
    Returns a list of x and y coordinates from a random seed or from a given seed of die faces.
    Seed is validated without raising exceptions within this function.
     
    Parameters:
        [OPTIONAL] STRING seed : 14 characters in the format XYXY..XY where X->A..F and Y->[1, 6]
        
    Returns:
        LIST<TUPLE<INT, INT>> rolls
    
    Examples:
        getDiceRolls() -> Random list of 7 tuples
        getDiceRolls("A1A2C3E1A4E4F1") -> [(0, 0), (1, 0), (2, 2), (0, 4), (3, 0), (3, 4), (0, 5)]
    """   
    rolls = []

    if seed is None or not isinstance(seed, str) or not re.match(r'^([A-F][1-6]){7}$', seed):
        for die in ALL_DICE:
            roll = getDieFaceCoordinates(die[random.randint(0, 5)])
            rolls.append(roll)
        return rolls

    for i in range(0, 14, 2):
        roll = getDieFaceCoordinates(seed[i] + seed[i+1])
        rolls.append(roll)
    return rolls
    
def initaliseBlockers(grid: list[list[int, int]], blockers: list[tuple[int, int]]) -> list[list[int, int]]:
    """ 
    Updates the grid with the provided blockers.
    Note the 2D list representing the grid is accessed via Y followed by X, hence grid[Y][X].
    getDiceRolls() passes validated blockers as parameter.

    Parameters:
        LIST<LIST<INT, INT>> grid
        LIST<TUPLE<INT, INT>> blockers
        
    Returns:
        LIST<LIST<INT, INT>> grid
    """ 
    for blocker in blockers:
        grid[blocker[1]][blocker[0]] = BLOCKER_ID
    return grid 

def isMoveValidSmallSquare(grid: list[list[int, int]], x: int, y: int) -> bool: 
    """ 
    Validates whether a small square can be placed onto a given grid at the given coordinates

    Parameters:
        LIST<LIST<INT, INT>> grid
        INT x
        INT y
    Returns:
        BOOL
    """ 
    """ 
    0: x
    """
    #Check shape within grid
    if x < 0 or x > 5 or  y < 0 or y > 5:
        return False 
    
    #Check if destination occupied on grid
    if grid[y][x] != EMPTY_ID:
        return False
    
    return True    

def placeSmallSquareOnGrid(grid: list[list[int, int]], pieceCoordinates: dict[int, tuple[int, int]], x: int, y: int) -> tuple[list[list[int, int]], dict[int, tuple[int, int]]]:
    """ 
    Places a small square onto a given grid at the given coordinates

    Parameters:
        LIST<LIST<INT, INT>> grid
        DICT<INT, TUPLE<INT, INT>> pieceCoordinates
        INT x
        INT y
    Returns:
        TUPLE<LIST<LIST<INT, INT>> grid, DICT<INT, TUPLE<INT, INT>> pieceCoordinates>
    """
    """ 
    0: x
    """
    grid[y][x] = SMALL_SQUARE_PIECE_ID 
    pieceCoordinates[SMALL_SQUARE_PIECE_ID] = [(x, y)]    
    return grid, pieceCoordinates

def isMoveValidBigSquare(grid: list[list[int, int]], x: int, y: int, config: int) -> bool:
    """ 
    Validates whether a big square can be placed onto a given grid at the given coordinates

    Parameters:
        LIST<LIST<INT, INT>> grid
        INT x
        INT y
        INT config
    Returns:
        BOOL
    """ 
    """ 
    0:  x o
        o o
    
    1:  o x
        o o
        
    2:  o o
        o x

    3:  o o
        x o
    """
    #Check shape within grid
    match config:
        case 0:
            if x < 0 or x > 4 or y < 0 or y > 4:
                return False 
        case 1:
            if x < 1 or x > 5 or y < 0 or y > 4:
                return False 
        case 2:
            if x < 1 or x > 5 or y < 1 or y > 5:
                return False 
        case 3:
            if x < 1 or x > 4 or y < 1 or y > 5:
                return False  

            
    #Check if destination occupied on grid
    match config:
        case 0:
            if grid[y][x] != EMPTY_ID or grid[y+1][x] != EMPTY_ID or grid[y][x+1] != EMPTY_ID or grid[y+1][x+1] != EMPTY_ID:
                return False
        case 1:
            if grid[y][x] != EMPTY_ID or grid[y][x-1] != EMPTY_ID or grid[y+1][x-1] != EMPTY_ID or grid[y+1][x] != EMPTY_ID:
                return False                    
        case 2:
            if grid[y][x] != EMPTY_ID or grid[y-1][x] != EMPTY_ID or grid[y][x-1] != EMPTY_ID or grid[y-1][x-1] != EMPTY_ID:
                return False
        case 3:
            if grid[y][x] != EMPTY_ID or grid[y][x-1] != EMPTY_ID or grid[y-1][x] != EMPTY_ID or grid[y-1][x-1] != EMPTY_ID:
                return False
            
    return True

def placeBigSquareOnGrid(grid: list[list[int, int]], pieceCoordinates: dict[int, tuple[int, int]], x: int, y: int, config: int) -> tuple[list[list[int, int]], dict[int, tuple[int, int]]]:
    """ 
    Places a big square onto a given grid at the given coordinates

    Parameters:
        LIST<LIST<INT, INT>> grid
        DICT<INT, TUPLE<INT, INT>> pieceCoordinates
        INT x
        INT y
        INT config
    Returns:
        TUPLE<LIST<LIST<INT, INT>> grid, DICT<INT, TUPLE<INT, INT>> pieceCoordinates>
    """
    """ 
    0:  x o
        o o
    
    1:  o x
        o o
        
    2:  o o
        o x

    3:  o o
        x o
    """            
    match config:
        case 0:
            grid[y][x] = BIG_SQUARE_PIECE_ID 
            grid[y+1][x] = BIG_SQUARE_PIECE_ID 
            grid[y][x+1] = BIG_SQUARE_PIECE_ID 
            grid[y+1][x+1] = BIG_SQUARE_PIECE_ID
            pieceCoordinates[BIG_SQUARE_PIECE_ID] = [(x, y), (x, y+1), (x+1, y), (x+1, y+1)]
        case 1:
            grid[y][x] = BIG_SQUARE_PIECE_ID 
            grid[y][x-1] = BIG_SQUARE_PIECE_ID 
            grid[y+1][x-1] = BIG_SQUARE_PIECE_ID 
            grid[y+1][x] = BIG_SQUARE_PIECE_ID
            pieceCoordinates[BIG_SQUARE_PIECE_ID] = [(x, y), (x-1, y), (x-1, y+1), (x, y+1)]
        case 2:
            grid[y][x] = BIG_SQUARE_PIECE_ID 
            grid[y-1][x] = BIG_SQUARE_PIECE_ID 
            grid[y][x-1] = BIG_SQUARE_PIECE_ID 
            grid[y-1][x-1] = BIG_SQUARE_PIECE_ID
            pieceCoordinates[BIG_SQUARE_PIECE_ID] = [(x, y), (x, y-1), (x-1, y), (x-1, y-1)]
        case 3:
            grid[y][x] = BIG_SQUARE_PIECE_ID 
            grid[y][x-1] = BIG_SQUARE_PIECE_ID 
            grid[y-1][x] = BIG_SQUARE_PIECE_ID 
            grid[y-1][x-1] = BIG_SQUARE_PIECE_ID
            pieceCoordinates[BIG_SQUARE_PIECE_ID] = [(x, y), (x-1, y), (x, y-1), (x-1, y-1)]
    
    return grid, pieceCoordinates
 
def isMoveValidShortBar(grid: list[list[int, int]], x: int, y: int, config: int) -> bool:
    """ 
    Validates whether a short bar can be placed onto a given grid at the given coordinates

    Parameters:
        LIST<LIST<INT, INT>> grid
        INT x
        INT y
        INT config
    Returns:
        BOOL
    """
    """ 
    0:  x o
    
    1:  x
        o
        
    2:  o x
    
    3:  o
        x
    """
    
    #Check shape within grid
    match config:
        case 0:
            if x < 0 or x > 4 or y < 0 or y > 5:
                return False
        case 1:
            if x < 0 or x > 5 or y < 0 or y > 4:
                return False
        case 2:
            if x < 1 or x > 5 or y < 0 or y > 5:
                return False
        case 3:
            if x < 0 or x > 5 or y < 1 or y > 5:
                return False
    
    #Check if destination occupied on grid
    match config:
        case 0:
            if grid[y][x] != EMPTY_ID or grid[y][x+1] != EMPTY_ID:
                return False
        case 1:
            if grid[y][x] != EMPTY_ID or grid[y+1][x] != EMPTY_ID:
                return False
        case 2:
            if grid[y][x] != EMPTY_ID or grid[y][x-1] != EMPTY_ID:
                return False
        case 3:
            if grid[y][x] != EMPTY_ID or grid[y-1][x] != EMPTY_ID:
                return False
            
    return True

def placeShortBarOnGrid(grid: list[list[int, int]], pieceCoordinates: dict[int, tuple[int, int]], x: int, y: int, config: int) -> tuple[list[list[int, int]], dict[int, tuple[int, int]]]:
    """ 
    Places a short bar onto a given grid at the given coordinates

    Parameters:
        LIST<LIST<INT, INT>> grid
        DICT<INT, TUPLE<INT, INT>> pieceCoordinates
        INT x
        INT y
        INT config
    Returns:
        TUPLE<LIST<LIST<INT, INT>> grid, DICT<INT, TUPLE<INT, INT>> pieceCoordinates>
    """
    """ 
    0:  x o
    
    1:  x
        o
        
    2:  o x
    
    3:  o
        x
    """       
    match config:
        case 0:
            grid[y][x] = SHORT_BAR_PIECE_ID
            grid[y][x+1] = SHORT_BAR_PIECE_ID
            pieceCoordinates[SHORT_BAR_PIECE_ID] = [(x, y), (x+1, y)]
        case 1:
            grid[y][x] = SHORT_BAR_PIECE_ID
            grid[y+1][x] = SHORT_BAR_PIECE_ID
            pieceCoordinates[SHORT_BAR_PIECE_ID] = [(x, y), (x, y+1)]
        case 2:
            grid[y][x] = SHORT_BAR_PIECE_ID
            grid[y][x-1] = SHORT_BAR_PIECE_ID
            pieceCoordinates[SHORT_BAR_PIECE_ID] = [(x, y), (x-1, y)]
        case 3:
            grid[y][x] = SHORT_BAR_PIECE_ID
            grid[y-1][x] = SHORT_BAR_PIECE_ID
            pieceCoordinates[SHORT_BAR_PIECE_ID] = [(x, y), (x, y-1)]    
    
    return grid, pieceCoordinates

def isMoveValidBar(grid: list[list[int, int]], x: int, y: int, config: int) -> bool:
    """ 
    Validates whether a bar can be placed onto a given grid at the given coordinates

    Parameters:
        LIST<LIST<INT, INT>> grid
        INT x
        INT y
        INT config
    Returns:
        BOOL
    """ 
    """ 
    0:  x o o
        
    1:  x
        o
        o
    
    2: o o x
    
    3:  o
        o
        x
        
    4: o x o
    
    5: o
       x
       o
    """
    #Check shape within grid            
    match config:
        case 0:
            if x < 0 or x > 3 or y < 0 or y > 5:
                return False
        case 1:
            if x < 0 or x > 5 or y < 0 or y > 3:
                return False
        case 2:
            if x < 2 or x > 5 or y < 0 or y > 5:
                return False
        case 3:
            if x < 0 or x > 5 or y < 0 or y > 5:
                return False
        case 4:
            if x < 1 or x > 4 or y < 0 or y > 5:
                return False 
        case 5:
            if x < 0 or x > 5 or y < 1 or y > 4:
                return False
    
    #Check if destination occupied on grid
    match config:
        case 0:
            if grid[y][x] != EMPTY_ID or grid[y][x+1] != EMPTY_ID or grid[y][x+2] != EMPTY_ID:
                return False
        case 1:
            if grid[y][x] != EMPTY_ID or grid[y+1][x] != EMPTY_ID or grid[y+2][x] != EMPTY_ID:
                return False
        case 2:
            if grid[y][x] != EMPTY_ID or grid[y][x-1] != EMPTY_ID or grid[y][x-2] != EMPTY_ID:
                return False
        case 3:
            if grid[y][x] != EMPTY_ID or grid[y-1][x] != EMPTY_ID or grid[y-2][x] != EMPTY_ID:
                return False
        case 4:
            if grid[y][x] != EMPTY_ID or grid[y][x-1] != EMPTY_ID or grid[y][x+1] != EMPTY_ID:
                return False           
        case 5:
            if grid[y][x] != EMPTY_ID or grid[y-1][x] != EMPTY_ID or grid[y+1][x] != EMPTY_ID:
                return False     
                 
    return True

def placeBarOnGrid(grid: list[list[int, int]], pieceCoordinates: dict[int, tuple[int, int]], x: int, y: int, config: int) -> tuple[list[list[int, int]], dict[int, tuple[int, int]]]:
    """ 
    Places a bar onto a given grid at the given coordinates

    Parameters:
        LIST<LIST<INT, INT>> grid
        DICT<INT, TUPLE<INT, INT>> pieceCoordinates
        INT x
        INT y
        INT config
    Returns:
        TUPLE<LIST<LIST<INT, INT>> grid, DICT<INT, TUPLE<INT, INT>> pieceCoordinates>
    """
    """ 
    0:  x o o
        
    1:  x
        o
        o
    
    2: o o x
    
    3:  o
        o
        x
        
    4: o x o
    
    5: o
       x
       o
    """      
    match config:
        case 0:
            grid[y][x] = BAR_PIECE_ID
            grid[y][x+1] = BAR_PIECE_ID
            grid[y][x+2] = BAR_PIECE_ID
            pieceCoordinates[BAR_PIECE_ID] = [(x, y), (x+1, y), (x+2, y)]
        case 1:
            grid[y][x] = BAR_PIECE_ID
            grid[y+1][x] = BAR_PIECE_ID
            grid[y+2][x] = BAR_PIECE_ID
            pieceCoordinates[BAR_PIECE_ID] = [(x, y), (x, y+1), (x, y+2)]
        case 2:
            grid[y][x] = BAR_PIECE_ID
            grid[y][x-1] = BAR_PIECE_ID
            grid[y][x-2] = BAR_PIECE_ID
            pieceCoordinates[BAR_PIECE_ID] = [(x, y), (x-1, y), (x-2, y)]
        case 3:
            grid[y][x] = BAR_PIECE_ID
            grid[y-1][x] = BAR_PIECE_ID
            grid[y-2][x] = BAR_PIECE_ID
            pieceCoordinates[BAR_PIECE_ID] = [(x, y), (x, y-1), (x, y-2)]
        case 4:
            grid[y][x] = BAR_PIECE_ID
            grid[y][x-1] = BAR_PIECE_ID 
            grid[y][x+1] = BAR_PIECE_ID
            pieceCoordinates[BAR_PIECE_ID] = [(x, y), (x-1, y), (x+1, y)]
        case 5:
            grid[y][x] = BAR_PIECE_ID
            grid[y-1][x] = BAR_PIECE_ID 
            grid[y+1][x] = BAR_PIECE_ID
            pieceCoordinates[BAR_PIECE_ID] = [(x, y), (x, y-1), (x, y+1)]

    return grid, pieceCoordinates
 
def isMoveValidLongBar(grid: list[list[int, int]], x: int, y: int, config: int) -> bool:
    """ 
    Validates whether a long bar can be placed onto a given grid at the given coordinates

    Parameters:
        LIST<LIST<INT, INT>> grid
        INT x
        INT y
        INT config
    Returns:
        BOOL
    """
    """       
    0:  x o o o
                
    1:  x
        o
        o
        o
        
    2:  o o o x
                
    3:  o
        o
        o
        x
    
    4: o x o o
    
    5: o o x o
    
    6:  o
        x
        o
        o
    
    7:  o
        o
        x
        o     
    """
    
    #Check shape within grid
    match config:
        case 0:
            if x < 0 or x > 2 or y < 0 or y > 5:
                return False
        case 1:
            if x < 0 or x > 5 or y < 0 or y > 2:
                return False
        case 2:
            if x < 3 or x > 5 or y < 0 or y > 5:
                return False
        case 3:
            if x < 0 or x > 5 or y < 3 or y > 5:
                return False
        case 4:
            if x < 1 or x > 3 or y < 0 or y > 5:
                return False
        case 5:
            if x < 2 or x > 4 or y < 0 or y > 5:
                return False
        case 6:
            if x < 0 or x > 5 or y < 1 or y > 3:
                return False
        case 7:
            if x < 0 or x > 5 or y < 2 or y > 4:
                return False
    
    #Check if destination occupied on grid
    match config:
        case 0:
            if grid[y][x] != EMPTY_ID or grid[y][x+1] != EMPTY_ID or grid[y][x+2] != EMPTY_ID or grid[y][x+3] != EMPTY_ID:
                return False
        case 1:
            if grid[y][x] != EMPTY_ID or grid[y+1][x] != EMPTY_ID or grid[y+2][x] != EMPTY_ID or grid[y+3][x] != EMPTY_ID:
                return False
        case 2:
            if grid[y][x] != EMPTY_ID or grid[y][x-1] != EMPTY_ID or grid[y][x-2] != EMPTY_ID or grid[y][x-3] != EMPTY_ID:
                return False
        case 3:
            if grid[y][x] != EMPTY_ID or grid[y-1][x] != EMPTY_ID or grid[y-2][x] != EMPTY_ID or grid[y-3][x] != EMPTY_ID:
                return False
        case 4:
            if grid[y][x] != EMPTY_ID or grid[y][x-1] != EMPTY_ID or grid[y][x+1] != EMPTY_ID or grid[y][x+2] != EMPTY_ID:
                return False
        case 5:
            if grid[y][x] != EMPTY_ID or grid[y][x+1] != EMPTY_ID or grid[y][x-1] != EMPTY_ID or grid[y][x-2] != EMPTY_ID:
                return False
        case 6:
            if grid[y][x] != EMPTY_ID or grid[y-1][x] != EMPTY_ID or grid[y+1][x] != EMPTY_ID or grid[y+2][x] != EMPTY_ID:
                return False
        case 7:
            if grid[y][x] != EMPTY_ID or grid[y+1][x] != EMPTY_ID or grid[y-1][x] != EMPTY_ID or grid[y-2][x] != EMPTY_ID:
                return False 
                
    return True

def placeLongBarOnGrid(grid: list[list[int, int]], pieceCoordinates: dict[int, tuple[int, int]], x: int, y: int, config: int) -> tuple[list[list[int, int]], dict[int, tuple[int, int]]]:
    """ 
    Places a long bar onto a given grid at the given coordinates

    Parameters:
        LIST<LIST<INT, INT>> grid
        DICT<INT, TUPLE<INT, INT>> pieceCoordinates
        INT x
        INT y
        INT config
    Returns:
        TUPLE<LIST<LIST<INT, INT>> grid, DICT<INT, TUPLE<INT, INT>> pieceCoordinates>
    """
    """       
    0:  x o o o
                
    1:  x
        o
        o
        o
        
    2:  o o o x
                
    3:  o
        o
        o
        x
    
    4: o x o o
    
    5: o o x o
    
    6: o
        x
        o
        o
    
    7: o
        o
        x
        o     
    """
    match config:
        case 0:
            grid[y][x] = LONG_BAR_PIECE_ID
            grid[y][x+1] = LONG_BAR_PIECE_ID
            grid[y][x+2] = LONG_BAR_PIECE_ID
            grid[y][x+3] = LONG_BAR_PIECE_ID
            pieceCoordinates[LONG_BAR_PIECE_ID] = [(x, y), (x+1, y), (x+2, y), (x+3, y)]
        case 1:
            grid[y][x] = LONG_BAR_PIECE_ID
            grid[y+1][x] = LONG_BAR_PIECE_ID
            grid[y+2][x] = LONG_BAR_PIECE_ID
            grid[y+3][x] = LONG_BAR_PIECE_ID
            pieceCoordinates[LONG_BAR_PIECE_ID] = [(x, y), (x, y+1), (x, y+2), (x, y+3)]
        case 2:
            grid[y][x] = LONG_BAR_PIECE_ID
            grid[y][x-1] = LONG_BAR_PIECE_ID
            grid[y][x-2] = LONG_BAR_PIECE_ID
            grid[y][x-3] = LONG_BAR_PIECE_ID
            pieceCoordinates[LONG_BAR_PIECE_ID] = [(x, y), (x-1, y), (x-2, y), (x-3, y)]
        case 3:
            grid[y][x] = LONG_BAR_PIECE_ID
            grid[y-1][x] = LONG_BAR_PIECE_ID
            grid[y-2][x] = LONG_BAR_PIECE_ID
            grid[y-3][x] = LONG_BAR_PIECE_ID
            pieceCoordinates[LONG_BAR_PIECE_ID] = [(x, y), (x, y-1), (x, y-2), (x, y-3)]
        case 4:
            grid[y][x] = LONG_BAR_PIECE_ID 
            grid[y][x-1] = LONG_BAR_PIECE_ID
            grid[y][x+1] = LONG_BAR_PIECE_ID 
            grid[y][x+2] = LONG_BAR_PIECE_ID
            pieceCoordinates[LONG_BAR_PIECE_ID] = [(x, y), (x-1, y), (x+1, y), (x+2, y)]
        case 5:
            grid[y][x] = LONG_BAR_PIECE_ID 
            grid[y][x+1] = LONG_BAR_PIECE_ID 
            grid[y][x-1] = LONG_BAR_PIECE_ID 
            grid[y][x-2] = LONG_BAR_PIECE_ID
            pieceCoordinates[LONG_BAR_PIECE_ID] = [(x, y), (x+1, y), (x-1, y), (x-2, y)]
        case 6:
            grid[y][x] = LONG_BAR_PIECE_ID
            grid[y-1][x] = LONG_BAR_PIECE_ID 
            grid[y+1][x] = LONG_BAR_PIECE_ID
            grid[y+2][x] = LONG_BAR_PIECE_ID
            pieceCoordinates[LONG_BAR_PIECE_ID] = [(x, y), (x, y-1), (x, y+1), (x, y+2)]
        case 7:
            grid[y][x] = LONG_BAR_PIECE_ID 
            grid[y+1][x] = LONG_BAR_PIECE_ID 
            grid[y-1][x] = LONG_BAR_PIECE_ID 
            grid[y-2][x] = LONG_BAR_PIECE_ID
            pieceCoordinates[LONG_BAR_PIECE_ID] = [(x, y), (x, y+1), (x, y-1), (x, y-2)]
    
    return grid, pieceCoordinates

def isMoveValidL(grid: list[list[int, int]], x: int, y: int, config: int) -> bool:
    """ 
    Validates whether an l can be placed onto a given grid at the given coordinates

    Parameters:
        LIST<LIST<INT, INT>> grid
        INT x
        INT y
        INT config
    Returns:
        BOOL
    """ 
    """ 
    0:
        x
        o
      o o
        
    1:
        o
        x
      o o
      
    2:
        o
        o
      o x
     
    3:
        o
        o
      x o
      
    4:
        x
        o o o
        
    5:
        o
        x o o
        
    6:
        o
        o x o
        
    7:
        o
        o o x
        
    8:
        o x
        o
        o
        
    9:
        x o
        o
        o
        
    10:
        o o
        x
        o
        
    11:
        o o
        o
        x
        
    12:
        x o o
            o

    13:
        o x o
            o

    14:
        o o x
            o

    15:
        o o o
            x

    16:
        x
        o
        o o

    17:
        o
        x
        o o

    18:
        o
        o
        x o

    19:
        o
        o
        o x

    20:
            o
        x o o

    21:
            o
        o x o

    22:
            o
        o o x

    23:
            x
        o o o

    24:
        x o
          o
          o

    25:
        o x
          o
          o

    26:
        o o
          x
          o

    27:
        o o
          o
          x

    28:
        o o o
        x
    
    29:
        x o o
        o         

    30:
        o x o
        o
    
    31:
        o o x
        o
    """
    match config:
        case 0:
            if x < 1 or x > 5 or y < 0 or y > 3:
                return False
        case 1:
            if x < 1 or x > 5 or y < 1 or y > 4:
                return False
        case 2:
            if x < 1 or x > 5 or y < 2 or y > 5:
                return False
        case 3:   
            if x < 0 or x > 4 or y < 2 or y > 5:
                return False 
        case 4:
            if x < 0 or x > 3 or y < 0 or y > 4:
                return False
        case 5:
            if x < 0 or x > 3 or y < 1 or y > 5:
                return False
        case 6:
            if x < 1 or x > 4 or y < 1 or y > 5:
                return False
        case 7:
            if x < 2 or x > 5 or y < 1 or y > 5:
                return False
        case 8:
            if x < 1 or x > 5 or y < 0 or y > 3:
                return False
        case 9:
            if x < 0 or x > 4 or y < 0 or y > 3:
                return False
        case 10:
            if x < 0 or x > 4 or y < 1 or y > 4:
                return False
        case 11:
            if x < 0 or x > 4 or y < 2 or y > 5:
                return False
        case 12:
            if x < 0 or x > 3 or y < 0 or y > 4:
                return False
        case 13:
            if x < 1 or x > 4 or y < 0 or y > 4:
                return False
        case 14:
            if x < 2 or x > 5 or y < 0 or y > 4:
                return False
        case 15:
            if x < 2 or x > 5 or y < 1 or y > 5:
                return False
        case 16:
            if x < 0 or x > 4 or y < 0 or y > 3:
                return False
        case 17:
            if x < 0 or x > 4 or y < 1 or y > 4:
                return False
        case 18:
            if x < 0 or x > 4 or y < 2 or y > 5:
                return False
        case 19:
            if x < 1 or x > 5 or y < 2 or y > 5:
                return False
        case 20:
            if x < 0 or x > 3 or y < 1 or y > 5:
                return False
        case 21:
            if x < 1 or x > 4 or y < 1 or y > 5:
                return False
        case 22:
            if x < 2 or x > 5 or y < 1 or y > 5:
                return False
        case 23:
            if x < 2 or x > 5 or y < 0 or y > 4:
                return False
        case 24:
            if x < 0 or x > 4 or y < 0 or y > 3:
                return False
        case 25:
            if x < 1 or x > 5 or y < 0 or y > 3:
                return False
        case 26:
            if x < 1 or x > 5 or y < 1 or y > 4:
                return False
        case 27:
            if x < 1 or x > 5 or y < 2 or y > 5:
                return False
        case 28:
            if x < 0 or x > 3 or y < 1 or y > 5:
                return False
        case 29:
            if x < 0 or x > 3 or y < 0 or y > 4:
                return False
        case 30:
            if x < 1 or x > 4 or y < 0 or y > 4:
                return False
        case 31:
            if x < 2 or x > 5 or y < 0 or y > 4:
                return False
        
    match config:
        case 0:
            if grid[y][x] != EMPTY_ID or grid[y+1][x] != EMPTY_ID or grid[y+2][x] != EMPTY_ID or grid[y+2][x-1] != EMPTY_ID:
                return False
        case 1:
            if grid[y][x] != EMPTY_ID or grid[y-1][x] != EMPTY_ID or grid[y+1][x] != EMPTY_ID or grid[y+1][x-1] != EMPTY_ID:
                return False
        case 2:
            if grid[y][x] != EMPTY_ID or grid[y][x-1] != EMPTY_ID or grid[y-1][x] != EMPTY_ID or grid[y-2][x] != EMPTY_ID:
                return False
        case 3:
            if grid[y][x] != EMPTY_ID or grid[y][x+1] != EMPTY_ID or grid[y-1][x+1] != EMPTY_ID or grid[y-2][x+1] != EMPTY_ID:
                return False
        case 4:
            if grid[y][x] != EMPTY_ID or grid[y+1][x] != EMPTY_ID or grid[y+1][x+1] != EMPTY_ID or grid[y+1][x+2] != EMPTY_ID:
                return False
        case 5:
            if grid[y][x] != EMPTY_ID or grid[y-1][x] != EMPTY_ID or grid[y][x+1] != EMPTY_ID or grid[y][x+2] != EMPTY_ID:
                return False
        case 6:
            if grid[y][x] != EMPTY_ID or grid[y][x+1] != EMPTY_ID or grid[y][x-1] != EMPTY_ID or grid[y-1][x-1] != EMPTY_ID:
                return False
        case 7:
            if grid[y][x] != EMPTY_ID or grid[y][x-1] != EMPTY_ID or grid[y][x-2] != EMPTY_ID or grid[y-1][x-2] != EMPTY_ID:
                return False
        case 8:
            if grid[y][x] != EMPTY_ID or grid[y][x-1] != EMPTY_ID or grid[y+1][x-1] != EMPTY_ID or grid[y+2][x-1] != EMPTY_ID:
                return False
        case 9:
            if grid[y][x] != EMPTY_ID or grid[y][x+1] != EMPTY_ID or grid[y+1][x] != EMPTY_ID or grid[y+2][x] != EMPTY_ID:
                return False    
        case 10:
            if grid[y][x] != EMPTY_ID or grid[y+1][x] != EMPTY_ID or grid[y-1][x] != EMPTY_ID or grid[y-1][x+1] != EMPTY_ID:
                return False  
        case 11:
            if grid[y][x] != EMPTY_ID or grid[y-1][x] != EMPTY_ID or grid[y-2][x] != EMPTY_ID or grid[y-2][x+1] != EMPTY_ID:
                return False  
        case 12:
            if grid[y][x] != EMPTY_ID or grid[y][x+1] != EMPTY_ID or grid[y][x+2] != EMPTY_ID or grid[y+1][x+2] != EMPTY_ID:
                return False 
        case 13:
            if grid[y][x] != EMPTY_ID or grid[y][x-1] != EMPTY_ID or grid[y][x+1] != EMPTY_ID or grid[y+1][x+1] != EMPTY_ID:
                return False 
        case 14:
            if grid[y][x] != EMPTY_ID or grid[y+1][x] != EMPTY_ID or grid[y][x-1] != EMPTY_ID or grid[y][x-2] != EMPTY_ID:
                return False 
        case 15:
            if grid[y][x] != EMPTY_ID or grid[y-1][x] != EMPTY_ID or grid[y-1][x-1] != EMPTY_ID or grid[y-1][x-2] != EMPTY_ID: 
                return False  
        case 16:
            if grid[y][x] != EMPTY_ID or grid[y+1][x] != EMPTY_ID or grid[y+2][x] != EMPTY_ID or grid[y+2][x+1] != EMPTY_ID: 
                return False  
        case 17:
            if grid[y][x] != EMPTY_ID or grid[y-1][x] != EMPTY_ID or grid[y+1][x] != EMPTY_ID or grid[y+1][x+1] != EMPTY_ID: 
                return False  
        case 18:
            if grid[y][x] != EMPTY_ID or grid[y][x+1] != EMPTY_ID or grid[y-1][x] != EMPTY_ID or grid[y-2][x] != EMPTY_ID: 
                return False  
        case 19:
            if grid[y][x] != EMPTY_ID or grid[y][x-1] != EMPTY_ID or grid[y-1][x-1] != EMPTY_ID or grid[y-2][x-1] != EMPTY_ID:
                return False     
        case 20:
            if grid[y][x] != EMPTY_ID or grid[y][x+1] != EMPTY_ID or grid[y][x+2] != EMPTY_ID or grid[y-1][x+2] != EMPTY_ID: 
                return False  
        case 21:
            if grid[y][x] != EMPTY_ID or grid[y][x-1] != EMPTY_ID or grid[y][x+1] != EMPTY_ID or grid[y-1][x+1] != EMPTY_ID: 
                return False  
        case 22:
            if grid[y][x] != EMPTY_ID or grid[y-1][x] != EMPTY_ID or grid[y][x-1] != EMPTY_ID or grid[y][x-2] != EMPTY_ID: 
                return False  
        case 23:
            if grid[y][x] != EMPTY_ID or grid[y+1][x] != EMPTY_ID or grid[y+1][x-1] != EMPTY_ID or grid[y+1][x-2] != EMPTY_ID:
                return False       
        case 24:
            if grid[y][x] != EMPTY_ID or grid[y][x+1] != EMPTY_ID or grid[y+1][x+1] != EMPTY_ID or grid[y+2][x+1] != EMPTY_ID:
                return False       
        case 25:
            if grid[y][x] != EMPTY_ID or grid[y][x-1] != EMPTY_ID or grid[y+1][x] != EMPTY_ID or grid[y+2][x] != EMPTY_ID: 
                return False    
        case 26:
            if grid[y][x] != EMPTY_ID or grid[y+1][x] != EMPTY_ID or grid[y-1][x] != EMPTY_ID or grid[y-1][x-1] != EMPTY_ID: 
                return False    
        case 27:
            if grid[y][x] != EMPTY_ID or grid[y-1][x] != EMPTY_ID or grid[y-2][x] != EMPTY_ID or grid[y-2][x-1] != EMPTY_ID: 
                return False                                   
        case 28:
            if grid[y][x] != EMPTY_ID or grid[y-1][x] != EMPTY_ID or grid[y-1][x+1] != EMPTY_ID or grid[y-1][x+2] != EMPTY_ID:
                return False  
        case 29:
            if grid[y][x] != EMPTY_ID or grid[y][x+1] != EMPTY_ID or grid[y][x+2] != EMPTY_ID or grid[y+1][x] != EMPTY_ID: 
                return False   
        case 30:
            if grid[y][x] != EMPTY_ID or grid[y][x+1] != EMPTY_ID or grid[y][x-1] != EMPTY_ID or grid[y+1][x-1] != EMPTY_ID: 
                return False 
        case 31:
            if grid[y][x] != EMPTY_ID or grid[y][x-1] != EMPTY_ID or grid[y][x-2] != EMPTY_ID or grid[y+1][x-2] != EMPTY_ID: 
                return False 
            
    return True

def placeLOnGrid(grid: list[list[int, int]], pieceCoordinates: dict[int, tuple[int, int]], x: int, y: int, config: int) -> tuple[list[list[int, int]], dict[int, tuple[int, int]]]:
    """ 
    Places an l onto a given grid at the given coordinates

    Parameters:
        LIST<LIST<INT, INT>> grid
        DICT<INT, TUPLE<INT, INT>> pieceCoordinates
        INT x
        INT y
        INT config
    Returns:
        TUPLE<LIST<LIST<INT, INT>> grid, DICT<INT, TUPLE<INT, INT>> pieceCoordinates>
    """
    """ 
    0:
        x
        o
      o o
        
    1:
        o
        x
      o o
      
    2:
        o
        o
      o x
     
    3:
        o
        o
      x o
      
    4:
        x
        o o o
        
    5:
        o
        x o o
        
    6:
        o
        o x o
        
    7:
        o
        o o x
        
    8:
        o x
        o
        o
        
    9:
        x o
        o
        o
        
    10:
        o o
        x
        o
        
    11:
        o o
        o
        x
        
    12:
        x o o
            o

    13:
        o x o
            o

    14:
        o o x
            o

    15:
        o o o
            x

    16:
        x
        o
        o o

    17:
        o
        x
        o o

    18:
        o
        o
        x o

    19:
        o
        o
        o x

    20:
            o
        x o o

    21:
            o
        o x o

    22:
            o
        o o x

    23:
            x
        o o o

    24:
        x o
          o
          o

    25:
        o x
          o
          o

    26:
        o o
          x
          o

    27:
        o o
          o
          x

    28:
        o o o
        x
    
    29:
        x o o
        o         

    30:
        o x o
        o
    
    31:
        o o x
        o
    """
    match config:
        case 0:
            grid[y][x] = L_PIECE_ID 
            grid[y+1][x] = L_PIECE_ID 
            grid[y+2][x] = L_PIECE_ID
            grid[y+2][x-1] = L_PIECE_ID
            pieceCoordinates[L_PIECE_ID] = [(x, y), (x, y+1), (x, y+2), (x-1, y+2)]
        case 1:
            grid[y][x] = L_PIECE_ID  
            grid[y-1][x] = L_PIECE_ID  
            grid[y+1][x] = L_PIECE_ID  
            grid[y+1][x-1] = L_PIECE_ID
            pieceCoordinates[L_PIECE_ID] = [(x, y), (x, y-1), (x, y+1), (x-1, y+1)]
        case 2:
            grid[y][x] = L_PIECE_ID  
            grid[y][x-1] = L_PIECE_ID  
            grid[y-1][x] = L_PIECE_ID  
            grid[y-2][x] = L_PIECE_ID
            pieceCoordinates[L_PIECE_ID] = [(x, y), (x-1, y), (x, y-1), (x, y-2)]
        case 3:
            grid[y][x] = L_PIECE_ID
            grid[y][x+1] = L_PIECE_ID
            grid[y-1][x+1] = L_PIECE_ID
            grid[y-2][x+1] = L_PIECE_ID
            pieceCoordinates[L_PIECE_ID] = [(x, y), (x+1, y), (x+1, y-1), (x+1, y-2)]
        case 4:
            grid[y][x] = L_PIECE_ID
            grid[y+1][x] = L_PIECE_ID
            grid[y+1][x+1] = L_PIECE_ID
            grid[y+1][x+2] = L_PIECE_ID
            pieceCoordinates[L_PIECE_ID] = [(x, y), (x, y+1), (x+1, y+1), (x+2, y+1)]
        case 5:
            grid[y][x] = L_PIECE_ID  
            grid[y-1][x] = L_PIECE_ID  
            grid[y][x+1] = L_PIECE_ID  
            grid[y][x+2] = L_PIECE_ID
            pieceCoordinates[L_PIECE_ID] = [(x, y), (x, y-1), (x+1, y), (x+2, y)]
        case 6:
            grid[y][x] = L_PIECE_ID  
            grid[y][x+1] = L_PIECE_ID  
            grid[y][x-1] = L_PIECE_ID  
            grid[y-1][x-1] = L_PIECE_ID
            pieceCoordinates[L_PIECE_ID] = [(x, y), (x+1, y), (x-1, y), (x-1, y-1)]
        case 7:
            grid[y][x] = L_PIECE_ID  
            grid[y][x-1] = L_PIECE_ID  
            grid[y][x-2] = L_PIECE_ID  
            grid[y-1][x-2] = L_PIECE_ID
            pieceCoordinates[L_PIECE_ID] = [(x, y), (x-1, y), (x-2, y), (x-2, y-1)]
        case 8:
            grid[y][x] = L_PIECE_ID
            grid[y][x-1] = L_PIECE_ID
            grid[y-1][x-1] = L_PIECE_ID
            grid[y-2][x-1] = L_PIECE_ID
            pieceCoordinates[L_PIECE_ID] = [(x, y), (x-1, y), (x-1, y-1), (x-1, y-2)]
        case 9:
            grid[y][x] = L_PIECE_ID  
            grid[y][x+1] = L_PIECE_ID  
            grid[y+1][x] = L_PIECE_ID  
            grid[y+2][x] = L_PIECE_ID
            pieceCoordinates[L_PIECE_ID] = [(x, y), (x+1, y), (x, y+1), (x, y+2)]
        case 10:
            grid[y][x] = L_PIECE_ID  
            grid[y+1][x] = L_PIECE_ID  
            grid[y-1][x] = L_PIECE_ID  
            grid[y-1][x+1] = L_PIECE_ID
            pieceCoordinates[L_PIECE_ID] = [(x, y), (x, y+1), (x, y-1), (x+1, y-1)]
        case 11:
            grid[y][x] = L_PIECE_ID  
            grid[y-1][x] = L_PIECE_ID 
            grid[y-2][x] = L_PIECE_ID  
            grid[y-2][x+1] = L_PIECE_ID
            pieceCoordinates[L_PIECE_ID] = [(x, y), (x, y-1), (x, y-2), (x+1, y-2)]
        case 12:
            grid[y][x] = L_PIECE_ID  
            grid[y][x+1] = L_PIECE_ID  
            grid[y][x+2] = L_PIECE_ID  
            grid[y+1][x+2] = L_PIECE_ID
            pieceCoordinates[L_PIECE_ID] = [(x, y), (x+1, y), (x+2, y), (x+2, y+1)]
        case 13:
            grid[y][x] = L_PIECE_ID  
            grid[y][x-1] = L_PIECE_ID  
            grid[y][x+1] = L_PIECE_ID  
            grid[y+1][x+1] = L_PIECE_ID
            pieceCoordinates[L_PIECE_ID] = [(x, y), (x-1, y), (x+1, y), (x+1, y+1)]
        case 14:
            grid[y][x] = L_PIECE_ID  
            grid[y+1][x] = L_PIECE_ID  
            grid[y][x-1] = L_PIECE_ID  
            grid[y][x-2] = L_PIECE_ID
            pieceCoordinates[L_PIECE_ID] = [(x, y), (x, y+1), (x-1, y), (x-2, y)]
        case 15:
            grid[y][x] = L_PIECE_ID 
            grid[y-1][x] != L_PIECE_ID 
            grid[y-1][x-1] = L_PIECE_ID 
            grid[y-1][x-2] = L_PIECE_ID
            pieceCoordinates[L_PIECE_ID] = [(x, y), (x, y-1), (x-1, y-1), (x-2, y-1)]
        case 16:
            grid[y][x] = L_PIECE_ID  
            grid[y+1][x] = L_PIECE_ID  
            grid[y+2][x] = L_PIECE_ID  
            grid[y+2][x+1] = L_PIECE_ID 
            pieceCoordinates[L_PIECE_ID] = [(x, y), (x, y+1), (x, y+2), (x+1, y+2)]
        case 17:
            grid[y][x] = L_PIECE_ID  
            grid[y-1][x] = L_PIECE_ID  
            grid[y+1][x] = L_PIECE_ID  
            grid[y+1][x+1] = L_PIECE_ID 
            pieceCoordinates[L_PIECE_ID] = [(x, y), (x, y-1), (x, y+1), (x+1, y+1)]
        case 18:
            grid[y][x] = L_PIECE_ID  
            grid[y][x+1] = L_PIECE_ID  
            grid[y-1][x] = L_PIECE_ID  
            grid[y-2][x] = L_PIECE_ID 
            pieceCoordinates[L_PIECE_ID] = [(x, y), (x+1, y), (x, y-1), (x, y-2)]
        case 19:
            grid[y][x] = L_PIECE_ID
            grid[y][x-1] = L_PIECE_ID
            grid[y-1][x-1] = L_PIECE_ID
            grid[y-2][x-1] = L_PIECE_ID
            pieceCoordinates[L_PIECE_ID] = [(x, y), (x-1, y), (x-1, y-1), (x-1, y-2)]
        case 20:
            grid[y][x] = L_PIECE_ID 
            grid[y][x+1] = L_PIECE_ID  
            grid[y][x+2] = L_PIECE_ID  
            grid[y-1][x+2] = L_PIECE_ID 
            pieceCoordinates[L_PIECE_ID] = [(x, y), (x+1, y), (x+2, y), (x+2, y-1)]
        case 21:
            grid[y][x] = L_PIECE_ID  
            grid[y][x-1] = L_PIECE_ID  
            grid[y][x+1] = L_PIECE_ID  
            grid[y-1][x+1] = L_PIECE_ID 
            pieceCoordinates[L_PIECE_ID] = [(x, y), (x-1, y), (x+1, y), (x+1, y-1)]
        case 22:
            grid[y][x] = L_PIECE_ID  
            grid[y-1][x] = L_PIECE_ID 
            grid[y][x-1] = L_PIECE_ID  
            grid[y][x-2] = L_PIECE_ID 
            pieceCoordinates[L_PIECE_ID] = [(x, y), (x, y-1), (x-1, y), (x-2, y)]
        case 23:
            grid[y][x] = L_PIECE_ID
            grid[y+1][x] = L_PIECE_ID
            grid[y+1][x-1] = L_PIECE_ID
            grid[y+1][x-2] = L_PIECE_ID
            pieceCoordinates[L_PIECE_ID] = [(x, y), (x, y+1), (x-1, y+1), (x-2, y+1)]
        case 24:
            grid[y][x] = L_PIECE_ID
            grid[y][x+1] = L_PIECE_ID
            grid[y+1][x+1] = L_PIECE_ID
            grid[y+2][x+1] = L_PIECE_ID
            pieceCoordinates[L_PIECE_ID] = [(x, y), (x+1, y), (x+1, y+1), (x+1, y+2)]
        case 25:
            grid[y][x] = L_PIECE_ID  
            grid[y][x-1] = L_PIECE_ID  
            grid[y+1][x] = L_PIECE_ID  
            grid[y+2][x] = L_PIECE_ID 
            pieceCoordinates[L_PIECE_ID] = [(x, y), (x-1, y), (x, y+1), (x, y+2)]
        case 26:
            grid[y][x] = L_PIECE_ID  
            grid[y+1][x] = L_PIECE_ID  
            grid[y-1][x] = L_PIECE_ID  
            grid[y-1][x-1] = L_PIECE_ID 
            pieceCoordinates[L_PIECE_ID] = [(x, y), (x, y+1), (x, y-1), (x-1, y-1)]
        case 27:
            grid[y][x] = L_PIECE_ID  
            grid[y-1][x] = L_PIECE_ID  
            grid[y-2][x] = L_PIECE_ID  
            grid[y-2][x-1] = L_PIECE_ID 
            pieceCoordinates[L_PIECE_ID] = [(x, y), (x, y-1), (x, y-2), (x-1, y-2)]
        case 28:
            grid[y][x] = L_PIECE_ID
            grid[y-1][x] = L_PIECE_ID 
            grid[y-1][x+1] = L_PIECE_ID 
            grid[y-1][x+2] = L_PIECE_ID
            pieceCoordinates[L_PIECE_ID] = [(x, y), (x, y-1), (x+1, y-1), (x+2, y-1)]
        case 29:
            grid[y][x] = L_PIECE_ID  
            grid[y][x+1] = L_PIECE_ID  
            grid[y][x+2] = L_PIECE_ID  
            grid[y+1][x] = L_PIECE_ID 
            pieceCoordinates[L_PIECE_ID] = [(x, y), (x+1, y), (x+2, y), (x, y+1)]
        case 30:
            grid[y][x] = L_PIECE_ID  
            grid[y][x+1] = L_PIECE_ID  
            grid[y][x-1] = L_PIECE_ID  
            grid[y+1][x-1] = L_PIECE_ID 
            pieceCoordinates[L_PIECE_ID] = [(x, y), (x+1, y), (x-1, y), (x-1, y+1)]
        case 31:
            grid[y][x] = L_PIECE_ID  
            grid[y][x-1] = L_PIECE_ID  
            grid[y][x-2] = L_PIECE_ID  
            grid[y+1][x-2] = L_PIECE_ID 
            pieceCoordinates[L_PIECE_ID] = [(x, y), (x-1, y), (x-2, y), (x-2, y+1)]
             
    return grid, pieceCoordinates

def isMoveValidT(grid: list[list[int, int]], x: int, y: int, config: int) -> bool:
    """ 
    Validates whether a t can be placed onto a given grid at the given coordinates

    Parameters:
        LIST<LIST<INT, INT>> grid
        INT x
        INT y
        INT config
    Returns:
        BOOL
    """ 
    """ 
    0: 
          x
        o o o
    1: 
          o
        x o o    
    2:
          o
        o x o    
    3:
          o
        o o x
    4:
        x
        o o
        o
    5:
        o
        x o
        o    
    6:
        o
        o o
        x    
    7:
        o
        o x
        o    
    8:
        x o o
          o
    9:
        o x o
          o    
    10:
        o o x
          o    
    11:
        o o o
          x    
    12:
          x
        o o
          o
    13:
          o
        x o
          o    
    14:
          o
        o x
          o    
    15:
          o
        o o
          x    
    """
    match config:
        case 0:
            if x < 1 or x > 4 or y < 0 or y > 4:
                return False
        case 1:
            if x < 0 or x > 3 or y < 1 or y > 5:
                return False
        case 2:
            if x < 1 or x > 4 or y < 1 or y > 5:
                return False
        case 3:   
            if x < 2 or x > 5 or y < 1 or y > 5:
                return False
        case 4:
            if x < 0 or x > 4 or y < 0 or y > 3:
                return False  
        case 5:
            if x < 0 or x > 4 or y < 1 or y > 4:
                return False
        case 6:
            if x < 0 or x > 4 or y < 2 or y > 5:
                return False
        case 7:
            if x < 1 or x > 5 or y < 1 or y > 4:
                return False
        case 8:
            if x < 0 or x > 3 or y < 0 or y > 4:
                return False
        case 9:
            if x < 1 or x > 4 or y < 0 or y > 4:
                return False
        case 10:
            if x < 2 or x > 5 or y < 0 or y > 4:
                return False
        case 11:
            if x < 1 or x > 4 or y < 1 or y > 5:
                return False
        case 12:
            if x < 1 or x > 5 or y < 0 or y > 3:
                return False
        case 13:
            if x < 0 or x > 4 or y < 1 or y > 4:
                return False
        case 14:
            if x < 1 or x > 5 or y < 1 or y > 4:
                return False
        case 15:
            if x < 1 or x > 5 or y < 2 or y > 5:
                return False
            
    match config:
        case 0:
            if grid[y][x] != EMPTY_ID or grid[y+1][x-1] != EMPTY_ID or grid[y+1][x] != EMPTY_ID or grid[y+1][x+1] != EMPTY_ID:
                return False
        case 1:
            if grid[y][x] != EMPTY_ID or grid[y][x+1] != EMPTY_ID or grid[y][x+2] != EMPTY_ID or grid[y-1][x+1] != EMPTY_ID:
                return False
        case 2:
            if grid[y][x] != EMPTY_ID or grid[y][x-1] != EMPTY_ID or grid[y][x+1] != EMPTY_ID or grid[y-1][x] != EMPTY_ID:
                return False
        case 3:
            if grid[y][x] != EMPTY_ID or grid[y][x-1] != EMPTY_ID or grid[y][x-2] != EMPTY_ID or grid[y-1][x-1] != EMPTY_ID:
                return False
        case 4:
            if grid[y][x] != EMPTY_ID or grid[y+1][x] != EMPTY_ID or grid[y+2][x] != EMPTY_ID or grid[y+1][x+1] != EMPTY_ID:
                return False
        case 5:
            if grid[y][x] != EMPTY_ID or grid[y-1][x] != EMPTY_ID or grid[y+1][x] != EMPTY_ID or grid[y][x+1] != EMPTY_ID:
                return False
        case 6:
            if grid[y][x] != EMPTY_ID or grid[y-1][x] != EMPTY_ID or grid[y-2][x] != EMPTY_ID or grid[y-1][x+1] != EMPTY_ID:
                return False
        case 7:
            if grid[y][x] != EMPTY_ID or grid[y][x-1] != EMPTY_ID or grid[y-1][x-1] != EMPTY_ID or grid[y+1][x-1] != EMPTY_ID:
                return False
        case 8:
            if grid[y][x] != EMPTY_ID or grid[y][x+1] != EMPTY_ID or grid[y][x+2] != EMPTY_ID or grid[y+1][x+1] != EMPTY_ID:
                return False
        case 9:
            if grid[y][x] != EMPTY_ID or grid[y][x-1] != EMPTY_ID or grid[y][x+1] != EMPTY_ID or grid[y+1][x] != EMPTY_ID:
                return False
        case 10:
            if grid[y][x] != EMPTY_ID or grid[y][x-1] != EMPTY_ID or grid[y][x-2] != EMPTY_ID or grid[y+1][x-1] != EMPTY_ID:
                return False
        case 11:
            if grid[y][x] != EMPTY_ID or grid[y-1][x-1] != EMPTY_ID or grid[y-1][x] != EMPTY_ID or grid[y-1][x+1] != EMPTY_ID:
                return False 
        case 12:
            if grid[y][x] != EMPTY_ID or grid[y+1][x] != EMPTY_ID or grid[y+2][x] != EMPTY_ID or grid[y+1][x-1] != EMPTY_ID:
                return False              
        case 13:
            if grid[y][x] != EMPTY_ID or grid[y-1][x] != EMPTY_ID or grid[y-1][x-1] != EMPTY_ID or grid[y-1][x+1] != EMPTY_ID:
                return False   
        case 14:
            if grid[y][x] != EMPTY_ID or grid[y-1][x] != EMPTY_ID or grid[y+1][x] != EMPTY_ID or grid[y][x-1] != EMPTY_ID:
                return False 
        case 15:
            if grid[y][x] != EMPTY_ID or grid[y-1][x] != EMPTY_ID or grid[y-2][x] != EMPTY_ID or grid[y-1][x-1] != EMPTY_ID:
                return False 
        
    return True

def placeTOnGrid(grid: list[list[int, int]], pieceCoordinates: dict[int, tuple[int, int]], x: int, y: int, config: int) -> tuple[list[list[int, int]], dict[int, tuple[int, int]]]:
    """ 
    Places a t onto a given grid at the given coordinates

    Parameters:
        LIST<LIST<INT, INT>> grid
        DICT<INT, TUPLE<INT, INT>> pieceCoordinates
        INT x
        INT y
        INT config
    Returns:
        TUPLE<LIST<LIST<INT, INT>> grid, DICT<INT, TUPLE<INT, INT>> pieceCoordinates>
    """
    """ 
    0: 
          x
        o o o
    1: 
          o
        x o o    
    2:
          o
        o x o    
    3:
          o
        o o x
    4:
        x
        o o
        o
    5:
        o
        x o
        o    
    6:
        o
        o o
        x    
    7:
        o
        o x
        o    
    8:
        x o o
          o
    9:
        o x o
          o    
    10:
        o o x
          o    
    11:
        o o o
          x    
    12:
          x
        o o
          o
    13:
          o
        x o
          o    
    14:
          o
        o x
          o    
    15:
          o
        o o
          x    
    """
    match config:
        case 0:
            grid[y][x] = T_PIECE_ID  
            grid[y+1][x-1] = T_PIECE_ID  
            grid[y+1][x] = T_PIECE_ID  
            grid[y+1][x+1] = T_PIECE_ID
            pieceCoordinates[T_PIECE_ID] = [(x, y), (x-1, y+1), (x, y+1), (x+1, y+1)]
        case 1:
            grid[y][x] = T_PIECE_ID  
            grid[y][x+1] = T_PIECE_ID  
            grid[y][x+2] = T_PIECE_ID  
            grid[y-1][x+1] = T_PIECE_ID
            pieceCoordinates[T_PIECE_ID] = [(x, y), (x+1, y), (x+2, y), (x+1, y-1)]
        case 2:
            grid[y][x] = T_PIECE_ID  
            grid[y][x-1] = T_PIECE_ID  
            grid[y][x+1] = T_PIECE_ID  
            grid[y-1][x] = T_PIECE_ID
            pieceCoordinates[T_PIECE_ID] = [(x, y), (x-1, y), (x+1, y), (x, y-1)]
        case 3:
            grid[y][x] = T_PIECE_ID  
            grid[y][x-1] = T_PIECE_ID  
            grid[y][x-2] = T_PIECE_ID  
            grid[y-1][x-1] = T_PIECE_ID
            pieceCoordinates[T_PIECE_ID] = [(x, y), (x-1, y), (x-2, y), (x-1, y-1)]
        case 4:
            grid[y][x] = T_PIECE_ID  
            grid[y+1][x] = T_PIECE_ID  
            grid[y+2][x] = T_PIECE_ID  
            grid[y+1][x+1] = T_PIECE_ID
            pieceCoordinates[T_PIECE_ID] = [(x, y), (x, y+1), (x, y+2), (x+1, y+1)]
        case 5:
            grid[y][x] = T_PIECE_ID  
            grid[y-1][x] = T_PIECE_ID  
            grid[y+1][x] = T_PIECE_ID  
            grid[y][x+1] = T_PIECE_ID
            pieceCoordinates[T_PIECE_ID] = [(x, y), (x, y-1), (x, y+1), (x+1, y)]
        case 6:
            grid[y][x] = T_PIECE_ID  
            grid[y-1][x] = T_PIECE_ID  
            grid[y-2][x] = T_PIECE_ID  
            grid[y-1][x+1] = T_PIECE_ID
            pieceCoordinates[T_PIECE_ID] = [(x, y), (x, y-1), (x, y-2), (x+1, y-1)]
        case 7:
            grid[y][x] = T_PIECE_ID  
            grid[y][x-1] = T_PIECE_ID  
            grid[y-1][x-1] = T_PIECE_ID  
            grid[y+1][x-1] = T_PIECE_ID
            pieceCoordinates[T_PIECE_ID] = [(x, y), (x-1, y), (x-1, y-1), (x-1, y+1)]
        case 8:
            grid[y][x] = T_PIECE_ID  
            grid[y][x+1] = T_PIECE_ID  
            grid[y][x+2] = T_PIECE_ID  
            grid[y+1][x+1] = T_PIECE_ID
            pieceCoordinates[T_PIECE_ID] = [(x, y), (x+1, y), (x+2, y), (x+1, y+1)]
        case 9:
            grid[y][x] = T_PIECE_ID  
            grid[y][x-1] = T_PIECE_ID  
            grid[y][x+1] = T_PIECE_ID  
            grid[y+1][x] = T_PIECE_ID
            pieceCoordinates[T_PIECE_ID] = [(x, y), (x-1, y), (x+1, y), (x, y+1)]
        case 10:
            grid[y][x] = T_PIECE_ID  
            grid[y][x-1] = T_PIECE_ID  
            grid[y][x-2] = T_PIECE_ID  
            grid[y+1][x-1] = T_PIECE_ID
            pieceCoordinates[T_PIECE_ID] = [(x, y), (x-1, y), (x-2, y), (x-1, y+1)]
        case 11:
            grid[y][x] = T_PIECE_ID  
            grid[y-1][x-1] = T_PIECE_ID  
            grid[y-1][x] = T_PIECE_ID  
            grid[y-1][x+1] = T_PIECE_ID
            pieceCoordinates[T_PIECE_ID] = [(x, y), (x-1, y-1), (x, y-1), (x+1, y-1)] 
        case 12:
            grid[y][x] = T_PIECE_ID  
            grid[y+1][x] = T_PIECE_ID  
            grid[y+2][x] = T_PIECE_ID  
            grid[y+1][x-1] = T_PIECE_ID
            pieceCoordinates[T_PIECE_ID] = [(x, y), (x, y+1), (x, y+2), (x-1, y+1)]               
        case 13:
            grid[y][x] = T_PIECE_ID  
            grid[y-1][x] = T_PIECE_ID  
            grid[y-1][x-1] = T_PIECE_ID  
            grid[y-1][x+1] = T_PIECE_ID
            pieceCoordinates[T_PIECE_ID] = [(x, y), (x, y-1), (x-1, y-1), (x+1, y-1)] 
        case 14:
            grid[y][x] = T_PIECE_ID  
            grid[y-1][x] = T_PIECE_ID  
            grid[y+1][x] = T_PIECE_ID  
            grid[y][x-1] = T_PIECE_ID
            pieceCoordinates[T_PIECE_ID] = [(x, y), (x, y-1), (x, y+1), (x-1, y)] 
        case 15:
            grid[y][x] = T_PIECE_ID  
            grid[y-1][x] = T_PIECE_ID  
            grid[y-2][x] = T_PIECE_ID  
            grid[y-1][x-1] = T_PIECE_ID
            pieceCoordinates[T_PIECE_ID] = [(x, y), (x, y-1), (x, y-2), (x-1, y-1)]   
        
    return grid, pieceCoordinates

def isMoveValidZ(grid: list[list[int, int]], x: int, y: int, config: int) -> bool:
    """ 
    Validates whether a z can be placed onto a given grid at the given coordinates

    Parameters:
        LIST<LIST<INT, INT>> grid
        INT x
        INT y
        INT config
    Returns:
        BOOL
    """ 
    """  
    0:
         x
       o o
       o
    1:
         o
       o x
       o
    2:
         o
       x o
       o    
    3:
         o
       o o
       x    
    4:
       x
       o o
         o
    5:
       o
       x o
         o    
    6:
       o
       o x
         o    
    7:
       o
       o o
         x    
    8:
        x o
          o o
    9:
        o x
          o o    
    10:
        o o
          x o    
    11:
        o o
          o x    
    12:
         o x
       o o
    13:
         x o
       o o    
    14:
         o o
       o x    
    15:
         o o
       x o
    """
    match config:
        case 0:
            if x < 1 or x > 5 or y < 0 or y > 3:
                return False
        case 1:
            if x < 1 or x > 5 or y < 1 or y > 4:
                return False
        case 2:
            if x < 0 or x > 4 or y < 1 or y > 4:
                return False
        case 3:
            if x < 0 or x > 4 or y < 2 or y > 5:
                return False
        case 4:
            if x < 0 or x > 4 or y < 0 or y > 3:
                return False
        case 5:
            if x < 0 or x > 4 or y < 1 or y > 4:
                return False
        case 6:
            if x < 1 or x > 5 or y < 1 or y > 4:
                return False
        case 7:
            if x < 1 or x > 5 or y < 2 or y > 5:
                return False
        case 8:
            if x < 0 or x > 3 or y < 0 or y > 4:
                return False
        case 9:
            if x < 1 or x > 4 or y < 0 or y > 4:
                return False
        case 10:
            if x < 1 or x > 4 or y < 1 or y > 5:
                return False
        case 11:
            if x < 2 or x > 5 or y < 1 or y > 5:
                return False
        case 12:
            if x < 2 or x > 5 or y < 0 or y > 4:
                return False
        case 13:
            if x < 1 or x > 4 or y < 0 or y > 4:
                return False
        case 14:
            if x < 1 or x > 4 or y < 1 or y > 5:
                return False
        case 15:
            if x < 0 or x > 3 or y < 1 or y > 5:
                return False
         
    match config:
        case 0:
            if grid[y][x] != EMPTY_ID or grid[y+1][x] != EMPTY_ID or grid[y+1][x-1] != EMPTY_ID or grid[y+2][x-1] != EMPTY_ID:
                return False
        case 1:
            if grid[y][x] != EMPTY_ID or grid[y-1][x] != EMPTY_ID or grid[y][x-1] != EMPTY_ID or grid[y+1][x-1] != EMPTY_ID:
                return False
        case 2:
            if grid[y][x] != EMPTY_ID or grid[y+1][x] != EMPTY_ID or grid[y][x+1] != EMPTY_ID or grid[y-1][x+1] != EMPTY_ID:
                return False
        case 3:
            if grid[y][x] != EMPTY_ID or grid[y-1][x] != EMPTY_ID or grid[y-1][x+1] != EMPTY_ID or grid[y-2][x+1] != EMPTY_ID:
                return False
        case 4:
            if grid[y][x] != EMPTY_ID or grid[y+1][x] != EMPTY_ID or grid[y+1][x+1] != EMPTY_ID or grid[y+2][x+1] != EMPTY_ID:
                return False
        case 5:
            if grid[y][x] != EMPTY_ID or grid[y-1][x] != EMPTY_ID or grid[y][x+1] != EMPTY_ID or grid[y+1][x+1] != EMPTY_ID:
                return False
        case 6:
            if grid[y][x] != EMPTY_ID or grid[y+1][x] != EMPTY_ID or grid[y][x-1] != EMPTY_ID or grid[y-1][x-1] != EMPTY_ID:
                return False
        case 7:
            if grid[y][x] != EMPTY_ID or grid[y-1][x] != EMPTY_ID or grid[y-1][x-1] != EMPTY_ID or grid[y-2][x-1] != EMPTY_ID:
                return False
        case 8:
            if grid[y][x] != EMPTY_ID or grid[y][x+1] != EMPTY_ID or grid[y+1][x+1] != EMPTY_ID or grid[y+1][x+2] != EMPTY_ID:
                return False
        case 9:
            if grid[y][x] != EMPTY_ID or grid[y][x-1] != EMPTY_ID or grid[y+1][x] != EMPTY_ID or grid[y+1][x+1] != EMPTY_ID:
                return False
        case 10:
            if grid[y][x] != EMPTY_ID or grid[y][x+1] != EMPTY_ID or grid[y-1][x] != EMPTY_ID or grid[y-1][x-1] != EMPTY_ID:
                return False
        case 11:
            if grid[y][x] != EMPTY_ID or grid[y][x-1] != EMPTY_ID or grid[y-1][x-1] != EMPTY_ID or grid[y-1][x-2] != EMPTY_ID:
                return False
        case 12:
            if grid[y][x] != EMPTY_ID or grid[y][x-1] != EMPTY_ID or grid[y+1][x-1] != EMPTY_ID or grid[y+1][x-2] != EMPTY_ID:
                return False
        case 13:
            if grid[y][x] != EMPTY_ID or grid[y][x+1] != EMPTY_ID or grid[y+1][x] != EMPTY_ID or grid[y+1][x-1] != EMPTY_ID:
                return False
        case 14:
            if grid[y][x] != EMPTY_ID or grid[y][x-1] != EMPTY_ID or grid[y-1][x] != EMPTY_ID or grid[y-1][x+1] != EMPTY_ID:
                return False
        case 15:  
            if grid[y][x] != EMPTY_ID or grid[y][x+1] != EMPTY_ID or grid[y-1][x+1] != EMPTY_ID or grid[y-1][x+2] != EMPTY_ID:
                return False
            
    return True

def placeZOnGrid(grid: list[list[int, int]], pieceCoordinates: dict[int, tuple[int, int]], x: int, y: int, config: int) -> tuple[list[list[int, int]], dict[int, tuple[int, int]]]:
    """ 
    Places a z onto a given grid at the given coordinates

    Parameters:
        LIST<LIST<INT, INT>> grid
        DICT<INT, TUPLE<INT, INT>> pieceCoordinates
        INT x
        INT y
        INT config
    Returns:
        TUPLE<LIST<LIST<INT, INT>> grid, DICT<INT, TUPLE<INT, INT>> pieceCoordinates>
    """
    """  
    0:
         x
       o o
       o
    1:
         o
       o x
       o
    2:
         o
       x o
       o    
    3:
         o
       o o
       x    
    4:
       x
       o o
         o
    5:
       o
       x o
         o    
    6:
       o
       o x
         o    
    7:
       o
       o o
         x    
    8:
        x o
          o o
    9:
        o x
          o o    
    10:
        o o
          x o    
    11:
        o o
          o x    
    12:
         o x
       o o
    13:
         x o
       o o    
    14:
         o o
       o x    
    15:
         o o
       x o
    """
    match config:
        case 0:
            grid[y][x] = Z_PIECE_ID  
            grid[y+1][x] = Z_PIECE_ID  
            grid[y+1][x-1] = Z_PIECE_ID  
            grid[y+2][x-1] = Z_PIECE_ID
            pieceCoordinates[Z_PIECE_ID] = [(x, y), (x, y+1), (x-1, y+1), (x-1, y+2)]
        case 1:
            grid[y][x] = Z_PIECE_ID  
            grid[y-1][x] = Z_PIECE_ID  
            grid[y][x-1] = Z_PIECE_ID  
            grid[y+1][x-1] = Z_PIECE_ID
            pieceCoordinates[Z_PIECE_ID] = [(x, y), (x, y-1), (x-1, y), (x-1, y+1)]
        case 2:
            grid[y][x] = Z_PIECE_ID  
            grid[y+1][x] = Z_PIECE_ID  
            grid[y][x+1] = Z_PIECE_ID  
            grid[y-1][x+1] = Z_PIECE_ID
            pieceCoordinates[Z_PIECE_ID] = [(x, y), (x, y+1), (x+1, y), (x+1, y-1)]
        case 3:
            grid[y][x] = Z_PIECE_ID  
            grid[y-1][x] = Z_PIECE_ID  
            grid[y-1][x+1] = Z_PIECE_ID  
            grid[y-2][x+1] = Z_PIECE_ID
            pieceCoordinates[Z_PIECE_ID] = [(x, y), (x, y-1), (x+1, y-1), (x+1, y-2)]
        case 4:
            grid[y][x] = Z_PIECE_ID  
            grid[y+1][x] = Z_PIECE_ID  
            grid[y+1][x+1] = Z_PIECE_ID  
            grid[y+2][x+1] = Z_PIECE_ID
            pieceCoordinates[Z_PIECE_ID] = [(x, y), (x, y+1), (x+1, y+1), (x+1, y+2)]
        case 5:
            grid[y][x] = Z_PIECE_ID  
            grid[y-1][x] = Z_PIECE_ID  
            grid[y][x+1] = Z_PIECE_ID  
            grid[y+1][x+1] = Z_PIECE_ID
            pieceCoordinates[Z_PIECE_ID] = [(x, y), (x, y-1), (x+1, y), (x+1, y+1)]
        case 6:
            grid[y][x] = Z_PIECE_ID  
            grid[y+1][x] = Z_PIECE_ID  
            grid[y][x-1] = Z_PIECE_ID  
            grid[y-1][x-1] = Z_PIECE_ID
            pieceCoordinates[Z_PIECE_ID] = [(x, y), (x, y+1), (x-1, y), (x-1, y-1)]
        case 7:
            grid[y][x] = Z_PIECE_ID  
            grid[y-1][x] = Z_PIECE_ID  
            grid[y-1][x-1] = Z_PIECE_ID  
            grid[y-2][x-1] = Z_PIECE_ID
            pieceCoordinates[Z_PIECE_ID] = [(x, y), (x, y-1), (x-1, y-1), (x-1, y-2)]
        case 8:
            grid[y][x] = Z_PIECE_ID  
            grid[y][x+1] = Z_PIECE_ID  
            grid[y+1][x+1] = Z_PIECE_ID  
            grid[y+1][x+2] = Z_PIECE_ID
            pieceCoordinates[Z_PIECE_ID] = [(x, y), (x+1, y), (x+1, y+1), (x+2, y+1)]
        case 9:
            grid[y][x] = Z_PIECE_ID  
            grid[y][x-1] = Z_PIECE_ID  
            grid[y+1][x] = Z_PIECE_ID  
            grid[y+1][x+1] = Z_PIECE_ID
            pieceCoordinates[Z_PIECE_ID] = [(x, y), (x-1, y), (x, y+1), (x+1, y+1)]
        case 10:
            grid[y][x] = Z_PIECE_ID  
            grid[y][x+1] = Z_PIECE_ID  
            grid[y-1][x] = Z_PIECE_ID  
            grid[y-1][x-1] = Z_PIECE_ID
            pieceCoordinates[Z_PIECE_ID] = [(x, y), (x+1, y), (x, y-1), (x-1, y-1)]
        case 11:
            grid[y][x] = Z_PIECE_ID  
            grid[y][x-1] = Z_PIECE_ID 
            grid[y-1][x-1] = Z_PIECE_ID 
            grid[y-1][x-2] = Z_PIECE_ID
            pieceCoordinates[Z_PIECE_ID] = [(x, y), (x-1, y), (x-1, y-1), (x-2, y-1)]
        case 12:
            grid[y][x] = Z_PIECE_ID  
            grid[y][x-1] = Z_PIECE_ID  
            grid[y+1][x-1] = Z_PIECE_ID 
            grid[y+1][x-2] = Z_PIECE_ID
            pieceCoordinates[Z_PIECE_ID] = [(x, y), (x-1, y), (x-1, y+1), (x-2, y+1)]
        case 13:
            grid[y][x] = Z_PIECE_ID  
            grid[y][x+1] = Z_PIECE_ID  
            grid[y+1][x] = Z_PIECE_ID  
            grid[y+1][x-1] = Z_PIECE_ID
            pieceCoordinates[Z_PIECE_ID] = [(x, y), (x+1, y), (x, y+1), (x-1, y+1)]
        case 14:
            grid[y][x] = Z_PIECE_ID  
            grid[y][x-1] = Z_PIECE_ID  
            grid[y-1][x] = Z_PIECE_ID  
            grid[y-1][x+1] = Z_PIECE_ID
            pieceCoordinates[Z_PIECE_ID] = [(x, y), (x-1, y), (x, y-1), (x+1, y-1)]
        case 15:
            grid[y][x] = Z_PIECE_ID  
            grid[y][x+1] = Z_PIECE_ID  
            grid[y-1][x+1] = Z_PIECE_ID  
            grid[y-1][x+2] = Z_PIECE_ID
            pieceCoordinates[Z_PIECE_ID] = [(x, y), (x+1, y), (x+1, y-1), (x+2, y-1)]
            
    return grid, pieceCoordinates

def isMoveValidArrow(grid: list[list[int, int]], x: int, y: int, config: int) -> bool:
    """ 
    Validates whether an arrow can be placed onto a given grid at the given coordinates

    Parameters:
        LIST<LIST<INT, INT>> grid
        INT x
        INT y
        INT config
    Returns:
        BOOL
    """ 
    """  
    0:
        x 
        o o
    1:
        o 
        x o    
    2:
        o 
        o x    
    3:
        o o
        x     
    4:
        x o
        o   
    5:
        o x
        o    
    6:
        x o
          o   
    7:
        o x
          o    
    8:
        o o
          x    
    9:
          o
        x o    
    10:
          o
        o x    
    11:
          x
        o o    
    """
    match config:
        case 0:
            if x < 0 or x > 4 or y < 0 or y > 4:
                return False
        case 1:
            if x < 0 or x > 4 or y < 1 or y > 5:
                return False
        case 2:
            if x < 1 or x > 5 or y < 1 or y > 5:
                return False 
        case 3:
            if x < 0 or x > 4 or y < 1 or y > 5:
                return False
        case 4:
            if x < 0 or x > 4 or y < 0 or y > 4:
                return False
        case 5:
            if x < 1 or x > 5 or y < 0 or y > 4:
                return False 
        case 6:
            if x < 0 or x > 4 or y < 0 or y > 4:
                return False
        case 7:
            if x < 1 or x > 5 or y < 0 or y > 4:
                return False
        case 8:
            if x < 1 or x > 5 or y < 1 or y > 5:
                return False 
        case 9:
            if x < 0 or x > 4 or y < 1 or y > 5:
                return False
        case 10:
            if x < 1 or x > 5 or y < 1 or y > 5:
                return False
        case 11:
            if x < 1 or x > 5 or y < 0 or y > 4:
                return False 
                                                
    match config:
        case 0:
            if grid[y][x] != EMPTY_ID or grid[y+1][x] != EMPTY_ID or grid[y+1][x+1] != EMPTY_ID:
                return False
        case 1:
            if grid[y][x] != EMPTY_ID or grid[y-1][x] != EMPTY_ID or grid[y][x+1] != EMPTY_ID:    
                return False
        case 2:
            if grid[y][x] != EMPTY_ID or grid[y][x-1] != EMPTY_ID or grid[y-1][x-1] != EMPTY_ID:
                return False
        case 3:
            if grid[y][x] != EMPTY_ID or grid[y-1][x] != EMPTY_ID or grid[y-1][x+1] != EMPTY_ID: 
                return False
        case 4:
            if grid[y][x] != EMPTY_ID or grid[y+1][x] != EMPTY_ID or grid[y][x+1] != EMPTY_ID:
                return False
        case 5:
            if grid[y][x] != EMPTY_ID or grid[y][x-1] != EMPTY_ID or grid[y+1][x-1] != EMPTY_ID:    
                return False
        case 6:
            if grid[y][x] != EMPTY_ID or grid[y][x+1] != EMPTY_ID or grid[y+1][x+1] != EMPTY_ID:
                return False
        case 7:
            if grid[y][x] != EMPTY_ID or grid[y+1][x] != EMPTY_ID or grid[y][x-1] != EMPTY_ID: 
                return False
        case 8:
            if grid[y][x] != EMPTY_ID or grid[y-1][x] != EMPTY_ID or grid[y-1][x-1] != EMPTY_ID:
                return False
        case 9:
            if grid[y][x] != EMPTY_ID or grid[y][x+1] != EMPTY_ID or grid[y-1][x+1] != EMPTY_ID:  
                return False  
        case 10:
            if grid[y][x] != EMPTY_ID or grid[y-1][x] != EMPTY_ID or grid[y][x-1] != EMPTY_ID:
                return False
        case 11:
            if grid[y][x] != EMPTY_ID or grid[y+1][x] != EMPTY_ID or grid[y+1][x-1] != EMPTY_ID: 
                return False
                    
    return True

def placeArrowOnGrid(grid: list[list[int, int]], pieceCoordinates: dict[int, tuple[int, int]], x: int, y: int, config: int) -> tuple[list[list[int, int]], dict[int, tuple[int, int]]]:
    """ 
    Places an arrow onto a given grid at the given coordinates

    Parameters:
        LIST<LIST<INT, INT>> grid
        DICT<INT, TUPLE<INT, INT>> pieceCoordinates
        INT x
        INT y
        INT config
    Returns:
        TUPLE<LIST<LIST<INT, INT>> grid, DICT<INT, TUPLE<INT, INT>> pieceCoordinates>
    """
    """  
    0:
        x 
        o o
    1:
        o 
        x o    
    2:
        o 
        o x    
    3:
        o o
        x     
    4:
        x o
        o   
    5:
        o x
        o    
    6:
        x o
          o   
    7:
        o x
          o    
    8:
        o o
          x    
    9:
          o
        x o    
    10:
          o
        o x    
    11:
          x
        o o    
    """
    match config:
        case 0:
            grid[y][x] = ARROW_PIECE_ID  
            grid[y+1][x] = ARROW_PIECE_ID  
            grid[y+1][x+1] = ARROW_PIECE_ID
            pieceCoordinates[ARROW_PIECE_ID] = [(x, y), (x, y+1), (x+1, y+1)]
        case 1:
            grid[y][x] = ARROW_PIECE_ID  
            grid[y-1][x] = ARROW_PIECE_ID  
            grid[y][x+1] = ARROW_PIECE_ID    
            pieceCoordinates[ARROW_PIECE_ID] = [(x, y), (x, y-1), (x+1, y)]
        case 2:
            grid[y][x] = ARROW_PIECE_ID  
            grid[y][x-1] = ARROW_PIECE_ID  
            grid[y-1][x-1] = ARROW_PIECE_ID
            pieceCoordinates[ARROW_PIECE_ID] = [(x, y), (x-1, y), (x-1, y-1)]
        case 3:
            grid[y][x] = ARROW_PIECE_ID  
            grid[y-1][x] = ARROW_PIECE_ID  
            grid[y-1][x+1] = ARROW_PIECE_ID 
            pieceCoordinates[ARROW_PIECE_ID] = [(x, y), (x, y-1), (x+1, y-1)]
        case 4:
            grid[y][x] = ARROW_PIECE_ID  
            grid[y+1][x] = ARROW_PIECE_ID  
            grid[y][x+1] = ARROW_PIECE_ID
            pieceCoordinates[ARROW_PIECE_ID] = [(x, y), (x, y+1), (x+1, y)]
        case 5:
            grid[y][x] = ARROW_PIECE_ID  
            grid[y][x-1] = ARROW_PIECE_ID  
            grid[y+1][x-1] = ARROW_PIECE_ID    
            pieceCoordinates[ARROW_PIECE_ID] = [(x, y), (x-1, y), (x-1, y+1)]
        case 6:
            grid[y][x] = ARROW_PIECE_ID  
            grid[y][x+1] = ARROW_PIECE_ID  
            grid[y+1][x+1] = ARROW_PIECE_ID
            pieceCoordinates[ARROW_PIECE_ID] = [(x, y), (x+1, y), (x+1, y+1)]
        case 7:
            grid[y][x] = ARROW_PIECE_ID  
            grid[y+1][x] = ARROW_PIECE_ID  
            grid[y][x-1] = ARROW_PIECE_ID 
            pieceCoordinates[ARROW_PIECE_ID] = [(x, y), (x, y+1), (x-1, y)]
        case 8:
            grid[y][x] = ARROW_PIECE_ID  
            grid[y-1][x] = ARROW_PIECE_ID  
            grid[y-1][x-1] = ARROW_PIECE_ID
            pieceCoordinates[ARROW_PIECE_ID] = [(x, y), (x, y-1), (x-1, y-1)]
        case 9:
            grid[y][x] = ARROW_PIECE_ID  
            grid[y][x+1] = ARROW_PIECE_ID  
            grid[y-1][x+1] = ARROW_PIECE_ID  
            pieceCoordinates[ARROW_PIECE_ID] = [(x, y), (x+1, y), (x+1, y-1)]  
        case 10:
            grid[y][x] = ARROW_PIECE_ID  
            grid[y-1][x] = ARROW_PIECE_ID  
            grid[y][x-1] = ARROW_PIECE_ID
            pieceCoordinates[ARROW_PIECE_ID] = [(x, y), (x, y-1), (x-1, y)]
        case 11:
            grid[y][x] = ARROW_PIECE_ID  
            grid[y+1][x] = ARROW_PIECE_ID  
            grid[y+1][x-1] = ARROW_PIECE_ID 
            pieceCoordinates[ARROW_PIECE_ID] = [(x, y), (x, y+1), (x-1, y+1)]
            
    return grid, pieceCoordinates

def isMoveValid(grid: list[list[int, int]], pieceID: int, x: int, y: int, config: int) -> bool:
    """ 
    Returns whether a given pieceID with a given config is able to be placed at a given coordinate on a given grid.
    
    Parameters:
    LIST<LIST<INT, INT>> grid
    INT pieceID : [0, 8]
    INT x : [0, 5]
    INT y : [0, 5]
    INT config
    
    Returns:
        BOOL
    """
    
    """ 
    Within the match statement, 'x' describes the origin square of a piece, while 'o' describes a non-origin part of the piece. 
    For example a three by one line: x o o
    """ 
    match pieceID:
        case 0: #Small Square
            return isMoveValidSmallSquare(grid, x, y)
        case 1: #Big Square
            return isMoveValidBigSquare(grid, x, y, config)
        case 2: #Short Bar
            return isMoveValidShortBar(grid, x, y, config)
        case 3: #Bar
            return isMoveValidBar(grid, x, y, config)
        case 4: #Long Bar
            return isMoveValidLongBar(grid, x, y, config) 
        case 5: #L
            return isMoveValidL(grid, x, y, config)   
        case 6: #T 
            return isMoveValidT(grid, x, y, config)    
        case 7: #Z
            return isMoveValidZ(grid, x, y, config)
        case 8: #Arrow
            return isMoveValidArrow(grid, x, y, config)

def placePieceOnGrid(grid: list[list[int, int]], pieceCoordinates: dict[int, tuple[int, int]], pieceID: int, x: int, y: int, config: int) -> list[list[list[int]], dict[int, tuple[int, int]]]: 
    """ 
    Updates the grid by setting the given piece onto the grid..
    Parameters are validated within functions calling placePieceOnGrid()
    
    Parameters:
    LIST<LIST<INT, INT>> grid
    DICT<INT, TUPLE<INT, INT>> pieceCoordinates
    INT pieceID : [0, 8]
    INT x : [0, 5]
    INT y : [0, 5]
    INT config
    
    Returns:
        TUPLE<LIST<LIST<INT, INT>> grid, DICT<INT, TUPLE<INT, INT>> pieceCoordinates>
    """    
    """
    Within the match statement, 'x' describes the origin square of a piece, while 'o' describes a non-origin part of the piece. 
    For example a three by one line: x o o
    """
    match pieceID:
        case 0: #Small Square
            grid, pieceCoordinates = placeSmallSquareOnGrid(grid, pieceCoordinates, x, y)
        case 1: #Big Square
            grid, pieceCoordinates = placeBigSquareOnGrid(grid, pieceCoordinates, x, y, config)
        case 2: #Short Bar
            grid, pieceCoordinates = placeShortBarOnGrid(grid, pieceCoordinates, x, y, config)
        case 3: #Bar
            grid, pieceCoordinates = placeBarOnGrid(grid, pieceCoordinates, x, y, config)
        case 4: #Long Bar
            grid, pieceCoordinates = placeLongBarOnGrid(grid, pieceCoordinates, x, y, config)       
        case 5: #L
            grid, pieceCoordinates = placeLOnGrid(grid, pieceCoordinates, x, y, config)
        case 6: #T 
            grid, pieceCoordinates = placeTOnGrid(grid, pieceCoordinates, x, y, config)
        case 7: #Z
            grid, pieceCoordinates = placeZOnGrid(grid, pieceCoordinates, x, y, config)  
        case 8: #Arrow 
            grid, pieceCoordinates = placeArrowOnGrid(grid, pieceCoordinates, x, y, config)

    return grid, pieceCoordinates

def removePieceFromGrid(grid: list[list[int, int]], pieceCoordinates: dict[int, tuple[int, int]], pieceID: int) -> list[list[int]]:
    """ 
    Updates the grid by removing the given piece from the grid.
    piece is validated within function calling removePieceFromGrid().
    
    Parameters:
    LIST<LIST<INT, INT>> grid
    DICT<INT, TUPLE<INT, INT>> pieceCoordinates
    INT pieceID : [0, 8]
    
    Returns:
        LIST<LIST<INT, INT>> grid
    """
    for coordinates in pieceCoordinates[pieceID]:
        grid[coordinates[1]][coordinates[0]] = EMPTY_ID
    return grid
                   
def printGrid(grid: list[list[int, int]]) -> None:
    """
    Prints the terminal representation of the 2D list representing the grid

    Parameters:
        None
        
    Returns:
        None
    """    
    for y in range(0, 6):
        for x in range(0, 6):
            if x == 5: #include escape character \n
                if grid[y][x] == BLOCKER_ID:
                    print("#") 
                elif grid[y][x] == EMPTY_ID:
                    print("~") 
                else:
                    print(grid[y][x]) 
            else:
                if grid[y][x] == BLOCKER_ID:
                    print("#", end=" ") 
                elif grid[y][x] == EMPTY_ID:
                    print("~", end=" ") 
                else:
                    print(grid[y][x], end=" ") 
    print("")          
    
def getEmptySquareCoordinates(grid: list[list[int, int]]) -> tuple[int]:
    """
    Searches the grid representation for an element with value of EMPTY_ID, if not found returns invalid coordinates

    Parameters:
        None
        
    Returns:
        TUPLE<INT>
    """   
    for y in range(0, len(grid)):
        for x in range(0, len(grid[0])):
            if grid[y][x] == EMPTY_ID:
                return (x, y)
    return (-1, -1)

def findSolution(grid: list[list[int, int]], pieceCoordinates: dict[int, tuple[int, int]], unusedPiecesID: list[int]) -> bool:
    """
    Uses a backtracking algorithm to search for a single solution on a given grid configuration

    Parameters:
    LIST<LIST<INT, INT>> grid
    DICT<INT, TUPLE<INT, INT>> pieceCoordinates
    LIST<INT> unusedPiecesID
        
    Returns:
        BOOL
    """     
    if len(unusedPiecesID) == 0:
        return True
    
    emptySquare = getEmptySquareCoordinates(grid)
    for pieceID in unusedPiecesID:
        for config in PIECE_CONFIGURATIONS[pieceID]:
            if isMoveValid(grid, pieceID, emptySquare[0], emptySquare[1], config):
                grid, pieceCoordinates = placePieceOnGrid(grid, pieceCoordinates, pieceID, emptySquare[0], emptySquare[1], config)
                unusedPiecesID.remove(pieceID)
                
                if findSolution(grid, pieceCoordinates, unusedPiecesID):
                    return True
                
                grid = removePieceFromGrid(grid, pieceCoordinates, pieceID)
                pieceCoordinates[pieceID] = None
                unusedPiecesID.insert(0, pieceID)
                unusedPiecesID.sort()

    return False