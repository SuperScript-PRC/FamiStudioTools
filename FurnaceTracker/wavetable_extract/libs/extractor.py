import re
from dataclasses import dataclass


@dataclass
class WaveTable:
    height: int
    width: int
    values: list[int]


wavetable_rule = re.compile(
    r"- (?P<index>[0-9]+) \((?P<width>[0-9]+)x(?P<height>[0-9]+)\): (?P<values>[0-9 ]+)"
)


def extract_wavetables(content: str) -> list[WaveTable]:
    wavetables = []
    for i in wavetable_rule.finditer(content):
        index = int(i.group("index"))
        height = int(i.group("height"))
        width = int(i.group("width")) - 1
        values = [int(j) for j in i.group("values").split(" ")][:-1]
        if width != len(values):
            raise ValueError(f"{index}: wavetable length doesn't match size: {width} != {len(values)}: {values}")
        wavetables.append(
            WaveTable(
                height=height,
                width=width,
                values=values,
            )
        )
    return wavetables
