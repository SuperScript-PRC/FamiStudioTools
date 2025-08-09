from .define import Note, Effect, NoteType, NOTE_PITCH

def parse_order_row(row: str):
    index, *columns_raw = row.split("|")

def parse_order_row_single_column(index: int, column: str):
    values = column.strip().split(" ")
    valen = len(values)
    if valen < 0:
        raise ValueError("Invalid order row: empty")
    note_type, note_pitch, note_base = parse_note(values[0])
    note = Note(note_type, index)
    if note_type == NoteType.NOTE:
        note.note_base = note_base
        note.note = note_pitch
    if valen > 1:
        note.instrument_index = parse_instrument_index(values[1])
    if valen > 2:
        note.volume = parse_volume(values[2])
    if valen > 3:
        note.effects = parse_effects(values[3:])
    return note


def parse_note(note: str):
    if note == "...":
        return NoteType.EMPTY, 0, 0
    elif note == "OFF":
        return NoteType.OFF, 0, 0
    else:
        note_pitch = NOTE_PITCH[note[:2].strip("-")]
        note_base = int(note[2])
        return NoteType.NOTE, note_pitch, note_base
    
def parse_volume(volume: str):
    if volume == "...":
        return 0
    else:
        return int(volume, 16)
    
def parse_instrument_index(instrument: str):
    return int(instrument, 16)

def parse_effects(effects_strs: list[str]):
    effects: dict[Effect, int] = {}
    for effect_str in effects_strs:
        if len(effect_str) != 4:
            raise ValueError(f"Effect string not valid: {effect_str}")
        if effect_str == "....":
            continue
        effect_type = int(effect_str[:2], 16)
        effect_value = int(effect_str[2:], 16)
        effects[Effect(effect_type)] = effect_value
    return effects