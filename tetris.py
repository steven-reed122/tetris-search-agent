from settings import *
import math
import random
from tetrimino import Tetrimino, Block
import pygame.freetype as ft

class Text:
    def __init__(self, app):
        self.app = app
        self.font = ft.Font(FONT_PATH)

    def draw(self):
        self.font.render_to(self.app.screen, (WIN_W * 0.595, WIN_H * 0.02),
                            text='TETRIS', fgcolor='white',
                            size=TILE_SIZE * 1.65, bgcolor = 'black')
        self.font.render_to(self.app.screen, (WIN_W * 0.65, WIN_H * 0.22),
                            text='next', fgcolor='orange',
                            size=TILE_SIZE * 1.4, bgcolor = 'black')
        self.font.render_to(self.app.screen,(WIN_W * 0.64, WIN_H * 0.67),
                            text='score', fgcolor='orange',
                            size=TILE_SIZE * 1.4, bgcolor = 'black')
        self.font.render_to(self.app.screen, (WIN_W * 0.64, WIN_H * 0.8),
                            text=f'{self.app.tetris.score}', fgcolor='white',
                            size=TILE_SIZE * 1.8)

class Tetris:
    def __init__(self, app, field_array=None, tetrimino=None, bag=False):
        self.bag_on = bag
        self.app = app
        self.sprite_group = pg.sprite.Group()
        if field_array is None:
            self.field_array = self.get_field_array()
        else:
            self.field_array = field_array


        self.bag = []
        self.tetrimino = Tetrimino(self)
        self.next_tetrimino = Tetrimino(self, current=False)

        self.speed_up = False

        self.score = 0
        self.full_lines = 0
        self.points_per_line = {0: 0, 1: 100, 2: 300, 3: 700, 4:1500}

        self.ai_trigger = True
        self.ai_trigger_flipped_once = False

        self.num_lines_cleared = 0


    def get_score(self):
        self.score += self.points_per_line[self.full_lines]
        self.full_lines = 0

    def check_full_lines(self):
        row = FIELD_H - 1
        for y in range(FIELD_H - 1, -1, -1):
            for x in range(FIELD_W):
                self.field_array[row][x] = self.field_array[y][x]

                if self.field_array[y][x]:
                    self.field_array[row][x].pos = vec(x,y)

            if sum(map(bool, self.field_array[y])) < FIELD_W:
                row -= 1
            else:
                for x in range(FIELD_W):
                    self.field_array[row][x].alive =  False
                    self.field_array[row][x] = 0

                self.full_lines += 1
                self.num_lines_cleared += 1

    def put_tetrimino_blocks_in_array(self):
        for block in self.tetrimino.blocks:
            x,y = int(block.pos.x), int(block.pos.y)
            self.field_array[y][x] = block

    def calc_new_field_array(self):
        field_array_copy = [row[:] for row in self.field_array]
        for block in field_array_copy:
            x,y = int(block.pos.x), int(block.pos.y)
            field_array_copy[y][x] = block

    def get_field_array(self):
        return [[0 for x in range(FIELD_W)] for y in range(FIELD_H)]

    def is_game_over(self):
        if self.tetrimino.blocks[0].pos.y == INIT_POS_OFFSET[1]:
            pg.time.wait(300)
            return True

    def check_tetrimino_landing(self):
        if self.tetrimino.landing:
            if self.is_game_over():
                return "game ended"
            else:
                self.speed_up = False
                self.put_tetrimino_blocks_in_array()
                self.next_tetrimino.current = True
                self.tetrimino = self.next_tetrimino
                if self.bag_on:
                    if not self.bag:
                        self.bag = [key for key in list(TETRIMINOES.keys())]
                    choice = random.choice(self.bag)
                    self.bag.remove(choice)
                    self.next_tetrimino = Tetrimino(self, shape=choice, current=False)
                else:
                    self.next_tetrimino = Tetrimino(self, current=False)
                self.trigger_AI()

    def trigger_AI(self):
        self.ai_trigger = True

    def control(self, pressed_key):
        if pressed_key == pg.K_LEFT:
            self.tetrimino.move(direction='left')
        elif pressed_key == pg.K_RIGHT:
            self.tetrimino.move(direction='right')
        elif pressed_key == pg.K_UP:
            self.tetrimino.rotate()
        elif pressed_key == pg.K_DOWN:
            self.speed_up = True

    def draw_grid(self):
        for x in range(FIELD_W):
            for y in range(FIELD_H):
                pg.draw.rect(self.app.screen, 'black',
                             (x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE), 1)
    def update(self):
        tetrimino_landing_return = None
        trigger = [self.app.anim_trigger, self.app.fast_anim_trigger][self.speed_up]
        if self.ai_trigger_flipped_once:
            self.ai_trigger = False
        else:
            self.ai_trigger_flipped_once = True
        if trigger:
            self.check_full_lines()
            self.tetrimino.update()
            tetrimino_landing_return = self.check_tetrimino_landing()
            self.get_score()
        self.sprite_group.update()
        return tetrimino_landing_return

    def draw(self):
        self.draw_grid()
        self.sprite_group.draw(self.app.screen)