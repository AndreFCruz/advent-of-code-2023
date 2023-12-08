import re
import sys
import math
import operator
from functools import reduce


# A, K, Q, J, T, 9, 8, 7, 6, 5, 4, 3, or 2
CARD_STRENGTH_ORDER = "23456789TJQKA"


def parse_input(input_lines: list[str]) -> list[tuple[str, int]]:
    line_regex = re.compile(r"(?P<hand>\w+) (?P<bid>\d+)")
    return [
        (match["hand"], int(match["bid"]))
        for line in input_lines
        if (match := line_regex.match(line))
    ]


def solve_part_one(problem_data) -> int:
    """Solve part one.
    """

    # Sort hands by strength
    sorted_hands = sorted(
        problem_data,
        key=lambda line: score_hand_strength(line[0]),
        reverse=False,
    )

    # Return sum of winnings
    return sum(
        (1 + rank) * bid
        for rank, (_hand, bid) in enumerate(sorted_hands)
    )


def solve_part_two(problem_data) -> int:
    """Solve part two.
    """
    pass


def score_hand_strength(hand: str) -> int:
    """Score the strength of a hand.
    """
    numeric_base = len(CARD_STRENGTH_ORDER)
    cards_in_hand = len(hand)

    def score_cards(hand: str) -> int:
        # Base case
        if len(hand) == 1:
            return CARD_STRENGTH_ORDER.index(hand)
        
        # Count the last card and sum the rest
        return (
            CARD_STRENGTH_ORDER.index(hand[-1])
            + numeric_base * score_cards(hand[:-1])
        )

    # Count card occurrences
    card_counts = {card: hand.count(card) for card in hand}
    
    # Comparison key for card scores (ignoring hand type)
    score = score_cards(hand)

    # Find hand type
    # 1. Five of a kind
    if len(card_counts) == 1:
        return numeric_base ** (cards_in_hand + 7) + score

    # 2. Four of a kind
    elif len(card_counts) == 2 and 4 in card_counts.values():
        return numeric_base ** (cards_in_hand + 6) + score

    # 3. Full house
    elif len(card_counts) == 2 and 3 in card_counts.values():
        return numeric_base ** (cards_in_hand + 5) + score

    # 4. Three of a kind
    elif 3 in card_counts.values():
        return numeric_base ** (cards_in_hand + 4) + score

    # 5. Two pairs
    elif len(card_counts) == 3 and 2 in card_counts.values():
        return numeric_base ** (cards_in_hand + 3) + score

    # 6. One pair
    elif len(card_counts) == 4 and 2 in card_counts.values():
        return numeric_base ** (cards_in_hand + 2) + score

    # 7. High card
    elif len(card_counts) == 5:
        return score

    else:
        raise ValueError("Unknown hand type")


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
