from .extractor import WaveTable
from .constructor import N163Instrument


def convert_to_n163_format(height: int, values: list[int]) -> list[int]:
    if (length := len(values)) > 240:
        raise ValueError(f"Wavetable is too long for N163: {length}")
    return [round(value / (height - 1) * 15) for value in values]


def convert_to_n163_instrument(ins_name: str, wavetable: WaveTable) -> N163Instrument:
    return N163Instrument(
        ins_name,
        wavetable.width,
        convert_to_n163_format(wavetable.height, wavetable.values),
    )
