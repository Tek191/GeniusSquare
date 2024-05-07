""" 
Unit testing for the Genius Square Solver
"""

import unittest
import GeniusSquareSolver as ggs

""" 
Shorthand for grid element IDs to grid uniform by elements being one character long
"""
X = ggs.BLOCKER_ID
O = ggs.EMPTY_ID

""" 
Helper functions used to reduce code duplication.
Helper functions are independent of tested functions.
"""
def helperGetEmptyGrid():
    grid = [
            [O, O, O, O, O, O],
            [O, O, O, O, O, O],
            [O, O, O, O, O, O],
            [O, O, O, O, O, O],
            [O, O, O, O, O, O],
            [O, O, O, O, O, O]
        ] 
    return grid

def helperGetSingleBlockerGrid():
    grid = [
            [X, O, O, O, O, O],
            [O, O, O, O, O, O],
            [O, O, O, O, O, O],
            [O, O, O, O, O, O],
            [O, O, O, O, O, O],
            [O, O, O, O, O, O]
        ] 
    return grid

class TestGeniusSquareSolver(unittest.TestCase):
    def test_getDieFaceCoordinates(self):
        self.assertEqual(ggs.getDieFaceCoordinates("A4"), (3, 0)) #Standard Test Case
        self.assertEqual(ggs.getDieFaceCoordinates("A1"), (0, 0)) #Boundary Test Case
        self.assertEqual(ggs.getDieFaceCoordinates("F6"), (5, 5)) #Boundary Test Case
    
    def test_getDiceRolls(self):
        self.assertEqual(ggs.getDiceRolls("A1A2C3E1A4E4F1"), [(0, 0), (1, 0), (2, 2), (0, 4), (3, 0), (3, 4), (0, 5)]) #Standard Test Case
    
    def test_getDiceRolls(self):
        #Standard Test Case: No seed
        for i in range(0, 10):
            randomRoll = ggs.getDiceRolls()
            self.assertIsInstance(randomRoll, list)
            for pair in randomRoll:
                self.assertIsInstance(pair, tuple)
                self.assertIsInstance(pair[0], int)
                self.assertTrue(pair[0] >= 0 and pair[0] <= 5)
                self.assertIsInstance(pair[1], int)
                self.assertTrue(pair[1] >= 0 and pair[1] <= 5)
        
        #Standard Test Case: Set seed
        setSeedRoll = ggs.getDiceRolls("B1F1D2F2C3A4E6")
        expectedRoll = [(0, 1), (0, 5), (1, 3), (1, 5), (2, 2), (3, 0), (5, 4)]
        self.assertEqual(setSeedRoll, expectedRoll)
        
        #Erroneous Test Case: Seed is string but too short
        for i in range(0, 10):
            invalidSeedLengthRoll = ggs.getDiceRolls("B1F1")
            self.assertIsInstance(invalidSeedLengthRoll, list)
            for pair in invalidSeedLengthRoll:
                self.assertIsInstance(pair, tuple)
                self.assertIsInstance(pair[0], int)
                self.assertTrue(pair[0] >= 0 and pair[0] <= 5)
                self.assertIsInstance(pair[1], int)
                self.assertTrue(pair[1] >= 0 and pair[1] <= 5)        
        
        #Erroneous Test Case: Seed is string but wrong format
        for i in range(0, 10):
            invalidSeedFormatRoll = ggs.getDiceRolls("11111111111111")
            self.assertIsInstance(invalidSeedFormatRoll, list)
            for pair in invalidSeedFormatRoll:
                self.assertIsInstance(pair, tuple)
                self.assertIsInstance(pair[0], int)
                self.assertTrue(pair[0] >= 0 and pair[0] <= 5)
                self.assertIsInstance(pair[1], int)
                self.assertTrue(pair[1] >= 0 and pair[1] <= 5)   
        
        #Erroneous Test Case: Seed is not string
        for i in range(0, 10):
            invalidSeedTypeRoll = ggs.getDiceRolls(5)
            self.assertIsInstance(invalidSeedTypeRoll, list)
            for pair in invalidSeedTypeRoll:
                self.assertIsInstance(pair, tuple)
                self.assertIsInstance(pair[0], int)
                self.assertTrue(pair[0] >= 0 and pair[0] <= 5)
                self.assertIsInstance(pair[1], int)
                self.assertTrue(pair[1] >= 0 and pair[1] <= 5)           

    def test_intialiseBlockers(self):
        #Standard Test Case
        expectedGrid = [
            [X, X, O, O, O, O],
            [O, X, O, O, O, O],
            [O, O, X, O, O, O],
            [O, O, O, X, O, O],
            [O, O, O, O, X, O],
            [O, O, O, O, O, X]
        ]         
        grid = [
            [O, O, O, O, O, O],
            [O, O, O, O, O, O],
            [O, O, O, O, O, O],
            [O, O, O, O, O, O],
            [O, O, O, O, O, O],
            [O, O, O, O, O, O]
        ] 
        
        blockerCoordinates = [(0, 0), (1, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5)]
        grid = ggs.initaliseBlockers(grid, blockerCoordinates)
        self.assertEqual(grid, expectedGrid)
      
    def test_pieceValidationAndPlacement(self):
        #Standard Test Case
        try:
            for currentPiece in ggs.ALL_PIECE_IDS:
                for config in ggs.PIECE_CONFIGURATIONS[currentPiece]:
                    for yCord in range(0, 6):
                        for xCord in range(0, 6):
                            grid = ggs.deepcopy(ggs.EMPTY_GRID)                            
                            pieceCoordinates = ggs.deepcopy(ggs.DEFAULT_PIECE_COORDINATES)
                            
                            if ggs.isMoveValid(grid, currentPiece, xCord, yCord, config):
                                grid, pieceCoordinates = ggs.placePieceOnGrid(grid, pieceCoordinates, currentPiece, xCord, yCord, config)    
                                grid = ggs.removePieceFromGrid(grid, pieceCoordinates, currentPiece)
                                pieceCoordinates[currentPiece] = None
            test = True
        except Exception:
            test = False 
        
        self.assertEqual(test, True)
        
    def test_getEmptySquareCoordinates(self):
        #Standard Test Case
        grid = [
            [X, X, X, O, O, O],
            [O, O, O, O, O, O],
            [O, O, O, O, O, O],
            [O, O, O, O, O, O],
            [O, O, O, O, O, O],
            [O, O, O, O, O, O]
        ]     
        emptySquareCoordinates = ggs.getEmptySquareCoordinates(grid)   
        self.assertEqual(emptySquareCoordinates, (3, 0))
    
    def test_findSolution(self):
        #Standard Test Case
        existingSolutions = {}
        cycles = 0
        for a in ggs.DICE_ONE:
            for b in ggs.DICE_TWO:
                for c in ggs.DICE_THREE:
                    for d in ggs.DICE_FOUR:
                        for e in ggs.DICE_FIVE:
                            for f in ggs.DICE_SIX:
                                for j in ggs.DICE_SEVEN:  
                                    seed = a+b+c+d+e+f+j
                                    if seed in existingSolutions:
                                        continue
                                    cycles += 1
                                    grid = ggs.deepcopy(ggs.EMPTY_GRID)                            
                                    pieceCoordinates = ggs.deepcopy(ggs.DEFAULT_PIECE_COORDINATES)
                                    unusedPiecesID = ggs.deepcopy(ggs.ALL_PIECE_IDS)
                                    diceRoll = ggs.getDiceRolls(seed)
                                    grid = ggs.initaliseBlockers(grid, diceRoll)
                                    solution = ggs.findSolution(grid, pieceCoordinates, unusedPiecesID)
                                    if not solution:
                                        self.fail(f"Failed to solve {seed}")
                                    existingSolutions[seed] = solution
        self.assertTrue(True) 
    
if __name__ == '__main__':
    unittest.main()