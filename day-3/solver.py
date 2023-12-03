import re
import sys
import operator
from functools import reduce



def solve_part_one(input_lines: list[str]) -> int:
    """Solve part one.
    
    Scan the input lines and, for each number, check whether it's contacting any
    symbol. Finally sum up all numbers that are contacting any symbol.

    Parameters
    ----------
    input_lines : list[str]
        Input lines.
    
    Returns
    -------
    sum : int
        The sum of all numbers fulfilling the constraint.
    """
    line_regex = re.compile(r"(\d+)")

    return sum(
        int(num_match[0])
        for line_idx, line in enumerate(input_lines)
        for num_match in line_regex.finditer(line)
        if any_symbol_contacting_number_at(
            input_lines,
            row=line_idx,
            col=num_match.start(),
            num_digits=num_match.end() - num_match.start(),
        )
    )


def any_symbol_contacting_number_at(
        input_lines: list[str],
        row: int,
        col: int,
        num_digits: int,
    ) -> bool:
    """Checks whether the number at the given position is in contact with any
    symbol.
    """
    return any(
        is_symbol(char)
        for line in input_lines[max(0, row - 1): min(len(input_lines), row + 2)]
        for char in line[max(0, col-1): min(len(line), col + num_digits + 1)]
    )


def is_symbol(char: str):
    return not char.isdigit() and char != '.'


def main():

    # # Read input
    # # > Load from stdin
    # input_lines = sys.stdin.readlines()

    # > Or load from file
    from pathlib import Path
    input_path = Path(__file__).parent / "input.txt"
    input_lines = [
        l.strip() for l in input_path.read_text().split("\n")
    ]
    print(set(ch for line in input_lines for ch in line))

    # Solve problem
    output = solve_part_one(input_lines)

    # Write to stdout
    print(output, file=sys.stdout)


if __name__ == "__main__":
    main()
