from settings import *
from tetris import Tetris, Text
import sys
from AI import Search_AI
from json_functions import *

class App:
    def __init__(self, user=True, bag=True):
        pg.init()
        pg.display.set_caption('Tetris')
        self.screen = pg.display.set_mode(WIN_RES)
        self.clock = pg.time.Clock()
        self.set_timer()
        self.tetris = Tetris(self, bag=bag)
        self.text = Text(self)
        self.user = user


    def set_timer(self):
        self.user_event = pg.USEREVENT + 0
        self.fast_user_event = pg.USEREVENT + 1
        self.anim_trigger = False
        self.fast_anim_trigger = False
        pg.time.set_timer(self.user_event, ANIM_TIME_INTERVAL)
        pg.time.set_timer(self.fast_user_event, FAST_ANIM_TIME_INTERVAL)


    def update(self):
        tetris_update_return = self.tetris.update()
        self.clock.tick(FPS)
        return tetris_update_return

    def draw(self):
        self.screen.fill(color=BG_COLOR)
        self.screen.fill(color=FIELD_COLOR, rect=(0,0, *FIELD_RES))
        self.tetris.draw()
        self.text.draw()
        pg.display.flip()

    def check_events_user(self):
        self.anim_trigger = False
        self.fast_anim_trigger = False
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                pg.quit()
                sys.exit()
            elif event.type == pg.KEYDOWN:
                self.tetris.control(pressed_key=event.key)
            elif event.type == self.user_event:
                self.anim_trigger = True
            elif event.type == self.fast_user_event:
                self.fast_anim_trigger = True

    def check_events_search(self, move_sequence):
        self.anim_trigger = False
        self.fast_anim_trigger = False
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                pg.quit()
                sys.exit()
            elif event.type == self.user_event:
                self.anim_trigger = True
            elif event.type == self.fast_user_event:
                self.fast_anim_trigger = True


        # Simulate keypress when timer ticks
        if self.anim_trigger and move_sequence:
            this_move = move_sequence.pop(0)
            self.tetris.control(pressed_key=this_move)

    def run(self, scores_list):
        this_move_sequence = []
        first_AI_run = True
        while True:
            if self.user:
                self.check_events_user()
            else:
                if self.tetris.ai_trigger:
                    if not first_AI_run:
                        search_ai = Search_AI(self.tetris.field_array, self.tetris.tetrimino.shape)
                        search_ai.get_move()
                        this_move_sequence = search_ai.best_move_sequence
                    else:
                        first_AI_run = False
                self.check_events_search(this_move_sequence)
            if self.update() == "game ended":
                break
            self.draw()
        if scores_list is not None:
            scores_list.append(self.tetris.score)


def do_tetris(score_list=None):
    user_input = input("Who is playing? Enter 1 for user and anything else for AI: ")
    bag_input = input("Would you like the bag feature to be disabled? \n"
                      "Enter y to disable it and anything else to leave it enabled: ")
    user = False
    bag = True
    if user_input == '1':
        user = True
    if bag_input == 'y':
        bag = False
    app = App(user=user, bag=bag)
    print("Bag is on?",app.tetris.bag_on)
    app.run(score_list)
    return app.tetris.num_lines_cleared

if __name__ == '__main__':
   do_tetris()

