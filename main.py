"""Create and solve a queen game."""

from objects import Game


def main() -> None:
    """Execute the code."""
    test = Game(size=13)
    test.create_colored_rd_board()
    test.show()
    test.solve_board()
    test.show()


if __name__ == "__main__":
    main()
