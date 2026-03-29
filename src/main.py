import mss
import numpy as np
import time
from solver.objects import Game
from detector import find_queen_game
from clicker import clicker


with mss.mss() as sct:
    start = time.time()
    screen = np.array(sct.grab(sct.monitors[1]))
    after_screen = time.time()
    print(f"Time for screen : {after_screen - start}")
    tab, dim = find_queen_game(screen)
    after_size = time.time()
    print(f"Time for resizing : {after_size - after_screen}")
    test = Game(size=len(tab))
    test.load_board_from_colors(tab)
    after_game = time.time()
    print(f"Time for loading_board : {after_game - after_size}")
    test.solve_board()
    queen_pos = test.queens_to_location()
    after_resol = time.time()
    print(f"Time for solving : {after_resol - after_game}")

    print(f"Time for all except clicking : {time.time() - start}")
    clicker(screen.shape[:2], dim, queen_pos)
    print(f"time for clicking : {time.time() - after_resol}")