import environment
import random
from math import sqrt

DOWN = 0
UP = 1
RIGHT = 2
LEFT = 3

ACTIONS = [DOWN, UP, RIGHT, LEFT]

class NPuzzle(environment.Environment):

    def __init__(self, n1sqrt=3, seed=None):
        self._rng = random.Random(seed)
        self._state = NPuzzleBoard(n1sqrt)
        self._goal = NPuzzleBoard()
        self.reset()

    def render(self):
        self._state.render()

    def step(self, action):
        succ = self._state.successor(action)
        if succ is not None:
            self._state = succ
        return self.done() 
    
    def actions(self):
        return ACTIONS

    def n(self):
        return self._state.n()

    def reset(self):
        random_walk_length = self.n()**3
        for _ in range(random_walk_length):
            succ = self._state.successors()
            _, next_state = self._rng.sample(succ, 1)[0]
            self._state = next_state

    def done(self):
        return self._state == self._goal

    def state(self):
        return self._state


class NPuzzleBoard(environment.State):

    def __init__(self, n1sqrt=3, initial_configuration=None):
        self._n1sqrt = n1sqrt
        if initial_configuration is not None:
            assert self.n()+1 == len(initial_configuration)
            self._board = tuple(initial_configuration)
        else:
            self._board = tuple(range(self.n()+1))
        
    def __hash__(self):
        return hash(self._board)

    def __eq__(self, other):
        if not isinstance(other, NPuzzleBoard):
            return NotImplemented
        return self._board == other._board

    def successor(self, action):
        hole_index = self._board.index(0)
        hole_r = hole_index // self._n1sqrt
        hole_c = hole_index % self._n1sqrt
        swap_hole_to = None
        if action == DOWN:
            if hole_r - 1 >= 0:
                swap_hole_to = (hole_r-1)*self._n1sqrt + hole_c
        elif action == UP:
            if hole_r + 1 < self._n1sqrt:
                swap_hole_to = (hole_r+1)*self._n1sqrt + hole_c
        elif action == RIGHT:
            if hole_c - 1 >= 0:
                swap_hole_to = hole_r*self._n1sqrt + hole_c-1
        elif action == LEFT:
            if hole_c + 1 < self._n1sqrt:
                swap_hole_to = hole_r*self._n1sqrt + hole_c+1
        if swap_hole_to is not None:
            board = list(self._board)
            board[hole_index], board[swap_hole_to] = \
                    board[swap_hole_to], board[hole_index]
            return NPuzzleBoard(self._n1sqrt, board)
        return None

    def successors(self):
        successors = []
        for a in ACTIONS:
            succ = self.successor(a)
            if succ is not None:
                successors.append((a, succ))
        return successors

    def render(self):
        for row in range(self._n1sqrt):
            print("\t".join(str(cell) for cell in
                self._board[row*self._n1sqrt:(row+1)*self._n1sqrt]))

    def n(self):
        return self._n1sqrt*self._n1sqrt - 1

    def manhattan_distance(self):
        distance = 0
        for idx, cell in enumerate(self._board):
            if cell != 0:
                row = idx // self._n1sqrt
                col = idx % self._n1sqrt
                dst_row = (cell-1) // self._n1sqrt
                dst_col = (cell-1) % self._n1sqrt
                distance += abs(row-dst_row) + abs(col-dst_col)
        return distance



