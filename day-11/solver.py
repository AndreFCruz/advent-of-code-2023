import sys


def parse_input(input_lines: list[str]):
    pass


def solve_part_one(problem_data) -> int:
    """Solve part one.
    """
    pass


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
    input_path = Path(__file__).parent / "example1.txt"
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
