import re
import sys
import math
import operator
from dataclasses import dataclass
from functools import reduce


EPSILON = 1e-6


@dataclass
class BoatRaces:
    times: list
    distances: list

    def get_time_distance_pairs(self):
        return zip(self.times, self.distances)


def parse_input(input_lines: list[str]) -> BoatRaces:
    numbers_regex = re.compile(r"(?P<number>\d+)")

    times = map(int, numbers_regex.findall(input_lines[0]))
    distances = map(int, numbers_regex.findall(input_lines[1]))
    return BoatRaces(times, distances)


def solve_quadratic_equation(a: float, b: float, c: float) -> tuple[float, float]:
    """Solve the quadratic equation `a*x**2 + b*x + c = 0`.
    """
    return (
        (-b + (b ** 2 - 4 * a * c) ** (1/2)) / (2 * a),
        (-b - (b ** 2 - 4 * a * c) ** (1/2)) / (2 * a),
    )


def num_integers_between(a: float, b: float) -> int:
    """Return the number of integers between `a` and `b`.
    """
    if a > b:
        a, b = b, a
    return math.ceil(b - EPSILON) - math.ceil(a + EPSILON)


def solve_part_one(boat_races: BoatRaces) -> int:
    """Solve part one.

    Solve the equation:
        v(t - v) > d,
    where v is the velocity and the amount of time the button was pressed,
    t is the total time the race lasts,
    and d is the current record distance.

    The standard form equality is:
        -v**2 + t*v - d = 0.

    Solving the equality for `v` will yield two solutions, the solution to part
    one is the number of integers between the two `v` solutions.
    """
    solutions_for_v = [
        solve_quadratic_equation(a=-1, b=t, c=-d)
        for t, d in boat_races.get_time_distance_pairs()
    ]

    return reduce(
        operator.mul,
        [
            num_integers_between(solutions[0], solutions[1])
            for solutions in solutions_for_v
        ],
    )


def solve_part_two(boat_races: BoatRaces) -> int:
    """Solve part two.
    """
    time = int("".join(str(t) for t in boat_races.times))
    dist = int("".join(str(t) for t in boat_races.distances))

    return num_integers_between(
        *solve_quadratic_equation(a=-1, b=time, c=-dist)
    )


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
    input_obj = parse_input(input_lines)

    # Solve problem
    # output = solve_part_one(input_obj)
    output = solve_part_two(input_obj)

    # Write to stdout
    print(output, file=sys.stdout)


if __name__ == "__main__":
    main()
