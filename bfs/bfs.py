from typing import Callable

import pytest
import time
# chess puzzle

# how do i represent the state of the system?
# how do i generate all possible edges that can be traversed from a given node?
# what is the starting point
# what is the goal / how do i know when i'm done?

# # # # # # # #
"""
0 # # # # # # #
# # 1 # # # # #
# # # # # # # #
# 2 # # # # # #
# # # 3 # # # #
# # # # # # 5 #
# # # # 4 # # #
# # # # # # # 6
"""

Square = tuple[int, int]
Path = list[Square]

start: Square = (0, 0)
goal: Square = (7, 7)

current_state: Path = [start]


def is_goal(state: Path) -> bool:
    return state[-1] == goal


def is_valid_coordinate(coordinate: int) -> bool:
    return 0 <= coordinate <= 7


# def is_valid_square(square: Square) -> bool:
#     return all([is_valid_coordinate(coordinate) for coordinate in square])

def is_valid_square(square):
    valid = True
    for coordinate in square:
        if not is_valid_coordinate(coordinate):
            valid = False   
    return valid

def get_next_squares(current_square: Square) -> list[Square]:
    directions = [
        (-2, -1),
        (-1, 2),
        (1, -2),
        (2, 1),
        (1, 2),
        (-1, -2),
        (2, -1),
        (-2, 1),
    ]
    next_suqares = [
        (current_square[0] + direction[0], current_square[1]+direction[1])
        for direction in directions
    ]
    
    valid_squares = [
        square for square in next_suqares if is_valid_square(square)
    ]
    return valid_squares


def get_next_paths(current_path: Path) -> list[Path]:
    current_square = current_path[-1]
    
    valid_squares = get_next_squares(current_square)
    
    return [
        current_path + [square] for square in valid_squares
    ]        


def bfs(
    current_state: Path,
    is_goal: Callable[[Path], bool],
    get_next_paths: Callable[[Path], list[Path]],
):
    frontier = [current_state]
    while current_path := frontier.pop(0):
        if is_goal(current_path):
            return current_path
        
        frontier.extend(get_next_paths(current_path))
    return []   

@pytest.mark.parametrize(
    "square,valid",
    [
        ((0, 0), True),
        ((8, 8), False),
        ((-1, 0), False),
        ((0, -1), False),
        ((0, 8), False),
        ((8, 0), False),
        ((7, 7), True),
        ((0, 7), True),
    ],
)
def test_is_valid_square(square, valid):
    assert is_valid_square(square) == valid


best_path = bfs(current_state=[(0, 0)], is_goal=is_goal, get_next_paths=get_next_paths)
print(best_path)
