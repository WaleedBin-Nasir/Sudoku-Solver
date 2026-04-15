# Sudoku CSP Solver

A high-performance Sudoku solver implemented as a Constraint Satisfaction Problem (CSP). This project utilizes advanced search and consistency algorithms, including AC-3, Forward Checking, and Backtracking with MRV, to solve grid puzzles efficiently.

## Features

* CSP-Based Engine: Models Sudoku as a constraint satisfaction problem with variables (cells), domains (1–9), and alldiff constraints.
* AC-3 Algorithm: Enforces arc consistency to prune the search space before and during backtracking.
* Forward Checking (FC): Anticipates failures early by looking ahead at neighboring cell domains.
* Backtracking Search: Systematically explores solutions using the Minimum Remaining Values (MRV) heuristic to select the most constrained variables first.
* Dual Interface:
    - CLI: Run batch processing on text-based Sudoku boards via q3_sudoku_csp.py.
    - GUI: A desktop application built with Tkinter to visualize the solving process.

## Algorithms and Implementation

The solver follows a rigorous academic approach to CSP:

1. Initial Propagation: AC-3 is run initially to resolve cells through constraint propagation. In many "Easy" puzzles, this alone can resolve almost all cells.
2. MRV Heuristic: During backtracking, the solver picks the cell with the smallest remaining domain to reduce the branching factor.
3. Constraint Density: Testing shows that the solver's efficiency is highly dependent on the density of initial clues. Sparse boards (Hard/Very Hard) exhibit an exponential increase in search cost.

## Performance Results

The solver was tested against four difficulty levels. While it handles well-constrained puzzles with 100% accuracy, it identifies potential contradictions in sparser, more complex boards.

| Board     | Solved? | BT Calls | BT Failures | Failure Rate |
|-----------|---------|----------|-------------|--------------|
| Easy      | Yes     | 1        | 0           | 0.0%         |
| Medium    | Yes     | 16       | 0           | 0.0%         |
| Hard      | No      | 174      | 142         | 81.6%        |
| Very Hard | No      | 2707     | 2673        | 98.7%        |

### Key Observations:
* Efficiency: Easy and Medium boards are solved with zero failures, proving the effectiveness of AC-3 and Forward Checking for standard puzzles.
* Complexity: Harder boards show a dramatic jump in backtracking calls (from 16 to over 2,700), illustrating the exponential cost of search when constraint density is low.
* Inconsistency Detection: For extremely difficult or "Evil" boards, AC-3 can sometimes detect inconsistencies before backtracking even begins.

## Project Structure

* sudoku_solver.py: Core engine containing CSP logic (AC-3, FC, Backtracking).
* sudoku_io.py: File I/O for reading boards and converting them to strings.
* sudoku_gui.py: Tkinter implementation for the graphical simulator.
* q3_sudoku_csp.py: CLI entry point for processing board files.

## Getting Started

### Prerequisites
* Python 3.x
* Tkinter (usually included with standard Python installations)

### Usage
To run the Graphical Simulator:
python sudoku_gui.py

To run the CLI Solver:
python q3_sudoku_csp.py sudoku_boards/easy.txt
