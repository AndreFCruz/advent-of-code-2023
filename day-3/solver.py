import re
import sys
import operator
from functools import reduce
from itertools import product


def solve_part_two(input_lines: list[str]) -> int:
    """Solve part two.

    Scan each line for asterisk symbols, "*", and for each symbol check whether
    it's contacting exactly two numbers. Finally, sum up the product of all such
    two numbers.

    Parameters
    ----------
    input_lines : list[str]
        The input lines.

    Returns
    -------
    sum : int
        The sum of all products between numbers contacting the same "gear".
    """
    asterisk_regex = re.compile(r"[*]")

    return sum(
        reduce(operator.mul, number_pair)
        for line_idx, line in enumerate(input_lines)
        for match in asterisk_regex.finditer(line)
        if (
            number_pair := two_numbers_contacting_asterisk(
                input_lines,
                row=line_idx,
                col=match.start(),
            )
        )
    )


def two_numbers_contacting_asterisk(
        input_lines: list[str],
        row: int,
        col: int,
    ) -> bool:
    """Checks whether there are *exactly* two numbers contacting the given
    asterisk.
    """
    number_regex = re.compile(r"\d+")

    # NOTE: these matches should be pre-computed for all asterisks
    all_number_matches = {
        line_idx: set(list(number_regex.finditer(line)))
        for line_idx, line in enumerate(input_lines)
    }

    def get_number_match_at_pos(num_row, num_col) -> object:
        for m in all_number_matches[num_row]:
            if m.start() <= num_col and m.end() >= num_col:
                return m
        
        raise ValueError(f"Number not found at pos {(num_row, num_col)}")

    line_len = len(input_lines[row])
    adjacent_tiles = list(
        product(
            range(max(0, row-1), min(len(input_lines), row+2)),
            range(max(0, col-1), min(line_len, col+2))
        )
    )

    matches_contacting_asterisk = set()
    for adj_row, adj_col in adjacent_tiles:

        # Is there a digit at this position
        if input_lines[adj_row][adj_col].isdigit():
            m = get_number_match_at_pos(adj_row, adj_col)
            matches_contacting_asterisk |= {m}

    # If exactly two matches: return the number pair
    if len(matches_contacting_asterisk) == 2:
        return [int(m[0]) for m in matches_contacting_asterisk]
    else:
        return False


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

    # Solve problem
    # output = solve_part_one(input_lines)
    output = solve_part_two(input_lines)

    # Write to stdout
    print(output, file=sys.stdout)


if __name__ == "__main__":
    main()
