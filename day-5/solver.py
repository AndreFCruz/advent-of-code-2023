import re
import sys
from typing import ClassVar
from dataclasses import dataclass


# A very large number representing infinity
INFTY = 1e20


def range_intersection(rangeA: tuple, rangeB: tuple) -> tuple | bool:
    rangeA_start, rangeA_end = rangeA
    rangeB_start, rangeB_end = rangeB
    assert rangeA_end >= rangeA_start and rangeB_end >= rangeB_start

    if rangeA_end < rangeB_start or rangeB_end < rangeA_start:
        return False

    else:
        return (max(rangeA_start, rangeB_start), min(rangeA_end, rangeB_end))


class RangeMap:
    def __init__(self, mappings: list[tuple[int, int, int]], with_identity_maps: bool = False):

        self.mappings = sorted(
            mappings,
            key=lambda tup: tup[1],     # sort by source start
        )

        if with_identity_maps:
            self.add_self_identity_mappings()

    def add_self_identity_mappings(self):
        # Added for part two
        self.mappings = self.fill_identity_mappings(self.mappings)

    @staticmethod
    def fill_identity_mappings(mappings, start_at: int = None, end_at: int = None) -> list:
        """Add identity maps for missing ranges in the given mappings.
        """

        start_at = start_at or mappings[0][1]       # first mapped source
        end_at = end_at or mappings[-1][1]          # last mapped source

        # > add extra tuples with identity mappings; i.e., src->src
        curr_pos = start_at
        new_identity_maps = []
        for (dst, src, length) in mappings:
            if curr_pos < src:
                new_identity_maps.append((curr_pos, curr_pos, src - curr_pos))

            # Place `curr_pos` at the end of the current mapping
            curr_pos = src + length

        # Add whatever range is left after the last mapping
        if end_at > curr_pos:
            new_identity_maps.append((curr_pos, curr_pos, end_at - curr_pos))

        # Add the new identity maps and re-sort list
        mappings.extend(new_identity_maps)
        return sorted(
            mappings,
            key=lambda tup: tup[1],     # sort by source start
        )

    def get_dst(self, src: int) -> int:

        # Iterate through the mappings (sorted by source start)
        for dst_start, src_start, range_len in self.mappings:

            # NOTE: mapping range is closed on the left and open on the right!
            # range: [src_start, src_start + range_len[
            if src_start <= src < src_start + range_len:
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
            for i in range(0, len(self.seeds) - 1, 2)
        ]

    def compress_seed_to_loc_maps(self) -> RangeMap:
        """Compress all range maps into a single mapping."""
        return RangeMap(
            mappings=[
                mp
                for seed_start, seed_end in self.seed_range
                for mp in self._get_mappings_for_range(
                    seed_start, seed_end,
                    range_attr_name=self.map_sequence_names[0],
                )
            ]
        )

    def _get_mappings_for_range(
            self,
            range_start: int,
            range_end: int,
            range_attr_name: str,
        ) -> list[tuple]:

        curr_range_map = getattr(self, range_attr_name)
        mappings = list()

        for (_curr_dst, curr_src, curr_len) in curr_range_map.mappings:

            intersect = range_intersection(
                (range_start, range_end),
                (curr_src, curr_src + curr_len),
            )

            # There's some intersection with the current mapping
            if intersect is not False:
                i_start, i_end = intersect

                mappings.append(
                    (
                        curr_range_map.get_dst(i_start),        # destination
                        i_start,                                # source
                        i_end - i_start,                        # range length
                    )
                )

                # Check early loop break
                if i_end == range_end:
                    break

        # Add self mappings for whichever range portions were not mapped
        mappings = RangeMap.fill_identity_mappings(
            mappings,
            start_at=range_start,
            end_at=range_end,
        )

        # Base case
        if range_attr_name == self.map_sequence_names[-1]:
            return mappings

        # else: Recursive case
        next_range_idx = self.map_sequence_names.index(range_attr_name) + 1
        next_range_name = self.map_sequence_names[next_range_idx]

        # TODO: yield instead of returning?
        return [
            (
                new_dst,
                src + new_src - dst,
                new_length,
            )
            for (dst, src, length) in mappings
            for (new_dst, new_src, new_length) in self._get_mappings_for_range(
                range_start=dst,
                range_end=dst + length,
                range_attr_name=next_range_name,
            )
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

    # Compress all mappings into a single src->dst RangeMap for all seed ranges
    seed_mappings = almanac.compress_seed_to_loc_maps()

    lowest_loc = None
    for (dst, _, _) in seed_mappings.mappings:

        if lowest_loc is None or lowest_loc > dst:
            lowest_loc = dst

    return lowest_loc


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
    # output = solve_part_one(almanac)
    output = solve_part_two(almanac)

    # Write to stdout
    print(output, file=sys.stdout)


if __name__ == "__main__":
    main()
