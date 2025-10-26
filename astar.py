# astar.py
# --- Generic A* implementation for the 8-puzzle ---

from heapq import heappush, heappop
from itertools import count
from typing import Callable, Dict, Optional, Tuple, List, Set
from puzzle import neighbors, is_goal, State, GOAL

Heuristic = Callable[[State], int]

def reconstruct(parent: Dict[State, Optional[State]], goal: State) -> List[State]:
    path = [goal]
    cur = goal
    while parent[cur] is not None:
        cur = parent[cur]
        path.append(cur)
    path.reverse()
    return path

def astar(start: State, h: Heuristic):
    tie = count()
    open_heap = []
    heappush(open_heap, (h(start), next(tie), start))

    g = {start: 0}
    parent = {start: None}
    closed: Set[State] = set()
    expanded = 0

    while open_heap:
        f, _, u = heappop(open_heap)
        if u in closed:
            continue
        if is_goal(u):
            return reconstruct(parent, u), expanded
        closed.add(u)
        expanded += 1

        for v in neighbors(u):
            tentative = g[u] + 1
            if v in closed:
                continue
            if v not in g or tentative < g[v]:
                g[v] = tentative
                parent[v] = u
                heappush(open_heap, (tentative + h(v), next(tie), v))
    return None, expanded
