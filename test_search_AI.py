import unittest

from sympy.series.limits import heuristics

from settings import *
from AI import Search_AI, print_field_array
from small_tetris import Small_Tetris
from AI import Heuristics


class TestHeuristics(unittest.TestCase):
    def setUp(self):
        self.field_array = [[0] * 10 for _ in range(20)]  # 20x10 field

    def test_get_completed_lines(self):
        self.field_array[19] = [1,1,1,1,1,1,1,1,1,1]
        self.field_array[18] = [1,1,1,1,1,1,0,1,1,1]
        self.field_array[17] = [1,1,1,1,1,1,1,1,1,1]
        self.field_array[16] = [1,1,0,1,1,1,1,1,1,0]
        self.field_array[15] = [1,1,1,1,1,1,1,1,1,1]
        these_heuristics = Heuristics(self.field_array)
        self.assertEqual(3, these_heuristics.get_completed_lines())

    def test_get_aggregate_height(self):
        self.field_array[15] = [0, 1, 0, 1, 1, 1, 0, 1, 1, 0]
        self.field_array[16] = [1, 1, 0, 1, 1, 1, 0, 1, 1, 0]
        self.field_array[17] = [1, 1, 1, 0, 1, 1, 0, 1, 1, 0]
        self.field_array[18] = [1, 0, 1, 1, 1, 1, 0, 1, 1, 1]
        self.field_array[19] = [1, 1, 1, 1, 1, 1, 0, 1, 1, 1]
        these_heuristics = Heuristics(self.field_array)
        self.assertEqual(39, these_heuristics.get_aggregate_height())

    def test_get_num_holes(self):
        self.field_array[15] = [0, 1, 0, 1, 1, 1, 1, 1, 1, 0]
        self.field_array[16] = [1, 1, 0, 1, 1, 1, 0, 1, 0, 0]
        self.field_array[17] = [0, 1, 1, 0, 1, 1, 0, 1, 0, 0]
        self.field_array[18] = [1, 0, 1, 1, 1, 1, 0, 1, 1, 1]
        self.field_array[19] = [1, 1, 0, 1, 1, 1, 0, 1, 1, 1]
        these_heuristics = Heuristics(self.field_array)
        self.assertEqual(14, these_heuristics.get_num_holes())

    def test_get_bumpiness(self):
        self.field_array[15] = [0, 1, 0, 1, 0, 1, 1, 1, 1, 0]
        self.field_array[16] = [1, 1, 0, 1, 1, 1, 0, 1, 1, 0]
        self.field_array[17] = [0, 1, 1, 0, 1, 1, 0, 1, 0, 0]
        self.field_array[18] = [1, 0, 1, 1, 1, 1, 0, 1, 1, 1]
        self.field_array[19] = [1, 1, 1, 1, 1, 1, 0, 1, 1, 1]
        these_heuristics = Heuristics(self.field_array)
        self.assertEqual(10, these_heuristics.get_bumpiness())

class TestSearch_AI(unittest.TestCase):
    def setUp(self):
        self.field_array = [[0] * 10 for _ in range(20)]

    def test_get_possible_next_board_states(self):
        this_search_ai = Search_AI(self.field_array, 'I')
        this_search_ai.get_possible_next_board_states()
        for field_array in this_search_ai.possible_next_board_states:
            print_field_array(field_array)

    def test_get_next_moves_qualities(self):
        this_search_ai = Search_AI(self.field_array, 'I')
        this_search_ai.get_possible_next_board_states()
        this_search_ai.get_next_moves_qualities()

    def test_best_next_move_sequence(self):
        this_search_ai = Search_AI(self.field_array, 'I')
        this_search_ai.get_possible_next_board_states()
        this_search_ai.get_next_moves_qualities()
        this_search_ai.get_best_next_move_sequence()
        print()
        print(this_search_ai.best_move_sequence)

    def test_get_move(self):
        this_search_ai = Search_AI(self.field_array, 'I')
        this_search_ai.get_move()
        print()
        print(this_search_ai.best_move_sequence)



