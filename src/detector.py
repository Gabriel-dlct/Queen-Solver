from PIL import Image
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np
import cv2 


#Keeping only the board.
def find_board(img):
    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    binary_inv = 255 - binary
    num_labels, _, stats, _ = cv2.connectedComponentsWithStats(binary_inv, connectivity=8)
    best = None
    max_area = 0
    for i in range(1, num_labels):
        x, y, w, h, area = stats[i]
        if area < 1000:
            continue
        ratio = w / h
        if 0.85 < ratio < 1.15 and area > max_area:
            max_area = area
            best = (x, y, w, h)
    if best:
        x, y, w, h = best
        squared_img = img[y:y+h, x:x+w]

    return squared_img, best

def detect_length_queen(q_games):
    gray = cv2.cvtColor(q_games, cv2.COLOR_RGB2GRAY)
    _, binary = cv2.threshold(gray, 40, 255, cv2.THRESH_BINARY)
    binary_inv = 255 - binary

    # plt.imshow(binary_inv)
    # plt.show()



    h_proj = binary_inv.sum(axis=1)
    def count_lines(proj, threshold_ratio=0.5):
        threshold = proj.max() * threshold_ratio
        above = proj > threshold          # True là où il y a une ligne
        # Détecte les transitions False→True (début d'une ligne)
        crossings = np.diff(above.astype(int))
        return (crossings == 1).sum()

    h_count = count_lines(h_proj)
    return h_count 

def get_cell_colors(q_games, length):
    q_games = q_games[:, :, :3] 
    h, w = q_games.shape[:2]
    cell_h = h / length
    cell_w = w / length

    colors = np.zeros((length, length, 3), dtype=np.uint8)

    for row in range(length):
        for col in range(length):
            cy = int((row + 0.5) * cell_h)
            cx = int((col + 0.5) * cell_w)
            colors[row, col] = q_games[cy, cx]

    return colors

def find_queen_game(img):
    #Keeping only the queen_game image
    q_games, dim = find_board(img)

    # plt.imshow(q_games)
    # plt.show()


    #Finding its length
    length  = detect_length_queen(q_games)


    #Find the colors
    tab = get_cell_colors(q_games, length)

    return tab, dim
