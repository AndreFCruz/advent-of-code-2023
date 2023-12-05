import re
import sys
from typing import ClassVar
from dataclasses import dataclass


class RangeMap:
    def __init__(self, mappings: list[tuple[int, int, int]]):

        self.mappings = sorted(
            mappings,
            key=lambda tup: tup[1],     # sort by source start
        )

    def get_dst(self, src: int) -> int:

        # Iterate through the mappings (sorted by source start)
        for dst_start, src_start, range_len in self.mappings:
            if src_start <= src <= src_start + range_len:
                return src + (dst_start - src_start)

        # By default (if no particular mapping is provided), return self
        return src


@dataclass
class Almanac:
    seeds: list[int]
    seed_to_soil: RangeMap
    soil_to_fertilizer: RangeMap
    fertilizer_to_water: RangeMap
    water_to_light: RangeMap
    light_to_temperature: RangeMap
    temperature_to_humidity: RangeMap
    humidity_to_location: RangeMap

    # Names of the map variables in the correct order
    map_sequence_names: ClassVar[list] = [
        "seed_to_soil",
        "soil_to_fertilizer",
        "fertilizer_to_water",
        "water_to_light",
        "light_to_temperature",
        "temperature_to_humidity",
        "humidity_to_location",
    ]

    def get_seed_location(self, seed: int) -> int:
        """Traverses all maps in the correct order to find the location of the given seed.
        """

        current_val = seed
        for map_name in self.map_sequence_names:
            current_val = getattr(self, map_name).get_dst(current_val)

        return current_val

    def __post_init__(self):
        """Generate seed range needed for part two.
        """
        self.seed_range = [
            (self.seeds[i], self.seeds[i] + self.seeds[i + 1])
            for i in range(len(self.seeds) - 1)
        ]


def parse_input(input_lines: list[str]) -> Almanac:
    """Parses the input lines into a data structure."""

    # Parse seeds
    seed_regex = re.compile(r"^seeds: (?P<content>.*)$")
    seeds = [
        int(elem)
        for elem in seed_regex.fullmatch(input_lines[0].strip())["content"].split(" ")
    ]

    # Parse all maps
    map_name_regex = re.compile(r"^((?P<name>\w+[-]to[-]\w+) map:)")
    map_line_regex = re.compile(r"^(?P<dst>\d+)\s+(?P<src>\d+)\s+(?P<len>\d+)")

    line_idx = 1
    range_maps: [str, RangeMap] = dict()
    while line_idx < len(input_lines):

        # Match map start
        if (name_match := map_name_regex.match(input_lines[line_idx])):

            line_idx += 1
            curr_name = name_match["name"].replace("-", "_")
            curr_mappings = list()

            while (content_match := map_line_regex.match(input_lines[line_idx])):
                curr_mappings.append(
                    tuple(map(int, (content_match["dst"], content_match["src"], content_match["len"])))
                )
                line_idx += 1

            range_maps[curr_name] = RangeMap(mappings=curr_mappings)

        else:
            line_idx += 1

    return Almanac(
        seeds=seeds,
        **range_maps,
    )


def solve_part_two(almanac: Almanac) -> int:
    """Solve part two.
    """
    pass


def solve_part_one(almanac: Almanac) -> int:
    """Solve part one: sum up the score of all cards.
    """
    return min(
        almanac.get_seed_location(seed)
        for seed in almanac.seeds
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
    almanac = parse_input(input_lines)

    # Solve problem
    output = solve_part_one(almanac)
    # output = solve_part_two(almanac)

    # Write to stdout
    print(output, file=sys.stdout)


if __name__ == "__main__":
    main()
