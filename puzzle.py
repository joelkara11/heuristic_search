# -----------------------------------------------------------
# Module: puzzle.py
# Inputs: State (tuple of 9 ints), optional steps/seed
# Outputs: Neighbors, random solvable states, bool (solvable)
# Function: Represents the 8-puzzle board; generates legal moves,
#           checks solvability (inversions), and produces random solvable states.
# -----------------------------------------------------------


from typing import Tuple, Iterable
import random

State = Tuple[int, ...]
GOAL: State = (1,2,3,4,5,6,7,8,0)

def is_goal(state: State) -> bool:
    return state == GOAL

def index_rc(idx: int):
    return divmod(idx, 3)

def rc_index(r, c):
    return r * 3 + c

def neighbors(state: State) -> Iterable[State]:
    z = state.index(0)
    zr, zc = index_rc(z)
    for dr, dc in [(-1,0), (1,0), (0,-1), (0,1)]:
        nr, nc = zr + dr, zc + dc
        if 0 <= nr < 3 and 0 <= nc < 3:
            ni = rc_index(nr, nc)
            new_state = list(state)
            new_state[z], new_state[ni] = new_state[ni], new_state[z]
            yield tuple(new_state)

def inversions(state: State) -> int:
    arr = [x for x in state if x != 0]
    return sum(1 for i in range(len(arr)) for j in range(i+1,len(arr)) if arr[i] > arr[j])

def is_solvable(state: State) -> bool:
    return inversions(state) % 2 == 0

def random_walk(start: State = GOAL, steps: int = 20) -> State:
    s = start
    last = None
    for _ in range(steps):
        cand = list(neighbors(s))
        if last in cand and len(cand) > 1:
            cand.remove(last)
        nxt = random.choice(cand)
        last, s = s, nxt
    return s
