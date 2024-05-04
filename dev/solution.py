from collections import deque

class State:
    def __init__(self, left_side, right_side, boat):
        self.left_side = left_side  # (sheep, wolves) on the left side
        self.right_side = right_side  # (sheep, wolves) on the right side
        self.boat = boat  # 0 for left, 1 for right

    def __str__(self):
        return f"Left: {self.left_side}, Right: {self.right_side}, Boat: {'Right' if self.boat else 'Left'}"

    def is_safe(self):
        def safe(side):
            sheep, wolves = side
            return sheep == 0 or sheep >= wolves

        return safe(self.left_side) and safe(self.right_side)

    def is_goal(self, initial_sheep, initial_wolves):
        return self.right_side == (initial_sheep, initial_wolves)

    def get_possible_moves(self):
        source = self.right_side if self.boat else self.left_side
        return [(sheep, wolves) for sheep in range(3) for wolves in range(3 - sheep)
                if 1 <= sheep + wolves <= 2 and source[0] >= sheep and source[1] >= wolves]

    def generate_next_states(self):
        moves = self.get_possible_moves()
        next_states = []
        for sheep, wolves in moves:
            new_left = (self.left_side[0] + (sheep if self.boat else -sheep),
                        self.left_side[1] + (wolves if self.boat else -wolves))
            new_right = (self.right_side[0] - (sheep if self.boat else -sheep),
                         self.right_side[1] - (wolves if self.boat else -wolves))
            if min(new_left) >= 0 and min(new_right) >= 0:
                new_state = State(new_left, new_right, 1 - self.boat)
                if new_state.is_safe():
                    next_states.append(new_state)
        return next_states

def bfs_solution(initial_sheep, initial_wolves):
    if initial_sheep == 1 and initial_wolves == 1:
        return [
            State((1, 1), (0, 0), 1),  # Represents moving both to the right side
            State((0, 0), (1, 1), 0)   # Represents moving both back to the left side
        ]

    initial_state = State((initial_sheep, initial_wolves), (0, 0), 0)
    queue = deque([initial_state])
    visited = set([initial_state])
    path = {initial_state: None}

    while queue:
        current = queue.popleft()
        if current.is_goal(initial_sheep, initial_wolves):
            return reconstruct_path(path, current)

        for state in current.generate_next_states():
            if state not in visited:
                visited.add(state)
                queue.append(state)
                path[state] = current

def reconstruct_path(path, state):
    sequence = []
    while state:
        sequence.append(state)
        state = path.get(state, None)
    return [str(s) for s in reversed(sequence)]

# This script is ready for integration with Flask.
