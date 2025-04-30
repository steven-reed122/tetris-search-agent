# future changes
# add feature to tetris where piece come from 'bag' of all seven piece that refills when empty
    # this will make all piece types more consistent

# penalize covering top level holes more

from sympy.series.limits import heuristics

from settings import *
from small_tetris import Small_Tetris

# heuristics // defines how the board state will compair with a goal board state after a specific move
# completed lines // the number of rows a potential next move would clear, maximize this
# aggregate height // the sum of the heights of every column, minimize this to a point
# holes // all empty spaces with at list one block above it, minimize this as much as possible
# bumpiness // the sum of the differences between all adjacent columns, minimize this to a point

class Heuristics:
    def __init__(self, field_array, pro=False):
        self.field_array = field_array
        self.completed_lines = 0

    def get_completed_lines(self):
        num_completed_lines = 0
        for row in self.field_array:
            if 0 not in row:
                num_completed_lines += 1
        return num_completed_lines

    def get_aggregate_height(self):
        """
        Computes the aggregate height of a Tetris board.
        Each column's height is the distance from the bottom to the highest filled cell.

        :param board: List of rows (top to bottom), where each row is a list of ints.
        :return: Sum of the heights of all columns.
        """
        aggregate_height = 0

        for col in range(len(self.field_array[0])):
            for row in range(len(self.field_array)):
                if self.field_array[row][col]:
                    height = len(self.field_array) - row
                    aggregate_height += height
                    break  # Found the topmost block in this column

        return aggregate_height

    def get_num_holes(self):
        """
        Computes the number of holes in the Tetris board.
        A hole is an empty cell with at least one filled cell above it in the same column.

        :param board: List of rows (top to bottom), where each row is a list of ints.
        :return: Integer count of holes.
        """
        if not self.field_array or not self.field_array[0]:
            return 0

        num_rows = len(self.field_array)
        num_cols = len(self.field_array[0])
        holes = 0

        for col in range(num_cols):
            block_found = False
            for row in range(num_rows):
                if self.field_array[row][col]:
                    block_found = True
                elif block_found:
                    holes += 1

        return holes

    def get_bumpiness(self):
        """
        Computes the bumpiness of the Tetris board.
        Bumpiness is the sum of absolute differences between adjacent column heights.

        :param board: List of rows (top to bottom), each row is a list of ints.
        :return: Integer bumpiness value.
        """
        if not self.field_array or not self.field_array[0]:
            return 0

        num_rows = len(self.field_array)
        num_cols = len(self.field_array[0])
        heights = []

        for col in range(num_cols):
            for row in range(num_rows):
                if self.field_array[row][col]:
                    heights.append(num_rows - row)
                    break
            else:
                heights.append(0)  # No block in this column

        bumpiness = sum(abs(heights[i] - heights[i + 1]) for i in range(num_cols - 1))
        return bumpiness

    # multiply the heuristics together in an "optimal" way, this will be iterated over time
    # current strategy is
    # completed lines to the fourth power to bias for completing more lines is better (1, 16, 81, 256)
    # aggregate height gets penalized after 40 (4 completed rows) but good before then
    # holes always get sharply penalized
    # bumpiness gets penalized after some value (starting with 15)
    def calculate_move_quality(self):
        completed_lines_component = self.get_completed_lines() ** 4 + self.get_completed_lines() * 10
        aggregate_height_component = self.get_aggregate_height() * -2
        num_holes_component = self.get_num_holes() * -40
        bumpiness_component = self.get_bumpiness() * -5
        quality_value = (completed_lines_component + aggregate_height_component
                         + num_holes_component + bumpiness_component)
        return quality_value

class Search_AI:
    def __init__(self, field_array, piece):
        self.tetris = Small_Tetris(field_array, piece)
        self.tetris.set_piece_pos_start()
        self.piece_name = piece
        self.possible_next_board_states = []
        self.possible_next_board_states_moves_list = []
        self.quality_list = None
        self.best_move = None
        self.best_move_sequence = None

    def move_piece_all_the_way(self, direction):
        count = 0
        while True:
            count += 1
            if not self.tetris.move_piece(direction):
                break
        return count

    def num_rotations(self):
        rotations = 4
        if self.piece_name == 'O':
            rotations = 1
        elif self.piece_name in ('I', 'S', 'Z'):
            rotations = 2
        return rotations

    def make_and_append_states_list(self, count_rotations, count_left, count_down):
        moves_list = []
        for i in range(count_rotations):
            moves_list.append(pg.K_UP)
        for i in range(abs(count_left)):
            if count_left > 0:
                moves_list.append(pg.K_LEFT)
            else:
                moves_list.append(pg.K_RIGHT)
        for i in range(count_down):
            moves_list.append(pg.K_DOWN)
        self.possible_next_board_states_moves_list.append(moves_list)
        return moves_list

    # now we need a way to get all possible next moves
    def get_possible_next_board_states(self):
        current_board_state = self.tetris.field_array
        self.possible_next_board_states = []
        rotations  = self.num_rotations()
        for rotation in range(rotations):
            # put current piece all the way left and capture how many times we moved it
            count_left = self.move_piece_all_the_way('left')
            # drop piece
            count_down = self.move_piece_all_the_way('down')
            # add tetrimino blocks to array
            new_array = self.tetris.calc_new_field()
            # add this board state to list
            self.possible_next_board_states.append(new_array)
            # make moves list and add it to list
            self.make_and_append_states_list(rotation, count_left, count_down)
            # loop
            while True:
                # reset board state
                self.tetris.field_array = current_board_state
                # move piece back to top
                self.tetris.set_piece_pos((self.tetris.current_piece[0][0], 0))
                # move piece one right
                # if any block in tetrimino out is of bounds
                    # break
                count_left -= 1
                if not self.tetris.move_piece('right'):
                    break
                # drop piece
                self.tetris.drop_piece()
                # add tetrimino blocks to array
                new_array = self.tetris.calc_new_field()
                # add this board state to list
                self.possible_next_board_states.append(new_array)
                # create move list and append move list to all moves list
                self.make_and_append_states_list(rotation, count_left, count_down)
            # reset board state
            self.tetris.field_array = current_board_state
            # move piece back to starting position which is one left of starting pos
            self.tetris.set_piece_pos_start()
            # rotate piece
            self.tetris.rotate()
        return self.possible_next_board_states

    # function for getting the heuristic value (quality) of possible next board states
    def get_next_moves_qualities(self):
        self.quality_list = [0] * len(self.possible_next_board_states)
        for i, next_board_state in enumerate(self.possible_next_board_states):
            these_heuristics = Heuristics(next_board_state)
            quality_value = these_heuristics.calculate_move_quality()
            # add that value to the quality list
            self.quality_list[i] = quality_value

    def get_best_next_move_sequence(self):
        self.best_move = max(self.quality_list)
        best_move_index = self.quality_list.index(self.best_move)
        self.best_move_sequence = self.possible_next_board_states_moves_list[best_move_index]


    def get_move(self):
        self.get_possible_next_board_states()
        self.get_next_moves_qualities()
        self.get_best_next_move_sequence()


# helper method to print field arrays in a readable format
def print_field_array(field_array):
    new_array = []
    for row in field_array:
        print(row)
    print()