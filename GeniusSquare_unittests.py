""" 
Unit testing for the Genius Square GUI
"""

import unittest
import GeniusSquareSolver as ggs
import GeniusSquare as gsGUI

class TestGeniusSquare(unittest.TestCase):
    def test_isSeedValid(self):
        #Standard Test Case
        self.assertEqual(gsGUI.isSeedValid("A1A2C3E1A4E4F1"), True)
        #Standard Test Case
        self.assertEqual(gsGUI.isSeedValid("A1A2"), False)

    def test_getValidDieFaces(self):
        #Standard Test Case
        self.assertEqual(gsGUI.getValidDieFaces("F3B3D3B6A4F4F1"), [(True, 5), (True, 5), (True, 1), (True, 3), (True, 0), (True, 1), (True, 0)])     
        #Standard Test Case
        self.assertEqual(gsGUI.getValidDieFaces("a"), [(False, 0), (False, 0), (False, 0), (False, 0), (False, 0), (False, 0), (False, 0)])     

    def test_updatePieceRotation(self):
        #Standard Test Case
        self.assertEqual(gsGUI.updatePieceRotation(5, 4), 9)
        #Standard Test Case
        self.assertEqual(gsGUI.updatePieceRotation(0, 0), 0)
        
    def test_updatePieceReflection(self):
        #Standard Test Case
        self.assertEqual(gsGUI.updatePieceReflection(6, 4), 14)
        #Standard Test Case
        self.assertEqual(gsGUI.updatePieceReflection(7, 9), 13)
        
    def test_updatePieceOrientation(self):
        #Standard Test Case
        testPiece = ggs.deepcopy(gsGUI.DEFAULT_PLAYER_PIECES[ggs.L_PIECE_ID])
        testPiece["config"] = gsGUI.updatePieceOrientation(testPiece, True, True)
        self.assertEqual(testPiece["config"], 20)

    def test_convertSeedIntoString(self):
        self.assertEqual(gsGUI.convertSeedIntoString([(2, 5), (2, 1), (2, 2), (5, 1), (5, 2), (4, 3), (0, 5)]), "F3B3C3B6C6D5F1")

if __name__ == '__main__':
    unittest.main()