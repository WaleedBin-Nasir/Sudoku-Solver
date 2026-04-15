from __future__ import annotations

import os
import tkinter as tk
from tkinter import messagebox, ttk

from sudoku_io import read_board
from sudoku_solver import Grid, solve_board


class SudokuApp:
    def __init__(self) -> None:
        self.root = tk.Tk()
        self.root.title("Sudoku CSP Simulator")
        self.root.minsize(980, 680)

        self.board_var = tk.StringVar(value="easy.txt")
        self.board_files = ["easy.txt", "medium.txt", "hard.txt", "veryhard.txt"]
        self.stats_var = tk.StringVar(value="Ready.")

        self.current_input: Grid | None = None
        self.current_solution: Grid | None = None

        main = tk.Frame(self.root, padx=16, pady=16)
        main.pack(fill=tk.BOTH, expand=True)

        controls = tk.Frame(main)
        controls.pack(fill=tk.X)

        tk.Label(controls, text="Select Board:", font=("Segoe UI", 10, "bold")).pack(
            side=tk.LEFT, padx=(0, 8)
        )
        ttk.Combobox(
            controls,
            textvariable=self.board_var,
            values=self.board_files,
            state="readonly",
            width=16,
        ).pack(side=tk.LEFT, padx=(0, 10))

        tk.Button(controls, text="Load Board", command=self.load_selected_board).pack(
            side=tk.LEFT, padx=4
        )
        tk.Button(
            controls,
            text="Solve (AC-3 + FC + Backtracking)",
            command=self.solve_selected_board,
        ).pack(side=tk.LEFT, padx=4)
        tk.Button(controls, text="Reset", command=self.reset_view).pack(
            side=tk.LEFT, padx=4
        )

        boards_wrap = tk.Frame(main)
        boards_wrap.pack(fill=tk.BOTH, expand=True, pady=(14, 0))

        self.input_panel = tk.Frame(boards_wrap)
        self.input_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.output_panel = tk.Frame(boards_wrap)
        self.output_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        tk.Label(
            self.input_panel, text="Input Board", font=("Segoe UI", 11, "bold")
        ).pack(pady=(0, 8))
        tk.Label(
            self.output_panel, text="Solved Board", font=("Segoe UI", 11, "bold")
        ).pack(pady=(0, 8))

        self.input_canvas = tk.Canvas(
            self.input_panel, width=430, height=430, bg="#f3f3f3", highlightthickness=0
        )
        self.input_canvas.pack(fill=tk.BOTH, expand=True)

        self.output_canvas = tk.Canvas(
            self.output_panel, width=430, height=430, bg="#f3f3f3", highlightthickness=0
        )
        self.output_canvas.pack(fill=tk.BOTH, expand=True)
        self.input_canvas.bind("<Configure>", lambda _e: self._draw_board(self.input_canvas, self.current_input))
        self.output_canvas.bind(
            "<Configure>", lambda _e: self._draw_board(self.output_canvas, self.current_solution)
        )

        stats_frame = tk.Frame(main)
        stats_frame.pack(fill=tk.X, pady=(10, 0))
        tk.Label(
            stats_frame, textvariable=self.stats_var, justify=tk.LEFT, font=("Consolas", 11)
        ).pack(anchor=tk.W)

        self.load_selected_board()
        self.root.mainloop()

    def _board_path(self) -> str:
        return os.path.join("sudoku_boards", self.board_var.get().strip())

    def _draw_board(self, canvas: tk.Canvas, board: Grid | None) -> None:
        canvas.delete("all")

        size = min(canvas.winfo_width(), canvas.winfo_height())
        if size <= 1:
            size = 430
        grid_size = int(size * 0.9)
        cell = grid_size / 9
        x0 = (size - grid_size) / 2
        y0 = (size - grid_size) / 2

        # Outer box
        canvas.create_rectangle(x0, y0, x0 + grid_size, y0 + grid_size, width=2)

        # Grid lines
        for i in range(1, 9):
            w = 2 if i % 3 == 0 else 1
            x = x0 + i * cell
            y = y0 + i * cell
            canvas.create_line(x, y0, x, y0 + grid_size, width=w)
            canvas.create_line(x0, y, x0 + grid_size, y, width=w)

        if board is None:
            return

        for r in range(9):
            for c in range(9):
                val = board[r][c]
                if val == 0:
                    continue
                x = x0 + (c + 0.5) * cell
                y = y0 + (r + 0.5) * cell
                canvas.create_text(
                    x,
                    y,
                    text=str(val),
                    font=("Times New Roman", max(14, int(cell * 0.45)), "bold"),
                    fill="#1d3f6e",
                )

    def _redraw_all(self) -> None:
        self._draw_board(self.input_canvas, self.current_input)
        self._draw_board(self.output_canvas, self.current_solution)

    def reset_view(self) -> None:
        self.current_input = None
        self.current_solution = None
        self.stats_var.set("Ready.")
        self._redraw_all()

    def load_selected_board(self) -> None:
        path = self._board_path()
        try:
            board = read_board(path)
        except Exception as exc:
            messagebox.showerror("Load Error", str(exc))
            return

        self.current_input = board
        self.current_solution = None
        self.stats_var.set(f"Loaded {path}\nClick solve to run CSP.")
        self._redraw_all()

    def solve_selected_board(self) -> None:
        path = self._board_path()
        try:
            board = read_board(path)
        except Exception as exc:
            messagebox.showerror("Read Error", str(exc))
            return

        solved, stats = solve_board(board)
        self.current_input = board
        self.current_solution = solved
        self._redraw_all()

        if solved is None:
            self.stats_var.set(
                f"Input file: {path}\nNo solution found.\n"
                f"BACKTRACK calls: {stats.backtrack_calls}\n"
                f"BACKTRACK failures: {stats.backtrack_failures}"
            )
        else:
            self.stats_var.set(
                f"Input file: {path}\nSolved successfully.\n"
                f"BACKTRACK calls: {stats.backtrack_calls}\n"
                f"BACKTRACK failures: {stats.backtrack_failures}"
            )


if __name__ == "__main__":
    SudokuApp()
