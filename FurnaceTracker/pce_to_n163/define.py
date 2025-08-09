from dataclasses import dataclass, field
from enum import IntEnum

class NoteType(IntEnum):
    EMPTY = 0
    NOTE = 1
    OFF = 2

# note effects in furnace tracker (chip: PC Engine).
class Effect(IntEnum):
    Arpeggio = 0x00
    PitchSlideUp = 0x01
    PitchSlideDown = 0x02
    Portamento = 0x03
    Vibrato = 0x04
    VolumeSlide_vibrato = 0x05
    VolumeSlide_portamento = 0x06
    Tremolo = 0x07
    SetPanning = 0x08
    SetGroovePattern = 0x09
    VolumeSlide = 0x0A
    JumpToPattern = 0x0B
    Retrigger = 0x0C
    JumpToNextPattern = 0x0D
    SetSpeed = 0x0F
    SetWaveform = 0x10
    ToggleNoiseMode = 0x11
    SetupLFO = 0x12
    TogglePCMMode = 0x13
    SetPanning_left = 0x14
    SetPanning_right = 0x15

@dataclass
class Note:
    type: NoteType
    pattern_index: int | None = None
    note_base: int | None = None
    note: int | None = None
    instrument_index: int | None = None
    volume: int | None = None
    effects: dict[Effect, int] = field(default_factory=dict)

NOTE_PITCH = {
    "C": 0,
    "C#": 1,
    "D": 2,
    "D#": 3,
    "E": 4,
    "F": 5,
    "F#": 6,
    "G": 7,
    "G#": 8,
    "A": 9,
    "A#": 10,
    "B": 11,
}