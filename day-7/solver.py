import re
import sys
import math
import operator
from functools import reduce


### Regular card strength order
CARD_STRENGTH_ORDER_PART_ONE = "23456789TJQKA"

### Card strength order for part two where Js are the weakest
CARD_STRENGTH_ORDER_PART_TWO = "J23456789TQKA"

### Numeric base used for scoring cards
NUMERIC_BASE = len(CARD_STRENGTH_ORDER_PART_ONE)


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
    global CARD_STRENGTH_ORDER
    CARD_STRENGTH_ORDER = CARD_STRENGTH_ORDER_PART_ONE

    return compute_sum_of_winnings(problem_data)


def solve_part_two(problem_data) -> int:
    """Solve part two.
    """
    global CARD_STRENGTH_ORDER
    CARD_STRENGTH_ORDER = CARD_STRENGTH_ORDER_PART_TWO

    return compute_sum_of_winnings(problem_data, jokers=True)


def compute_sum_of_winnings(problem_data: list, jokers: bool = False) -> int:
    """Compute sum of winnings from the given problem data.

    Parameters
    ----------
    problem_data : list
        A list of tuples of the form (hand, bid).
    jokers : bool, optional
        Whether to use J cards as jokers, by default False.

    Returns
    -------
    sum_of_winnings : int
        A sum of hand_bid * hand_rank over all hands.
    """

    # Sort hands by strength
    sorted_hands = sorted(
        problem_data,
        key=lambda line: score_hand_strength(line[0], jokers=jokers),
        reverse=False,
    )

    # Return sum of winnings
    return sum(
        (1 + rank) * bid
        for rank, (_hand, bid) in enumerate(sorted_hands)
    )


def score_cards(hand: str) -> int:
    """Score the cards in a hand, independently of hand type.
    """
    # Base case
    if len(hand) == 1:
        return CARD_STRENGTH_ORDER.index(hand)
    
    # Count the last card and sum the rest
    return (
        CARD_STRENGTH_ORDER.index(hand[-1])
        + NUMERIC_BASE * score_cards(hand[:-1])
    )


def score_hand_strength(hand: str, jokers: bool = False) -> int:
    """Score the strength of a hand.
    """
    cards_in_hand = len(hand)

    # Count card occurrences
    card_counts = {card: hand.count(card) for card in hand}

    # Add joker counts to the most often card
    if jokers and "J" in card_counts and len(card_counts) > 1:
        j_count = card_counts.pop("J", 0)
        card_counts[max(card_counts, key=card_counts.get)] += j_count

    # Comparison key for card scores (ignoring hand type)
    score = score_cards(hand)

    # Find hand type
    # 1. Five of a kind
    if len(card_counts) == 1:
        return NUMERIC_BASE ** (cards_in_hand + 7) + score

    # 2. Four of a kind
    elif len(card_counts) == 2 and 4 in card_counts.values():
        return NUMERIC_BASE ** (cards_in_hand + 6) + score

    # 3. Full house
    elif len(card_counts) == 2 and 3 in card_counts.values():
        return NUMERIC_BASE ** (cards_in_hand + 5) + score

    # 4. Three of a kind
    elif 3 in card_counts.values():
        return NUMERIC_BASE ** (cards_in_hand + 4) + score

    # 5. Two pairs
    elif len(card_counts) == 3 and 2 in card_counts.values():
        return NUMERIC_BASE ** (cards_in_hand + 3) + score

    # 6. One pair
    elif len(card_counts) == 4 and 2 in card_counts.values():
        return NUMERIC_BASE ** (cards_in_hand + 2) + score

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
    # output = solve_part_one(problem_data)
    output = solve_part_two(problem_data)

    # Write to stdout
    print(output, file=sys.stdout)


if __name__ == "__main__":
    main()
