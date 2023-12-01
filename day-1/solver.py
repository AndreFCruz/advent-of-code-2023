import sys


# Digit finder for Part 1
def get_first_digit(line: str) -> int:
    """Return the first digit character in the input."""
    for ch in line:
        if ch.isdigit():
            return int(ch)

    raise ValueError(f"No digits found in string '{line}'")


def solve_part_one(input: list[str]) -> int:
    return sum(
        get_first_digit(line) * 10 + get_first_digit(line[::-1])
        for line in input
    )


def get_first_and_last_digit(line: str) -> tuple[int, int]:
    """Return the first and last digit that show up in `line`.

    Digits can be spelled out ('one' to 'nine') or in characters ('1'-'9').
    """
    spelled_digits = [
        "zero",
        "one", "two", "three", "four", "five",
        "six", "seven", "eight", "nine",
    ]
    spelled_digits_to_int = dict(zip(spelled_digits, range(10)))

    first_idx, first_digit = len(line), None
    last_idx, last_digit = -1, None
    for digit_spelled, digit_char in spelled_digits_to_int.items():

        # Check first occurrence
        curr_first_idx_spelled = line.find(digit_spelled)
        curr_first_idx_char = line.find(str(digit_char))

        if curr_first_idx_spelled > -1 and curr_first_idx_spelled == min(first_idx, curr_first_idx_spelled):
            first_idx = curr_first_idx_spelled
            first_digit = digit_char

        if curr_first_idx_char > -1 and curr_first_idx_char == min(first_idx, curr_first_idx_char):
            first_idx = curr_first_idx_char
            first_digit = digit_char

        # Check last occurrence
        curr_last_idx_spelled = line.rfind(digit_spelled)
        curr_last_idx_char = line.rfind(str(digit_char))

        if curr_last_idx_spelled == max(last_idx, curr_last_idx_spelled):
            last_idx = curr_last_idx_spelled
            last_digit = digit_char

        if curr_last_idx_char == max(last_idx, curr_last_idx_char):
            last_idx = curr_last_idx_char
            last_digit = digit_char

    if first_digit is None:
        raise ValueError(f"No digit found in string '{line}'")
    else:
        return (first_digit, last_digit)


def solve_part_two(input: list[str]) -> int:
    """Return the sum of the first and last digits found in `input`.

    """
    parse_digit_tuple = lambda frst, scnd: frst * 10 + scnd

    return sum(
        parse_digit_tuple(*get_first_and_last_digit(line))
        for line in input
    )


if __name__ == "__main__":

    # # Solve part 1
    # print(solve_part_one(sys.stdin.readlines()))

    # Solve part 2
    print(solve_part_two(sys.stdin.readlines()))
