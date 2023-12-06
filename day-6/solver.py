import re
import sys


def parse_input(input_lines: list[str]) -> list[tuple[set[int], set[int]]]:
    pass


def solve_part_two(input_obj: list[tuple[set, set]]) -> int:
    """Solve part two.
    """
    pass


def solve_part_one(input_obj: list[tuple[set, set]]) -> int:
    """Solve part one.
    """
    pass


def main():

    # # Read input
    # # > Load from stdin
    # input_lines = sys.stdin.readlines()

    # > Or load from file
    from pathlib import Path
    input_path = Path(__file__).parent / "example1.txt"
    input_lines = [
        line.strip() for line in input_path.read_text().split("\n")
    ]

    # Parse input
    input_obj = parse_input(input_lines)

    # Solve problem
    output = solve_part_one(input_obj)
    # output = solve_part_two(input_obj)

    # Write to stdout
    print(output, file=sys.stdout)


if __name__ == "__main__":
    main()
