""" there's fire where you are going """

import curses
import random
import time
from concurrent.futures import ThreadPoolExecutor


class TamarindTuiApp:
    """ todo: idk i guess like a bruce springsteen quote or something """

    def __init__(self, logger):
        self.logger = logger
        self.running = True
        self.logger.info('started')
        self.player_icon = '💔'
        self.player_x = None
        self.player_y = None
        self.attack_icon = '🔥'
        self.snow_icon = '❄️'
        self.game_map = []
        self.thread_queue = ThreadPoolExecutor(max_workers=99)
        self.score = 0
        self.instructions = "Tamarind 🚒 " + \
            "Press w,a,s,d to move 🚒 " + \
            "Press q to quit 🚒 Space to attack 🚒 "

    def run(self):
        """ Sets up the game main loop to run in a curses wrapper """
        while self.running:
            self.logger.info('running')
            curses.wrapper(self.game)
            curses.endwin()
            self.running = False
            self.logger.info('stopped')

    def init_game_map(self):
        """ Called once at the start of the game """
        # initialize game map
        for i in range(curses.LINES):
            self.game_map.append([])
            for _ in range(curses.COLS):
                self.game_map[i].append(' ')

        # draw player
        self.player_x = curses.COLS // 2
        self.player_y = curses.LINES // 2
        self.game_map[self.player_y][self.player_x] = self.player_icon


    def game(self, stdscr):
        """ Main game loop """
        self.init_game_map()
        self.thread_queue.submit(self.snow, self.game_map)

        while True:
            for i in range(curses.LINES-1):
                for j in range(curses.COLS-1):
                    # if self.game_map[i][j] == ' ':
                    #     log_char = '|'
                    # self.logger.info(f'drawing: {j} {i} {log_char}')
                    stdscr.addstr(i, j, self.game_map[i][j])

            stdscr.addstr(0, 0, self.instructions + f'Score: {self.score} million')
            stdscr.refresh()
            # get keys non-blocking
            stdscr.nodelay(True)
            k = None
            try:
                k = stdscr.getkey()
                if k == 'q':
                    pass
                    # break
                else:
                    self.process_key(k)
            except curses.error:
                pass

    def snow(self, game_map):
        """ display snowflakes randomly """
        while self.running:
            x = random.randint(1, curses.COLS - 1)
            y = random.randint(1, curses.LINES - 1)
            game_map[y][x] = self.snow_icon
            time.sleep(0.1)

    def process_key(self, k):
        """ Processes the key pressed. If space, call child function to submit fire threads """
        self.logger.info('key: %s', k)
        if k == 'w':
            if self.player_y == 0:
                return
            self.logger.info(
                    f'up ({self.player_y}, {self.player_x}' + \
                            '-> {self.player_y-1}, {self.player_x})')
            if self.game_map[self.player_y-1][self.player_x] == self.snow_icon:
                self.score += 1
            self.game_map[self.player_y][self.player_x] = ' '
            self.player_y -= 1
            self.game_map[self.player_y][self.player_x] = self.player_icon
        elif k == 'a':
            if self.player_x == 0:
                return
            self.logger.info(
                    f'left ({self.player_y}, {self.player_x}' + \
                            '-> {self.player_y}, {self.player_x-1})')
            if self.game_map[self.player_y][self.player_x-1] == self.snow_icon:
                self.score += 1
            self.game_map[self.player_y][self.player_x] = ' '
            self.player_x -= 1
            self.game_map[self.player_y][self.player_x] = self.player_icon
        elif k == 's':
            if self.player_y == curses.LINES - 2:
                return
            self.logger.info(
                    f'down ({self.player_y}, {self.player_x}' + \
                            '-> {self.player_y+1}, {self.player_x})')
            if self.game_map[self.player_y+1][self.player_x] == self.snow_icon:
                self.score += 1
            self.game_map[self.player_y][self.player_x] = ' '
            self.player_y += 1
            self.game_map[self.player_y][self.player_x] = self.player_icon
        elif k == 'd':
            if self.player_x == curses.COLS - 1:
                return
            self.logger.info(
                    f'right ({self.player_y}, {self.player_x}' + \
                            '-> {self.player_y}, {self.player_x+1})')
            if self.game_map[self.player_y][self.player_x+1] == self.snow_icon:
                self.score += 1
            self.game_map[self.player_y][self.player_x] = ' '
            self.player_x += 1
            self.game_map[self.player_y][self.player_x] = self.player_icon
        elif k == ' ':
            self.logger.info('space')
            self.fire(self.game_map, self.player_x, self.player_y)
        else:
            self.logger.info('unknown key: %s', k)

    def fire(self, game_map, x, y):
        """ Submit threads to fire at the snowflakes """
        # clear column above player
        self.thread_queue.submit(self.fire_column, game_map, x, y-1, 1)
        # clear column below player
        self.thread_queue.submit(self.fire_column, game_map, x, y+1, len(game_map)-1)
        # clear row left of player
        self.thread_queue.submit(self.fire_row, game_map, y, x-1, 0)
        # clear row right of player
        self.thread_queue.submit(self.fire_row, game_map, y, x+1, len(game_map[0])-1)

    def fire_column(self, game_map, x, start_y, end_y):
        """ Fire vertically in column x from start_y to end_y """
        self.logger.info('fire_column: %s %s %s', x, start_y, end_y)
        for i in range(start_y, end_y, -1 if start_y>end_y else 1):
            self.logger.info(f'fire column {start_y}: {i} {x}')
            if game_map[i][x] == self.snow_icon:
                self.score += 1
            game_map[i][x] = self.attack_icon
            time.sleep(0.1)
            game_map[i][x] = ' '

    def fire_row(self, game_map, y, start_x, end_x):
        """ Fire horizontally in row y from start_x to end_x """
        self.logger.info('fire_row: %s %s %s', y, start_x, end_x)
        for i in range(start_x, end_x, -1 if start_x>end_x else 1):
            self.logger.info(f'fire row {start_x}: {y} {i}')
            if game_map[y][i] == self.snow_icon:
                self.score += 1
            game_map[y][i] = self.attack_icon
            time.sleep(0.1)
            game_map[y][i] = ' '
