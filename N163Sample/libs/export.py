import numpy as np
from numpy.typing import NDArray
from .define import Property

color_counter = 0
C = 512 / 40


def next_rainbow_color():
    global color_counter
    color_counter += 1
    # [R       G       B      )
    # [0   20  40  60  80  100)
    cc = color_counter % 100  # [0, 99]
    r = int(max(0, min(255, 512 - abs(0 - cc) * C)))
    g = int(max(0, min(255, 512 - abs(40 - cc) * C)))
    b = int(max(0, min(255, 512 - abs(80 - cc) * C)))
    return f"{r:02x}{g:02x}{b:02x}"


def generate_n163_instrument(
    name: str,
    folder_name: str,
    volume: NDArray[np.uint8],
    wave: NDArray[np.uint8],
    wave_size: int,
    wave_count: int,
):
    return Property(
        1,
        "Instrument",
        {
            "Name": name,
            "Color": next_rainbow_color(),
            "Expansion": "N163",
            "N163WavePreset": "Custom",
            "N163WaveSize": str(wave_size),
            "N163WavePos": "0",
            "N163WaveCount": str(wave_count),
            "Folder": folder_name,
        },
        children=[
            Property(
                2,
                "Envelope",
                {
                    "Type": "N163Wave",
                    "Length": str(wave_size * wave_count),
                    "Values": ",".join(map(str, wave)),
                },
                children=[],
            ),
            Property(
                2,
                "Envelope",
                {
                    "Type": "Volume",
                    "Length": str(wave_count),
                    "Values": ",".join(map(str, volume)),
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


def generate_note(
    instrument: Property,
    note: str,
    time: int,
    duration: int,
    first_fine_pitch: int | None = None,
):
    args = {
        "Time": str(time),
        "Value": note,
        "Duration": str(duration),
        "Instrument": instrument.includes["Name"],
        "PhaseReset": "1",
    }
    if first_fine_pitch:
        args["FinePitch"] = str(first_fine_pitch)
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


def collect_waves(
    volumes: NDArray[np.uint8],
    waves: list[NDArray[np.uint8]],
    base_note: str,
    first_fine_pitch: int = 0,
    wave_size: int = 240,
    wave_count: int = 4,
    pattern_length: int = 160,
):
    instrument_counter = 0
    pattern_counter = 0
    instruments: list[Property] = []
    patterns: list[Property] = []
    pattern_instances: list[Property] = []
    current_pattern, pinstance = generate_pattern(pattern_counter)
    PATTERN_MAX_NOTES = pattern_length // wave_count
    patterns.append(current_pattern)
    pattern_instances.append(pinstance)
    first = True
    for i in range(0, len(volumes), wave_count):
        wave = merge(waves[i:i+wave_count])
        volume = volumes[i:i+wave_count]
        instrument_name = f"Wave {instrument_counter}"
        folder_name = f"WaveFolder {instrument_counter // 100}"
        instrument = generate_n163_instrument(
            instrument_name, folder_name, volume, wave, wave_size, wave_count
        )
        instruments.append(instrument)
        now_time = instrument_counter % PATTERN_MAX_NOTES * wave_count
        if first:
            current_pattern.children.append(
                generate_note(
                    instrument, base_note, now_time, wave_count, first_fine_pitch
                )
            )
            first = False
        else:
            current_pattern.children.append(
                generate_note(instrument, base_note, now_time, wave_count)
            )
        for delta in range(wave_count - 1):
            current_pattern.children.append(generate_phasereset(now_time + delta + 1))
        instrument_counter += 1
        if instrument_counter % PATTERN_MAX_NOTES == 0:
            pattern_counter += 1
            current_pattern, pinstance = generate_pattern(pattern_counter)
            patterns.append(current_pattern)
            pattern_instances.append(pinstance)
    return instruments, patterns, pattern_instances

def merge(arrs: list[NDArray[np.uint8]]) -> NDArray[np.uint8]:
    return np.concatenate(arrs)