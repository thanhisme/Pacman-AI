import heapq

from game_config import *

class AStar:
    @staticmethod
    def heuristic(a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    @staticmethod
    def search(problem, goal):
        """
        Finds the path from the initial state to the goal using the A* algorithm.
        """
        frontier = [(
            AStar.heuristic(problem.initial_state, goal), 
            problem.initial_state, 
            0, 
            problem.power_steps, 
            [problem.initial_state]
        )]
        explored = set()

        while frontier:
            _, current_state, current_cost, current_power, current_path = heapq.heappop(frontier)

            # If the goal is reached, return the path
            if current_state == goal:
                problem.power_steps = current_power
                return current_path

            # Mark node as explored
            if current_state in explored:
                continue
            explored.add(current_state)

            # Expand to next possible states
            for action in problem.get_actions(current_state, current_power):
                child_state = action
                new_cost = current_cost + 1
                new_power = max(0, current_power - 1)

                # If pie is found, reset power_steps
                if problem.maze[child_state[0]][child_state[1]] == PIE_CHAR:
                    new_power = POWER_STEP_DURATION

                # Add to the frontier if not explored yet
                if child_state not in explored:
                    heapq.heappush(frontier, (
                        new_cost + AStar.heuristic(child_state, goal),
                        child_state,
                        new_cost,
                        new_power,
                        current_path + [child_state]
                    ))

        return None
