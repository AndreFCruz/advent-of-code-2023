import re
import sys


def parse_input(input_lines: list[str]):
    return [parse_numbers(line) for line in input_lines if line]


def parse_numbers(line: str) -> list[int]:
    numbers_regex = re.compile(r"[-]?\d+")
    return [int(num) for num in numbers_regex.findall(line)]


def solve_part_one(problem_data) -> int:
    """Solve part one.
    """
    return sum(
        extrapolate_value_from_history(history)
        for history in problem_data
    )


def extrapolate_value_from_history(history: list[int]) -> int:

    solution_lines = [history]

    # Construct pyramid lines
    while True:
        next_line = differences_between_adjacent_numbers(solution_lines[-1])
        solution_lines.append(next_line)

        # Stop if the next line is all zeros
        if set(next_line) == {0}: break

    # Reconstruct all extrapolated values and return the final extrapolated value
    for idx in range(len(solution_lines) - 2, -1, -1):
        extrapolated_val = solution_lines[idx][-1] + solution_lines[idx + 1][-1]
        solution_lines[idx].append(extrapolated_val)
    
    print(history[:5], solution_lines[0][-1])
    return solution_lines[0][-1]


def differences_between_adjacent_numbers(numbers: list[int]) -> list[int]:
    return [
        numbers[i + 1] - numbers[i]
        for i in range(len(numbers) - 1)
    ]


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
