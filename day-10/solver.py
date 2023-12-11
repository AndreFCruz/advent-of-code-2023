import sys
from typing import Iterator
from itertools import product


class Graph:

    NODE_TYPES = {"|", "-", "L", "J", "7", "F"}

    def __init__(self, graph_matrix):
        self.graph = graph_matrix
        self.num_rows = len(self.graph)         # self.graph.shape[0]
        self.num_cols = len(self.graph[0])      # self.graph.shape[1]

    @property
    def num_nodes(self):
        return self.num_rows * self.num_cols

    def __getitem__(self, node_key: tuple):
        row, col = node_key
        return self.graph[row][col]

    def _is_valid_node(self, node) -> bool:
        row, col = node
        return 0 <= row < self.num_rows and 0 <= col < self.num_cols

    def _connects_to_start_node(self, node, start_node) -> bool:
        """Checks whether `node` connects to the start node at `start_node`."""
        return (
            self._is_valid_node(node)
            and start_node in list(self.get_neighbors(node))
        )

    def get_neighbors_start_node(self, start_node) -> Iterator[tuple]:
        """Go through all potential neighbors and check which connect to the start node."""
        row, col = start_node

        yield from (
            node
            for delta_row, delta_col in ((-1, 0), (1, 0), (0, -1), (0, 1))
            if self._connects_to_start_node(
                (node := (row + delta_row, col + delta_col)),
                start_node,
            )
        )

    def get_neighbors(self, node: tuple) -> Iterator[tuple]:
        """Get neighbors of a node.

        * | is a vertical pipe connecting north and south.
        * - is a horizontal pipe connecting east and west.
        * L is a 90-degree bend connecting north and east.
        * J is a 90-degree bend connecting north and west.
        * 7 is a 90-degree bend connecting south and west.
        * F is a 90-degree bend connecting south and east.
        * . is ground; there is no pipe in this tile.
        """
        row, col = node
        node_value = self[node]

        # Alternative reasoning for start node: all non-ground are neighbors
        if node_value == "S":
            yield from self.get_neighbors_start_node(node)
            return

        # Add NORTH neighbor
        if node_value in {"J", "L", "|"} and row >= 1:
            yield (row - 1, col)

        # Add SOUTH neighbor
        if node_value in {"7", "F", "|"} and row <= self.num_rows - 1:
            yield (row + 1, col)

        # Add WEST neighbor
        if node_value in {"-", "J", "7"} and col >= 1:
            yield (row, col - 1)

        # Add EAST neighbor
        if node_value in {"-", "L", "F"} and col <= self.num_cols - 1:
            yield (row, col + 1)

    def __iter__(self):
        """Iterate through the nodes of the graph."""
        yield from (
            (row, col) for col in range(self.num_cols)
            for row in range(self.num_rows)
        )


def dijkstra(graph: Graph, start: str, end: str = None):
    """Dijkstra's algorithm for finding the shortest path between two nodes in a graph.

    Parameters
    ----------
    graph : Graph
        A graph object.
    start : str
        The start node.
    end : str, optional
        The end node, by default None (will return distances to all nodes).

    Returns
    -------
    dict or tuple
        A dict of distances if no end node was provided, otherwise a tuple of
        the shortest distance and corresponding path.
    """

    # Store shortest distances and parent nodes
    distances = {}
    previous = {node: None for node in graph}

    # There's no native PQ implementation that allows for updating priorities...
    priority_queue = {start: 0}
    # > loop will iteratively move nodes from PQ to distances as they are visited

    # Loop through all reachable nodes
    while priority_queue:

        # Get the next closest unvisited node
        current_node = min(priority_queue, key=priority_queue.get)
        current_dist = priority_queue.pop(current_node)
        distances[current_node] = current_dist

        # Update the distances to its neighbors
        for neighbor in graph.get_neighbors(current_node):

            # If neighbor not already visited
            if neighbor not in distances:

                # Distance from `start` to `neighbor` via `current_node`
                new_distance = distances[current_node] + 1      # edges always have weight=1
                if new_distance < distances.get(neighbor, float('inf')):
                    distances[neighbor] = new_distance
                    previous[neighbor] = current_node

                    priority_queue[neighbor] = new_distance

    # If no end node was provided, return the distances
    if end is None:
        return distances

    # Otherwise, return the shortest distance and corresponding path
    path = []
    current_node = end
    while current_node is not None:
        path.append(current_node)
        current_node = previous[current_node]
    path.reverse()

    return distances[end], path


def parse_input(input_lines: list[str]):
    """Parse the input and construct the corresponding graph."""
    return Graph(input_lines)


def solve_part_one(graph: Graph) -> int:
    """Solve part one.
    """
    distances = dijkstra(
        graph,
        start=[node for node in graph if graph[node] == "S"][0],
    )
    print(distances)
    return max(distances.values())


def solve_part_two(problem_data) -> int:
    """Solve part two.
    """
    pass


def main():

    # # Read input
    # # > Load from stdin
    # input_lines = sys.stdin.readlines()

    # > Or load from file
    from pathlib import Path
    input_path = Path(__file__).parent / "input.txt"
    input_lines = [
        parsed_line
        for line in input_path.read_text().split("\n")
        if (parsed_line := line.strip())
    ]

    # Parse input
    problem_data = parse_input(input_lines)

    # Solve problem
    output = solve_part_one(problem_data)
    # output = solve_part_two(problem_data)

    # Write to stdout
    print(output, file=sys.stdout)


if __name__ == "__main__":
    main()
