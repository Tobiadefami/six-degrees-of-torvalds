import networkx as nx
from riddle import get_next_states, is_goal
import matplotlib.pyplot as plt

# Assuming your bfs function and all supporting functions are defined as before
current_state = {"farmer": "left", "rabbit": "left", "cabbage": "left", "fox": "left"}

# New BFS function that builds a graph
def bfs_with_graph(current_state, is_goal, get_next_states):
    G = nx.DiGraph()  # Directed graph to represent state transitions
    frontier = [(current_state, [])]
    visited = set()

    while frontier:
        current_state, path = frontier.pop(0)
        state_str = str(current_state)  # Convert state to a string to use as a node
        if state_str not in G:
            G.add_node(state_str, label=state_str)

        state_tuple = tuple(sorted(current_state.items()))
        if state_tuple in visited:
            continue
        visited.add(state_tuple)

        if is_goal(current_state):
            return G, path + [current_state]

        for next_state in get_next_states(current_state):
            next_state_str = str(next_state)
            G.add_edge(state_str, next_state_str)  # Add edge from current to next state
            new_path = path + [current_state]
            frontier.append((next_state, new_path))

    return G, None

# Visualize the graph
def visualize_graph(G):
    pos = nx.spring_layout(G)  # Generate a layout for the nodes
    nx.draw(G, pos, with_labels=True, node_size=2000, node_color="lightblue", font_size=10, arrows=True)
    plt.show()

# Example usage
if __name__ == "__main__":
    G, solution_path = bfs_with_graph(current_state, is_goal, get_next_states)
    if solution_path:
        print("Solution found.")
        visualize_graph(G)
    else:
        print("No solution found.")
