import numpy as np
from numpy.typing import NDArray
from .define import Property


def generate_n163_instrument(name: str, wave: NDArray[np.uint8]):
    return Property(
        1,
        "Instrument",
        {
            "Name": name,
            "Color": "0000ff",
            "Expansion": "N163",
            "N163WavePreset": "Custom",
            "N163WaveSize": "240",
            "N163WavePos": "0",
            "N163WaveCount": "4",
        },
        children=[
            Property(
                2,
                "Envelope",
                {
                    "Type": "N163Wave",
                    "Length": "960",
                    "Values": ",".join(str(i) for i in wave),
                },
                children=[],
            ),
            Property(
                2,
                "Envelope",
                {"Type": "Repeat", "Length": "4", "Values": "1,1,1,1"},
                children=[],
            ),
        ],
    )


def generate_note(instrument: Property, time: int, first: bool):
    args = {
        "Time": str(time),
        "Value": "A#4",
        "Duration": "4",
        "Instrument": instrument.includes["Name"],
        "PhaseReset": "1",
    }
    if first:
        args["FinePitch"] = "-13"
    return Property(
        4,
        "Note",
        args,
        children=[],
    )


def generate_phasereset(time: int):
    return Property(
        4,
        "Note",
        {"Time": str(time), "PhaseReset": "1"},
        children=[],
    )


def generate_pattern(pattern_time: int):
    pattern_name = f"WavePattern {pattern_time + 1}"
    return (
        Property(
            3,
            "Pattern",
            {
                "Name": pattern_name,
                "Color": "0000ff",
            },
            children=[],
        ),
        Property(
            3,
            "PatternInstance",
            {"Time": str(pattern_time), "Pattern": pattern_name},
            children=[],
        ),
    )


def collect_waves(ws: list[NDArray[np.uint8]]):
    instrument_counter = 0
    pattern_counter = 0
    instruments: list[Property] = []
    patterns: list[Property] = []
    pattern_instances: list[Property] = []
    current_pattern, pinstance = generate_pattern(pattern_counter)
    PATTERN_MAX_NOTES = 40
    patterns.append(current_pattern)
    pattern_instances.append(pinstance)
    first = True
    for w in ws:
        instrument_name = f"Wave {instrument_counter}"
        instrument = generate_n163_instrument(instrument_name, w)
        instruments.append(instrument)
        now_time = instrument_counter % PATTERN_MAX_NOTES * 4
        current_pattern.children.append(generate_note(instrument, now_time, first))
        first = False
        for delta in range(3):
            current_pattern.children.append(generate_phasereset(now_time + delta + 1))
        instrument_counter += 1
        if instrument_counter % PATTERN_MAX_NOTES == 0:
            pattern_counter += 1
            current_pattern, pinstance = generate_pattern(pattern_counter)
            patterns.append(current_pattern)
            pattern_instances.append(pinstance)
    return instruments, patterns, pattern_instances
