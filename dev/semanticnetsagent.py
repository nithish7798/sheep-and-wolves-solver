from collections import deque

class State:
    def __init__(self, state_vars, num_moves=0, move=(0, 0), parent=None):
        self.state_vars = state_vars
        self.num_moves = num_moves
        self.parent = parent
        self.move = move

    @classmethod
    def initialState(cls, initialSheep, initialWolves):
        return cls((initialSheep, initialWolves, 1))

    def get_possible_moves(self):
        return [(1, 0), (2, 0), (0, 1), (0, 2), (1, 1)]

    def is_legal(self, initialSheep, initialWolves):
        sheep, wolves, boat = self.state_vars

        if sheep < 0 or sheep > initialSheep:
            return False
        elif wolves < 0 or wolves > initialWolves:
            return False
        elif sheep > 0 and wolves > sheep:
            return False
        return True

    def is_solution(self):
        return self.state_vars == (0, 0, 0)

    def get_next_states(self, initialSheep, initialWolves):
        moves = self.get_possible_moves()
        all_states = []

        for move in moves:
            change_sheep, change_wolves = move
            sheep, wolves, boat = self.state_vars
            new_boat = 1 - boat

            if boat == 1:  # Boat on the right side
                new_state_vars = (sheep - change_sheep, wolves - change_wolves, new_boat)
            else:
                new_state_vars = (sheep + change_sheep, wolves + change_wolves, new_boat)

            new_state = State(new_state_vars, self.num_moves + 1, move, self)
            if new_state.is_legal(initialSheep, initialWolves):
                all_states.append(new_state)

        return all_states


class SemanticNetsAgent:
    def solve(self, initialSheep, initialWolves):
        initial_state = State.initialState(initialSheep, initialWolves)
        to_search = deque([(initial_state, [])])
        seen_states = set()
        solutions = []

        while to_search:
            current_state, path = to_search.popleft()
            state_vars = current_state.state_vars

            if state_vars in seen_states:
                continue

            seen_states.add(state_vars)

            if current_state.is_solution():
                solutions.append(path)
                continue

            next_states = current_state.get_next_states(initialSheep, initialWolves)
            for next_state in next_states:
                to_search.append((next_state, path + [next_state.move]))

        return solutions
