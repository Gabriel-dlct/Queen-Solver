import mss
import numpy as np
import time
from solver.objects import Game
from detector import find_queen_game
from clicker import clicker
import matplotlib.pyplot as plt


with mss.mss() as sct:
    screen = np.array(sct.grab(sct.monitors[1]))
    tab, dim = find_queen_game(screen)
    test = Game(size=len(tab))
    test.load_board_from_colors(tab)

    test.check_colors()
    # before_resol = time.time()
    # test.solve_board()
    # print(f"Time for solving : {time.time() - before_resol}")

    test.show()