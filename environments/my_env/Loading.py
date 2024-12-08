import heapq
import copy

class AStarLoading:
    def __init__(self, grid, containers, manifest):
        self.grid = grid  # 2D grid representing the ship
        self.containers = containers  # List of containers to be loaded
        self.manifest = manifest  # Manifest file to track positions

    def heuristic(self, state, remaining_containers):
        """
        Estimate cost (Manhattan distance) for placing remaining containers.
        """
        total_cost = 0
        for container in remaining_containers:
            min_distance = float('inf')
            for y, row in enumerate(state):
                for x, slot in enumerate(row):
                    if slot == 'UNUSED':
                        distance = abs(container.yPos - y) + abs(container.xPos - x)
                        min_distance = min(min_distance, distance)
            total_cost += min_distance
        return total_cost

    def is_goal_state(self, state, remaining_containers):
        """
        Goal is reached if all containers are placed on the grid.
        """
        return len(remaining_containers) == 0

    def get_neighbors(self, state, container):
        """
        Generate all possible states by placing the current container.
        """
        neighbors = []
        for y, row in enumerate(state):
            for x, slot in enumerate(row):
                if slot == 'UNUSED':
                    new_state = copy.deepcopy(state)
                    new_state[y][x] = container.name
                    neighbors.append((new_state, x, y))
        return neighbors

    def a_star(self):
        """
        A* algorithm to find the optimal container placement.
        """
        start_state = copy.deepcopy(self.grid)
        remaining_containers = copy.deepcopy(self.containers)

        # Priority queue with initial state
        open_set = []
        heapq.heappush(open_set, (0, start_state, [], remaining_containers))

        while open_set:
            cost, current_state, steps, remaining_containers = heapq.heappop(open_set)

            if self.is_goal_state(current_state, remaining_containers):
                return steps, current_state

            if remaining_containers:
                container = remaining_containers.pop(0)  # Get the next container to place
                neighbors = self.get_neighbors(current_state, container)

                for new_state, x, y in neighbors:
                    new_steps = steps + [(container.name, x, y)]
                    g = cost + 1  # Increment cost for each move
                    h = self.heuristic(new_state, remaining_containers)
                    heapq.heappush(open_set, (g + h, new_state, new_steps, remaining_containers))

        return None, None  # No solution found

# Example Usage
if __name__ == "__main__":
    # Initial ship grid (8x12), 'UNUSED' for empty slots
    grid = [["UNUSED" for _ in range(12)] for _ in range(8)]

    # Containers to be loaded
    containers = [
        Container(xPos=0, yPos=0, weight=200, name="C1", id=1),
        Container(xPos=0, yPos=0, weight=150, name="C2", id=2),
    ]

    # Manifest (tracking purposes only in this example)
    manifest = "manifest.txt"

    # Initialize A* loading process
    loader = AStarLoading(grid, containers, manifest)
    steps, final_state = loader.a_star()

    if steps:
        print("Steps to load containers:")
        for step in steps:
            print(step)
        print("\nFinal grid:")
        for row in final_state:
            print(row)
    else:
        print("No solution found.")