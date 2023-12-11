import re
import sys
import math
import operator
from dataclasses import dataclass
from functools import reduce


def parse_input(input_lines: list[str]) -> tuple[str, dict[str, tuple[str, str]]]:
    left_right_instructions = input_lines[0].strip()

    graph = dict()
    node_regex_line = re.compile(r"(?P<src>\w+) = [(](?P<left>\w+), (?P<right>\w+)[)]")
    for line in input_lines[1:]:
        if (match := node_regex_line.match(line)) is not None:
            src = match.group("src")
            left = match.group("left")
            right = match.group("right")
            graph[src] = (left, right)

    return left_right_instructions, graph


def solve_part_one(problem_data) -> int:
    """Solve part one.
    """
    instructions, graph = problem_data

    DST_NODE = "ZZZ"
    curr_node = "AAA"
    num_steps = 0
    curr_instr_idx = 0
    while curr_node != DST_NODE:
        instr = instructions[curr_instr_idx]
        curr_node = graph[curr_node][0 if instr == "L" else 1]
        num_steps += 1
        curr_instr_idx = (curr_instr_idx + 1) % len(instructions)
    
    return num_steps


def solve_part_two(problem_data) -> int:
    """Solve part two.
    """
    def is_src_node(node: str):
        return node[-1] == "A"
    def is_dst_node(node: str):
        return node[-1] == "Z"
    
    instructions, graph = problem_data

    curr_nodes = [node for node in graph if is_src_node(node)]
    curr_instr_idx = 0
    num_steps = 0

    while not all(is_dst_node(node) for node in curr_nodes):
        for idx, node in enumerate(curr_nodes):
            instr = instructions[curr_instr_idx]
            curr_nodes[idx] = graph[node][0 if instr == "L" else 1]

        num_steps += 1
        curr_instr_idx = (curr_instr_idx + 1) % len(instructions)

    return num_steps


def main():

    # # Read input
    # # > Load from stdin
    # input_lines = sys.stdin.readlines()

    # > Or load from file
    from pathlib import Path
    input_path = Path(__file__).parent / "input.txt"
    input_lines = [
        line.strip() for line in input_path.read_text().split("\n")
    ]

    # Parse input
    problem_data = parse_input(input_lines)

    # Solve problem
    # output = solve_part_one(problem_data)
    output = solve_part_two(problem_data)

    # Write to stdout
    print(output, file=sys.stdout)


if __name__ == "__main__":
    main()
