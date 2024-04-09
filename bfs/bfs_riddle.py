from typing import Callable, List, Tuple

# Define the state as a tuple for simplicity, (farmer, fox, rabbit, cabbage)
State = Tuple[str, str, str, str]
Path = List[State]

start_state: State = ('L', 'L', 'L', 'L')
goal_state: State = ('R', 'R', 'R', 'R')

def is_goal(state: State) -> bool:
    return state == goal_state

def is_valid_state(state: State) -> bool:
    _, fox, rabbit, cabbage = state
    # Invalid if fox and rabbit are together without the farmer
    if fox == rabbit and fox != state[0]:
        return False
    # Invalid if rabbit and cabbage are together without the farmer
    if rabbit == cabbage and rabbit != state[0]:
        return False
    return True

def get_next_states(current_state: State) -> List[State]:
    next_states = []
    positions = ['L', 'R']
    # Try moving each character (including moving the farmer alone)
    for i in range(4):
        if current_state[i] == current_state[0]:  # Can only move with the farmer
            for pos in positions:
                new_state = list(current_state)
                new_state[0] = pos  # Move the farmer
                if i != 0:  # If not moving the farmer alone, move the character
                    new_state[i] = pos
                new_state_tuple = tuple(new_state)
                if is_valid_state(new_state_tuple):
                    next_states.append(new_state_tuple)
    return next_states

def get_next_paths(current_path: Path) -> List[Path]:
    current_state = current_path[-1]
    return [current_path + [next_state] for next_state in get_next_states(current_state)]

def bfs(
    start_state: State,
    is_goal: Callable[[State], bool],
    get_next_paths: Callable[[Path], List[Path]],
) -> Path:
    frontier: List[Path] = [[start_state]]
    visited = set()
    while path:=frontier.pop(0):
        if is_goal(path[-1]):
            return path
        state_tuple = tuple(sorted(path[-1]))
        if state_tuple in visited:
            continue
   
        frontier.extend(get_next_paths(path))
    return []

# Find the solution
solution_path = bfs(start_state, is_goal, get_next_paths)
for step, state in enumerate(solution_path):
    print(f"Step {step}: Farmer={state[0]}, Fox={state[1]}, Rabbit={state[2]}, Cabbage={state[3]}")
