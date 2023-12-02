import re
import sys
import operator
from functools import reduce


COLORS = ["red", "green", "blue"]

MAX_DIE_PART_1 = {
    "red": 12,
    "green": 13,
    "blue": 14,
}


def parse_input(input_lines: list[str]) -> dict[int, list[dict[str, int]]]:
    """Parse input lines into an organized data structure."""

    line_regex = re.compile(r"^Game (?P<id>\d+): (?P<content>.*)$")
    die_set_regex = re.compile(r"(?P<num>\d+) (?P<color>blue|green|red)")

    return {
        int(line_match["id"]): [
            {
                set_match["color"]: int(set_match["num"])
                for set_match in die_set_regex.finditer(game_set)
            }
            for game_set in line_match["content"].split(";")
        ]
        for line in input_lines
        if (line_match := line_regex.fullmatch(line.strip()))
    }


def solve_part_one(games: dict[int, list[dict[str, int]]], max_die: dict[str, int]) -> int:
    """Solves part one.

    Parameters
    ----------
    games : dict[int, list[dict[str, int]]]
        A dictionary whose keys are game IDs, and values are lists of revealed
        sets of die.

        games[game_id][idx_of_set_in_game][color] = number of die of this color on this set of this game

    max_die : dict[str, int]
        The maximum number of die allowed per color.
        Will sum up the IDs of the games that fulfill this constraint.

    Returns
    -------
    sum : int
        The sum over all game IDs that would be possible using only `max_die`.
    """
    def check_game_set(game_set: dict[str, int]) -> bool:
        """Checks whether this `game_set` would be possible with only `max_die`"""
        return all(
            game_set.get(color, 0) <= max_die.get(color, 0)
            for color in game_set.keys() | max_die.keys()
        )

    return sum(
        game_id
        for game_id, game_content in games.items()
        if all(check_game_set(game_set) for game_set in game_content)
    )


def solve_part_two(games: dict[int, list[dict[str, int]]]) -> int:
    """Solve part two.

    Parameters
    ----------
    games : dict[int, list[dict[str, int]]]
        The series of games played.

    Returns
    -------
    sum : int
        The sum over the power of each game's min cube set.
    """

    def get_min_die_for_game(game_sets: list[dict[str, int]]) -> dict:
        """Get the minimum set of die that would be required to run the `game_sets`."""
        return {
            color: max(gset.get(color, 0) for gset in game_sets)
            for color in COLORS
        }

    return sum(
        reduce(
            operator.mul,
            get_min_die_for_game(game_).values()
        )
        for game_ in games.values()
    )


if __name__ == "__main__":

    # Read input
    # > Load from stdin
    input_lines = sys.stdin.readlines()

    # # > Or load from file
    # from pathlib import Path
    # input_path = Path(__file__).parent / "example1.txt"
    # input_lines = input_path.read_text().split("\n")

    # Parse input
    games = parse_input(input_lines)

    # Solve problem
    # output = solve_part_one(games, max_die=MAX_DIE_PART_1)
    output = solve_part_two(games)

    # Write to stdout
    print(output, file=sys.stdout)
