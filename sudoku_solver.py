from __future__ import annotations

from collections import deque
import copy
from dataclasses import dataclass

Grid = list[list[int]]
Cell = tuple[int, int]
Domains = dict[Cell, set[int]]


def _peers_of(cell: Cell) -> set[Cell]:
    row, col = cell
    peers: set[Cell] = set()

    for c in range(9):
        if c != col:
            peers.add((row, c))
    for r in range(9):
        if r != row:
            peers.add((r, col))

    box_r = (row // 3) * 3
    box_c = (col // 3) * 3
    for r in range(box_r, box_r + 3):
        for c in range(box_c, box_c + 3):
            if (r, c) != cell:
                peers.add((r, c))
    return peers


ALL_CELLS: list[Cell] = [(r, c) for r in range(9) for c in range(9)]
PEERS: dict[Cell, set[Cell]] = {cell: _peers_of(cell) for cell in ALL_CELLS}


@dataclass
class SolverStats:
    backtrack_calls: int = 0
    backtrack_failures: int = 0


def board_to_domains(board: Grid) -> Domains:
    domains: Domains = {}
    for r in range(9):
        for c in range(9):
            val = board[r][c]
            domains[(r, c)] = {val} if val != 0 else set(range(1, 10))
    return domains


def revise(domains: Domains, xi: Cell, xj: Cell) -> bool:
    revised = False
    if len(domains[xi]) == 1 and len(domains[xj]) == 1:
        if next(iter(domains[xi])) == next(iter(domains[xj])):
            domains[xi].clear()
            return True
    if len(domains[xj]) == 1:
        only = next(iter(domains[xj]))
        if only in domains[xi] and len(domains[xi]) > 1:
            domains[xi].remove(only)
            revised = True
    return revised


def ac3(domains: Domains, queue: deque[tuple[Cell, Cell]] | None = None) -> bool:
    if queue is None:
        queue = deque()
        for xi in ALL_CELLS:
            for xj in PEERS[xi]:
                queue.append((xi, xj))

    while queue:
        xi, xj = queue.popleft()
        if revise(domains, xi, xj):
            if not domains[xi]:
                return False
            for xk in PEERS[xi]:
                if xk != xj:
                    queue.append((xk, xi))
    return True


def is_consistent_assignment(domains: Domains, cell: Cell, value: int) -> bool:
    for peer in PEERS[cell]:
        if len(domains[peer]) == 1 and value in domains[peer]:
            return False
    return True


def select_unassigned_variable(domains: Domains) -> Cell | None:
    unassigned = [cell for cell in ALL_CELLS if len(domains[cell]) > 1]
    if not unassigned:
        return None
    return min(unassigned, key=lambda cell: len(domains[cell]))


def order_domain_values(domains: Domains, cell: Cell) -> list[int]:
    return sorted(domains[cell])


def forward_check(domains: Domains, cell: Cell, value: int) -> bool:
    for peer in PEERS[cell]:
        if len(domains[peer]) > 1 and value in domains[peer]:
            domains[peer].remove(value)
            if not domains[peer]:
                return False
    return True


def backtrack(domains: Domains, stats: SolverStats) -> Domains | None:
    stats.backtrack_calls += 1

    var = select_unassigned_variable(domains)
    if var is None:
        return domains

    for value in order_domain_values(domains, var):
        if not is_consistent_assignment(domains, var, value):
            continue

        next_domains = copy.deepcopy(domains)
        next_domains[var] = {value}

        if not forward_check(next_domains, var, value):
            continue

        q = deque((peer, var) for peer in PEERS[var])
        if not ac3(next_domains, q):
            continue

        result = backtrack(next_domains, stats)
        if result is not None:
            return result

    stats.backtrack_failures += 1
    return None


def domains_to_board(domains: Domains) -> Grid:
    board: Grid = [[0 for _ in range(9)] for _ in range(9)]
    for (r, c), values in domains.items():
        if len(values) != 1:
            raise ValueError("Unresolved board domains.")
        board[r][c] = next(iter(values))
    return board


def solve_board(board: Grid) -> tuple[Grid | None, SolverStats]:
    stats = SolverStats()
    domains = board_to_domains(board)

    if not ac3(domains):
        return None, stats

    solved = backtrack(domains, stats)
    if solved is None:
        return None, stats
    solved_board = domains_to_board(solved)
    if not _is_complete_solution(solved_board):
        return None, stats
    return solved_board, stats


def _is_complete_solution(board: Grid) -> bool:
    target = set(range(1, 10))

    for r in range(9):
        if set(board[r]) != target:
            return False

    for c in range(9):
        col_vals = {board[r][c] for r in range(9)}
        if col_vals != target:
            return False

    for br in range(0, 9, 3):
        for bc in range(0, 9, 3):
            box_vals = set()
            for r in range(br, br + 3):
                for c in range(bc, bc + 3):
                    box_vals.add(board[r][c])
            if box_vals != target:
                return False

    return True
