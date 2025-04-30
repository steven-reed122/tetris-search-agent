from settings import *

# class to simulate a couple feature of tetris for use in the model
class Small_Tetris:
    def __init__(self, field_array, piece_type):
        self.field_array = field_array
        self.current_piece = TETRIMINOES[piece_type]

    def rotate_block(self, pos, pivot_pos):
        translated = vec(pos) - vec(pivot_pos)
        rotated = translated.rotate(90)
        rotated = vec(round(rotated.x), round(rotated.y))
        return rotated + pivot_pos

    def rotate(self):
        pivot_pos = self.current_piece[0]
        self.current_piece = [
            self.rotate_block(part, pivot_pos)
            for part in self.current_piece
        ]

    def set_piece_pos(self, pos):
        center_x, center_y = self.current_piece[0]
        dx = pos[0] - center_x
        dy = pos[1] - center_y
        self.current_piece = [(x + dx, y + dy) for (x, y) in self.current_piece]

    def set_piece_pos_start(self):
        self.set_piece_pos(INIT_POS_OFFSET)
        self.move_piece("left")

    def move_piece(self, direction):
        """
           Moves the current piece left or right by 1 unit, if within bounds.
           Direction should be either 'left' or 'right'.
           Returns True if move is successful, False otherwise.
           """
        if direction not in ("left", "right", "down", "up"):
            raise ValueError("Direction must be 'left' or 'right' or 'down'.")

        dx = 0
        dy = 0
        if direction == "left":
            dx = -1
        elif direction == "right":
            dx = 1
        elif direction == "down":
            dy = 1
        elif direction == "up":
            dy = -1
        new_piece = [(x + dx, y + dy) for (x, y) in self.current_piece]

        # Check bounds (x must be within field width)
        for x, y in new_piece:
            if x < 0 or x >= len(self.field_array[0]):
                return False  # Out of horizontal bounds

        if self._collides(new_piece):
            return False

        self.current_piece = new_piece
        return True

    def drop_piece(self):
        """
        Simulates dropping the current piece straight down until it lands.
        Returns the landed piece position (list of coordinates).
        """
        piece = self.current_piece
        max_y_shift = 0

        while True:
            # Try moving piece down by 1
            shifted = [(x, y + max_y_shift + 1) for (x, y) in piece]
            if self._collides(shifted):
                break
            max_y_shift += 1

        # Return the piece in final landed position
        self.current_piece = [(x, y + max_y_shift) for (x, y) in piece]
        return self.current_piece

    def _collides(self, piece_coords):
        """
        Returns True if any part of the piece is out of bounds or overlaps the field.
        """
        new_piece_coords = [(int(x),int(y)) for x,y in piece_coords.copy()]
        for x, y in new_piece_coords:
            if y >= len(self.field_array) or x < 0 or x >= len(self.field_array[0]):
                return True  # Out of bounds
            if y >= 0 and self.field_array[y][x] != 0:
                return True  # Collision with existing block
        return False

    def calc_new_field(self):
        result = [row[:] for row in self.field_array]
        for point in self.current_piece:
            point = vec(point)
            if result[int(point.y)][int(point.x)] != 0:
                return result
            else:
                result[int(point.y)][int(point.x)] = 1
        return result

    def add_to_field(self, new_field):
        self.field_array= new_field

    def print_board(self):
        for row in self.field_array:
            print(row)