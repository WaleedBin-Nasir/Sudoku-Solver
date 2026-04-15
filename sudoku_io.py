from __future__ import annotations

from sudoku_solver import Grid


def read_board(file_path: str) -> Grid:
    with open(file_path, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f if line.strip()]

    if len(lines) != 9:
        raise ValueError(f"{file_path}: board must contain exactly 9 non-empty lines.")

    board: Grid = []
    for i, line in enumerate(lines, start=1):
        if len(line) != 9 or any(ch < "0" or ch > "9" for ch in line):
            raise ValueError(
                f"{file_path}: line {i} must contain exactly 9 digits (0-9)."
            )
        board.append([int(ch) for ch in line])
    return board


def board_to_string(board: Grid) -> str:
    lines: list[str] = []
    for r in range(9):
        row_parts: list[str] = []
        for c in range(9):
            row_parts.append(str(board[r][c]))
            if c in (2, 5):
                row_parts.append("|")
        lines.append(" ".join(row_parts))
        if r in (2, 5):
            lines.append("-" * 21)
    return "\n".join(lines)
