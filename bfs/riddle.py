import pytest

"""
farmer, fox, cabbage, rabbit
task: farmer is to move all items accross the river but there are some constraints
1. cant leave rabbit with fox because fox will eat the rabbit
2. cant leave rabbit with cabbage because rabbit will eat the cabbage
3. boat can only take the farmer and one other item... and farmer has to be on the boat to row the boat

solution:

farmer + rabbit -> drop rabbit accross the river
farmer + None -> back to the initial position
farmer + cabbage -> drop cabbage accross the river and pick up rabbit
farmer + rabbit -> drop rabbit at initial position
farmer + fox -> drop fox accross the river
farmer + None -> back to the initial position
farmer + rabbit -> drop rabbit accross the river


frame as a graph problem:

start_position: one side of the river (say left)
end_position: other side of the river (say right)

nodes: farmer, rabbit, cabbage, fox


"""
current_state = {"farmer": "left", "rabbit": "left", "cabbage": "left", "fox": "left"}

goal = {"farmer": "right", "rabbit": "right", "cabbage": "right", "fox": "right"}


def is_goal(state):
    return state == goal


def is_valid_state(state):
    """
    A valid state is one in which the rabbit is not left with the fox and the rabbit is not left with the cabbage
    """
    # if rabbit position is the same as fox position and farmer position is not the same as fox position
    if state["rabbit"] == state["fox"] and state["farmer"] != state["fox"]:
        return False
    # if rabbit position is the same as cabbage and farmer position is not the same as cabbage position
    if state["rabbit"] == state["cabbage"] and state["farmer"] != state["cabbage"]:
        return False
    return True


def get_next_states(state):
    next_states = []
    items = ["rabbit", "cabbage", "fox", None]
    # Attempt to move each item and the case where the farmer moves alone.
    for item in items:
        if (
            item is None or state["farmer"] == state[item]
        ):  # Can move item or just the farmer
            new_state = state.copy()
            # Move the farmer; if an item is specified, move it with the farmer.
            new_state["farmer"] = "right" if state["farmer"] == "left" else "left"
            if item != None:
                new_state[item] = "right" if state[item] == "left" else "left"
            if is_valid_state(new_state):
                next_states.append(new_state)
    return next_states

    
def bfs(current_state, is_goal, get_next_states):
    frontier = [(current_state, [])]  # Track path as a list of states
    visited = set()  # Keep track of visited states to avoid loops
    while frontier:
        current_state, path = frontier.pop(0)
        if is_goal(current_state):
            return path + [current_state]  # Return the path including the goal state
        # Convert state to a hashable tuple for tracking visited states.
        state_tuple = tuple(sorted(current_state.items()))
        if state_tuple in visited:
            continue
        visited.add(state_tuple)
        for next_state in get_next_states(current_state):
            new_path = path + [current_state]  # Append current state to new path
            frontier.append((next_state, new_path))
    return None


# Example usage
if __name__ == "__main__":
    solution_path = bfs(current_state, is_goal, get_next_states)
    if solution_path:
        for step, state in enumerate(solution_path):
            print(f"Step {step}: {state}")
    else:
        print("No solution found.")
