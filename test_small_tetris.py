from sympy.physics.units import current

from small_tetris import Small_Tetris
import unittest
from settings import *

class TestSmallTetris(unittest.TestCase):

    def setUp(self):
        self.empty_field = [[0] * 10 for _ in range(20)]  # 20x10 field

    def test_rotation_all_pieces(self):
        expected_rotations = {
            'T': [(0, 0), (0, -1), (0, 1), (1, 0)],
            'O': [(0, 0), (1, 0), (0, 1), (1, 1)],
            'J': [(0, 0), (0, -1), (1, 0), (2, 0)],
            'L': [(0, 0), (0, 1), (1, 0), (2, 0)],
            'I': [(0, 0), (-1, 0), (1, 0), (2, 0)],
            'S': [(0, 0), (0, -1), (1, 0), (1, 1)],
            'Z': [(0, 0), (0, 1), (1, 0), (1, -1)],
        }

        for piece_type, expected in expected_rotations.items():
            with self.subTest(piece=piece_type):
                game = Small_Tetris(self.empty_field, piece_type)
                game.rotate()
                rotated = game.current_piece
                for i, vector in enumerate(expected_rotations[piece_type]):
                    expected_rotations[piece_type][i] = vec(vector)
                self.assertEqual(expected, rotated)

    def test_set_piece_pos(self):
        expected_locations = {
            'T': [(4,10), (3,10), (5,10), (4,9)],
            'O': [(4,10), (4,9), (5,10), (5,9)],  # O does not change on rotation
            'J': [(4, 10), (3, 10), (4, 9), (4, 8)],
            'L': [(4, 10), (5, 10), (4, 9), (4, 8)],
            'I': [(4, 10), (4, 11), (4, 9), (4, 8)],
            'S': [(4, 10), (3, 10), (4, 9), (5, 9)],
            'Z': [(4, 10), (5, 10), (4, 9), (3, 9)],
        }

        for piece_type, expected in expected_locations.items():
            with self.subTest(piece=piece_type):
                game = Small_Tetris(self.empty_field, piece_type)
                game.set_piece_pos((4,10))
                moved = game.current_piece
                self.assertEqual(expected, moved)

    def test_move_left_within_bounds(self):
        game = Small_Tetris(self.empty_field, 'I')
        game.set_piece_pos((5,0))
        success = game.move_piece('left')
        self.assertTrue(success)
        self.assertTrue(game.current_piece == [(4,0), (4,1), (4,-1), (4,-2)])

    def test_move_right_within_bounds(self):
        game = Small_Tetris(self.empty_field, 'I')
        game.set_piece_pos((5,0))
        success = game.move_piece('right')
        self.assertTrue(success)
        self.assertTrue(game.current_piece == [(6,0), (6,1), (6,-1), (6,-2)])

    def test_move_down_within_bounds(self):
        game = Small_Tetris(self.empty_field, 'I')
        game.set_piece_pos((5,0))
        success = game.move_piece('down')
        self.assertTrue(success)
        self.assertTrue(game.current_piece == [(5,1), (5,2), (5,0), (5,-1)])

    def test_move_right_out_of_bounds(self):
        game = Small_Tetris(self.empty_field, 'I')
        # set piece on edge of board
        game.set_piece_pos((19,0))
        success = game.move_piece('right')
        self.assertFalse(success)
        self.assertTrue(game.current_piece == [(19,0), (19,1), (19,-1), (19,-2)])

    def test_drop_piece_on_empty_field(self):
        game = Small_Tetris(self.empty_field, 'I')
        landed = game.drop_piece()
        self.assertTrue(all(y >= 0 for _, y in landed))
        self.assertTrue(landed == [(0, 18), (0, 19), (0, 17), (0, 16)])  # All at bottom
        self.assertTrue(game.current_piece == [(0,18), (0,19), (0,17), (0,16)])

    def test_collision_detection(self):
        field = [[0]*10 for _ in range(19)] + [[1]*10]
        game = Small_Tetris(field, 'I')
        landed = game.drop_piece()
        self.assertTrue(landed == [(0,17),(0,18),(0,16),(0,15),])  # Should land right before bottom
        self.assertTrue(game.current_piece == [(0,17),(0,18),(0,16),(0,15),])

    def test_add_to_field_no_overlap(self):
        game = Small_Tetris(self.empty_field, 'O')
        game.drop_piece()
        result = game.calc_new_field()
        # Check that the piece was added to the field
        self.assertTrue(result == [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [1, 1, 0, 0, 0, 0, 0, 0, 0, 0], [1, 1, 0, 0, 0, 0, 0, 0, 0, 0]])


    def test_add_to_field_with_overlap_raises(self):
        field = [[0]*10 for _ in range(19)] + [[1]*10]
        game = Small_Tetris(field, 'O')
        game.set_piece_pos((0,19))  # Force overlap
        self.assertTrue(game.calc_new_field() is None)
        self.assertTrue(game.field_array == field)

if __name__ == '__main__':
    unittest.main()
