"""Create the Queen game."""

import secrets
from enum import Enum
import cv2

import matplotlib.pyplot as plt
import numpy as np

WHITE = [1.0, 1.0, 1.0]

colors = [
    [1.0, 0.0, 0.0],
    [0.0, 1.0, 0.0],
    [0.0, 0.0, 1.0],
    [1.0, 1.0, 0.0],
    [0.0, 1.0, 1.0],
    [1.0, 0.0, 1.0],
    [0.5, 0.5, 0.5],
    [1.0, 0.5, 0.0],
    [0.5, 0.0, 0.5],
    [0.0, 0.5, 0.5],
    [0.5, 0.5, 0.0],
    [0.8, 0.4, 0.0],
    [0.3, 0.6, 0.0],
    [0.0, 0.6, 0.3],
    [0.6, 0.0, 0.3],
    [0.3, 0.0, 0.6],
    [0.6, 0.3, 0.0],
    [0.0, 0.3, 0.6],
    [0.2, 0.7, 0.5],
    [0.7, 0.2, 0.5],
]




class State(Enum):
    """Define the state of a square.

    Args:
        Enum : only 3 states possible.

    """

    UNKNOWN: int = 0
    EMPTY: int = 1
    QUEEN: int = 2


class Square:
    """Define a square of the board."""

    def __init__(self, color: list[int] = WHITE, state: State = State.UNKNOWN) -> None:
        """Define a square.

        Args:
            color (list[int], optional): _Color of the square. White by default.
            state (State, optional): _description_. State of the square.

        """
        self.color = color
        self.state = state


class Game:
    """Generate a solvable queen board."""

    def __init__(self, size: int) -> None:
        """Initialize the game."""
        self.size = size
        self.board = [[Square() for _ in range(size)] for _ in range(size)]
        self.colors = {}

    # Usable functions

    def show(self) -> None:
        """Plot the instance of the game."""
        mat = np.ones((self.size, self.size, 3))
        _, ax = plt.subplots()

        for i in range(self.size):
            for j in range(self.size):
                mat[i][j] = self.board[i][j].color
                if self.board[i][j].state == State.QUEEN:
                    ax.scatter(i, j, marker="X", color="black", s=200, linewidths=2)

                if self.board[i][j].state == State.EMPTY:
                    ax.scatter(i, j, marker="x", color="grey", s=50, linewidths=1)

        ax.imshow(mat)
        ax.set_xticks(np.arange(-0.5, self.size, 1), minor=True)
        ax.set_yticks(np.arange(-0.5, self.size, 1), minor=True)
        ax.grid(which="minor", color="black", linewidth=2)
        ax.set_xticks([])
        ax.set_yticks([])

        plt.show()

    def update_queen(self, position: tuple[int, int]) -> None:
        """Add correctly a queen to the board.

        Args:
            position (tuple[int, int]): _position of the desired queen.

        """
        i, j = position
        self._add_queen(position=position)
        for x in range(self.size):
            if x != i:
                self._add_empty((x, j))
        for y in range(self.size):
            if y != j:
                self._add_empty((i, y))

        for i, j in self._get_neighbors(position):
            self._add_empty((i, j))

    def create_colored_rd_board(self) -> None:
        """Generate a solvable queen board."""
        position = self._rd_correct_position()
        key = secrets.SystemRandom().sample(range(len(colors)), self.size)
        chosen_colors = [colors[i] for i in key]
        for i, j in enumerate(position):
            self.board[i][j].color = chosen_colors[i]

        while not self._iscolored():
            neighbors = self._get_uncolored_neighbors()
            if not neighbors:
                break
            ni, nj = neighbors[0]
            deltas = [(0, -1), (0, 1), (1, 0), (-1, 0)]
            color_sources = []
            for di, dj in deltas:
                ci, cj = ni + di, nj + dj
                if 0 <= ci < self.size and 0 <= cj < self.size:
                    if self.board[ci][cj].color != WHITE:
                        color_sources.append((ci, cj))
            if color_sources:
                secrets.SystemRandom().shuffle(color_sources)
                ci, cj = color_sources[0]
                self.board[ni][nj].color = self.board[ci][cj].color

    def solve_board(self) -> None:
        """Algorithm solving queen."""
        queen_placement: tuple[int] = self._solve_step(())
        for i, j in enumerate(queen_placement):
            self.update_queen((i, j))

    def optimized_solve_board(self):
        queen_placement: tuple[int] = self._optimized_solve_step(())
        for i, j in enumerate(queen_placement):
            self.update_queen((i, j))

    def isvalid(self, queen_placement: tuple[int]) -> bool:
        """Check if a position is valid."""
        if len(set(queen_placement)) != len(queen_placement):
            return False
        seen_colors = set()
        for col, row in enumerate(queen_placement):
            color = self.board[row][col].color
            if color != WHITE:
                tcolor = tuple(color)
                if tcolor in seen_colors:
                    return False
                seen_colors.add(tcolor)

        if self._isneighbours(queen_placement):
            return False

        return True

    def queens_to_location(self) -> list:
        pos = []
        for i in range(self.size):
            for j in range(self.size):
                if self.board[i][j].state == State.QUEEN:
                    pos.append(j)
        return pos

    def load_board_from_colors(self, color_matrix: np.ndarray) -> None:
        assert color_matrix.shape[0] == self.size

        cells = color_matrix[:, :, :3].astype(np.float32)
        labels = -np.ones((self.size, self.size), dtype=int)
        region_colors = {}
        current_label = 0
        threshold = 25  # distance euclidienne en espace 0-255

        def similar(c1, c2):
            return np.linalg.norm(c1 - c2) < threshold

        for i in range(self.size):
            for j in range(self.size):
                if labels[i, j] != -1:
                    continue
                # BFS depuis cette cellule non labellisée
                queue = [(i, j)]
                labels[i, j] = current_label
                region_pixels = [cells[i, j]]

                while queue:
                    ci, cj = queue.pop(0)
                    for di, dj in [(-1,0),(1,0),(0,-1),(0,1)]:
                        ni, nj = ci + di, cj + dj
                        if 0 <= ni < self.size and 0 <= nj < self.size:
                            if labels[ni, nj] == -1 and similar(cells[ni, nj], cells[i, j]):
                                labels[ni, nj] = current_label
                                region_pixels.append(cells[ni, nj])
                                queue.append((ni, nj))

                # Couleur moyenne de la région
                region_colors[current_label] = np.mean(region_pixels, axis=0) / 255.0
                current_label += 1

        for i in range(self.size):
            for j in range(self.size):
                self.board[i][j].color = region_colors[labels[i, j]].tolist()
                hasher = sum(region_colors[labels[i, j]].tolist())
                if hasher not in self.colors:
                    self.colors[hasher] = 0
                self.colors[hasher] += 1


    def check_colors(self):
        for k,v in self.colors.items():
            print(f"Nombre de couleurs pour {k} : {v}")

    # Construction functions.

    def _add_queen(self, position: tuple[int, int]) -> None:
        i, j = position
        self.board[i][j].state = State.QUEEN

    def _add_empty(self, position: tuple[int, int]) -> None:
        i, j = position
        self.board[i][j].state = State.EMPTY


    def _get_neighbors(self, position: tuple[int, int]) -> list[int, int]:
        i, j = position
        deltas = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        neighbors = [
            (i + di, j + dj)
            for di, dj in deltas
            if 0 <= i + di < self.size and 0 <= j + dj < self.size
        ]
        secrets.SystemRandom().shuffle(neighbors)
        return neighbors


    def _solve_step(self, queen_placement: tuple[int]) -> tuple[int]:
        """Backtrack the queen game."""

        if not self.isvalid(queen_placement):
            return None

        if len(queen_placement) == self.size:
            return queen_placement

        for child in range(self.size):
                if child not in queen_placement:
                    result = self._solve_step(queen_placement + (child,))
                    if result is not None:
                        return result
        return None


    # def _optimized_solve_step(self, queen_placement: QueenPlacement) -> tuple[int]:
    #     """Backtrack the queen game."""
    #     ### Check if there's only one case left for a color : put it there. So : initialise there
    #     ### use the 3rd state
    #     ### Save nb of case for each color then try to fit it up
        
    #     if not self.isvalid(queen_placement.placement):
    #         return None


    #     if queen_placement.left_empty == 0:
    #         return queen_placement.placement

    #     for k,v in self.colors.items():
    #         if v < 1:
    #             return None
    #         if v == 1 : 
    #             for i in range(self.size):
    #                 for j in range(self.size):
    #                     if sum(region_colors[labels[i, j]].tolist()) == k:
    #                         self.colors[hasher] = None
    #                         queen_placement.placement[i] = j
    #                         result = self._solve_step(queen_placement)
                

    #     for child in range(self.size):
    #             if child not in queen_placement.placement:
    #                 result = self._solve_step(queen_placement + (child,))
    #                 if result is not None:
    #                     return result
    #     return None



    @staticmethod
    def _isneighbours(queen_placement: tuple[int]) -> bool:
        """Check if 2 queens are neighbors."""
        for i in range(len(queen_placement) - 1):
            if abs(queen_placement[i] - queen_placement[i + 1]) < 2:
                return True
        return False

    def _rd_correct_position(self) -> tuple[int]:
        """Create a random correct position."""
        while True:
            queen_placement = tuple(
                secrets.SystemRandom().sample(range(self.size), self.size)
            )
            if not self._isneighbours(queen_placement):
                return queen_placement

    def _iscolored(self) -> bool:
        """Check if the board is totally colored."""
        for i in range(self.size):
            for j in range(self.size):
                if self.board[i][j].color == WHITE:
                    return False
        return True

    def _get_colored_cases(self) -> tuple[int]:
        """Return colored case of the board."""
        colored = [
            (i, j)
            for i in range(self.size)
            for j in range(self.size)
            if self.board[i][j].color != WHITE
        ]
        secrets.SystemRandom().shuffle(colored)
        return colored

    def _get_uncolored_neighbors(self) -> tuple[int]:
        """Return all empty case near a colored one."""
        neighbors = []
        for i, j in self._get_colored_cases():
            deltas = [(0, -1), (0, 1), (1, 0), (1, 0)]
            for di, dj in deltas:
                ni, nj = i + di, j + dj
                if 0 <= ni < self.size and 0 <= nj < self.size:
                    if self.board[ni][nj].color == WHITE:
                        neighbors.append((ni, nj))
        secrets.SystemRandom().shuffle(neighbors)
        return neighbors
