"""Create and solve a queen game."""

import argparse

from objects import Game


def parse_arguments() -> argparse.Namespace:
    """Parse the argumentsof the command line."""
    parser = argparse.ArgumentParser(description="Create and solve a queen game.")
    parser.add_argument("size", type=int, help='Size of the queen board.')
    return parser.parse_args()

def main() -> None:
    """Execute the code."""
    args = parse_arguments()
    size = args.size
    test = Game(size=size)
    test.create_colored_rd_board()
    test.show()
    test.solve_board()
    test.show()


if __name__ == "__main__":
    main()
