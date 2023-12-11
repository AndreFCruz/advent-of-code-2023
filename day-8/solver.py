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

    num_steps = 0
    curr_node = "AAA"
    dst_node = "ZZZ"
    curr_instr_idx = 0
    while curr_node != dst_node:
        instr = instructions[curr_instr_idx]
        curr_node = graph[curr_node][0 if instr == "L" else 1]
        num_steps += 1
        curr_instr_idx = (curr_instr_idx + 1) % len(instructions)
    
    return num_steps


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
        line.strip() for line in input_path.read_text().split("\n")
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
