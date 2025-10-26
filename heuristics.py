# -----------------------------------------------------------
# Module: heuristics.py
# Inputs: State (tuple of 9 ints)
# Outputs: Nonnegative heuristic value (int)
# Function: Implements Hamming and Manhattan distance heuristics
#           for the 8-puzzle (both admissible).
# -----------------------------------------------------------


from typing import Tuple
State = Tuple[int, ...]
GOAL = (1,2,3,4,5,6,7,8,0)

def hamming(state: State) -> int:
    return sum(1 for i,v in enumerate(state) if v != 0 and v != GOAL[i])

def manhattan(state: State) -> int:
    dist = 0
    for i,v in enumerate(state):
        if v == 0:
            continue
        r, c = divmod(i,3)
        gr, gc = divmod(GOAL.index(v),3)
        dist += abs(r-gr) + abs(c-gc)
    return dist
