import re
import sys


def parse_input(input_lines: list[str]) -> list[tuple[set[int], set[int]]]:
    """Parses the input lines into a data structure."""

    line_regex = re.compile(r"Card\s+(\d+):\s+(?P<winners>.*)\s+[|]\s+(?P<have>.*)")
    numbers_regex = re.compile(r"\d+")

    return [
        (
            set(numbers_regex.findall(match["winners"])),
            set(numbers_regex.findall(match["have"])),
        )
        for line in input_lines
        if (match := line_regex.fullmatch(line))
    ]


def solve_part_two(card_list: list[tuple[set, set]]) -> int:
    """Solve part two.
    """
    return sum(
        score_card_part_two(card_list, idx)
        for idx in range(len(card_list))
    )


def score_card_part_two(
        card_list: list[tuple[set, set]],
        idx: int,
        cache: dict[int, int] = {},     # caching already scored cards
    ) -> int:
    """Score the card at position `idx` by recursively scoring cards from `idx`
    to `idx+n`, where n is the number of matches on the initial card.
    """
    # Check if function was called with an out of range index
    if idx >= len(card_list):
        return 0

    # If card has not been scored, score it and save the result
    if idx not in cache:
        curr_winners, curr_have = card_list[idx]
        num_matches = len(curr_winners & curr_have)

        # Score:
        # 1 for the current scratchcard,
        # plus the score of each subsequent scratchcard obtained (the next
        # `num_matches` cards)
        cache[idx] = 1 + sum(
            score_card_part_two(
                card_list,
                idx=idx + j,
            )
            for j in range(1, num_matches + 1)
        )

    return cache[idx]


def solve_part_one(card_list: list[tuple[set, set]]) -> int:
    """Solve part one: sum up the score of all cards.
    """
    return sum(
        score_card_part_one(card=c) for c in card_list
    )


def score_card_part_one(card: tuple[set, set]) -> int:
    """Score the card by 2^(matches - 1), or zero if no match is made.
    """
    winners, have = card
    num_matches = len(winners & have)
    return 2 ** (num_matches - 1) if num_matches > 0 else 0


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
    card_list = parse_input(input_lines)

    # Solve problem
    # output = solve_part_one(card_list)
    output = solve_part_two(card_list)

    # Write to stdout
    print(output, file=sys.stdout)


if __name__ == "__main__":
    main()
