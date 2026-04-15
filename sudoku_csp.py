from __future__ import annotations

import sys

from sudoku_io import board_to_string, read_board
from sudoku_solver import solve_board


def main() -> None:
    if len(sys.argv) < 2:
        file_paths = ["sudoku_boards/easy.txt"]
        print("No input file provided. Defaulting to: sudoku_boards/easy.txt")
    else:
        file_paths = sys.argv[1:]

    for file_path in file_paths:
        print("=" * 60)
        print(f"Input file: {file_path}")
        board = read_board(file_path)
        solved, stats = solve_board(board)

        if solved is None:
            print("No solution found.")
        else:
            print("Solved board:")
            print(board_to_string(solved))

        print("\nRequired stats:")
        print(f"BACKTRACK calls: {stats.backtrack_calls}")
        print(f"BACKTRACK failures: {stats.backtrack_failures}")


if __name__ == "__main__":
    main()
