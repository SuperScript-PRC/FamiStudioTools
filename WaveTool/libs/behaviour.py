from .define import Property
from .effect import chord, pwm, averange
from .utils import (
    cls,
    make_wavetable_print,
    wait_resp,
    get_wavetable_data,
    set_wavetable_data,
)


def operation(wtis: list[Property]):
    instrument_1 = select_wavetable_instrument(wtis).copy()
    match select_function():
        case "Chorus":
            repeat_speed = select_repeat_speed()
            new_instrument = op_make_chord(instrument_1, repeat_speed)
        case "Length/2":
            new_instrument = op_length_div_2(instrument_1)
        case "PWM":
            repeat_speed = select_repeat_speed()
            new_instrument = op_pwm(instrument_1, repeat_speed)
        case "Averange":
            repeat_speed = select_repeat_speed()
            new_instrument = op_averange(instrument_1, repeat_speed)
        case _:
            print("Not implemented.")
            return None
    print("Done.")
    return new_instrument


def op_make_chord(instrument: Property, repeat: int):
    instrument = instrument.copy()
    wave_size, _, wave_raw = get_wavetable_data(instrument)
    use_wave_count = 1024 // wave_size
    wave = chord(wave_raw, use_wave_count)
    set_wavetable_data(instrument, wave_size, use_wave_count, wave, repeat, loop=True)
    instrument.includes["Name"] += " (Chord)"
    return instrument

def op_length_div_2(instrument: Property):
    instrument = instrument.copy()
    wave_size, wave_count, wave_raw = get_wavetable_data(instrument)
    wave_size = wave_size // 2
    wave_count = wave_count // 2
    wave_raw = wave_raw[::2]
    set_wavetable_data(instrument, wave_size, wave_count, wave_raw)
    instrument.includes["Name"] += " (Len/2)"
    return instrument

def op_pwm(instrument: Property, repeat: int):
    instrument = instrument.copy()
    wave_size, _, wave_raw = get_wavetable_data(instrument)
    use_wave_count = 1024 // wave_size
    wave = pwm(wave_raw, use_wave_count)
    set_wavetable_data(instrument, wave_size, use_wave_count, wave, repeat, loop=True)
    instrument.includes["Name"] += " (PWM)"
    return instrument

def op_averange(instrument: Property, repeat: int):
    instrument = instrument.copy()
    wave_size, _, wave_raw = get_wavetable_data(instrument)
    use_wave_count = 1024 // wave_size
    wave = averange(wave_raw, use_wave_count)
    set_wavetable_data(instrument, wave_size, use_wave_count, wave, repeat, loop=True)
    instrument.includes["Name"] += " (Averange)"
    return instrument

def select_wavetable_instrument(wtis: list[Property]):
    if not wtis:
        raise ValueError("No wavetable instrument")
    section = 0
    max_section = len(wtis) - 1
    while 1:
        cls()
        current_instrument = wtis[section]
        size, length, wave = get_wavetable_data(current_instrument)
        upwave, downwave = make_wavetable_print(wave[:size])
        print(upwave + "\n" + downwave)
        for i, wt in enumerate(wtis):
            if i == section:
                print(f"> {i + 1}. {wt['Name']}")
            else:
                print(f"  {i + 1}. {wt['Name']}")
        match wait_resp(["up", "down", "right"]):
            case "up":
                section = (section - 1) % (max_section + 1)
            case "down":
                section = (section + 1) % (max_section + 1)
            case "right":
                return wtis[section]
    raise AssertionError("It can't run to here.")


def select_function():
    functions = ("Chorus", "Averange", "PWM", "Length/2")
    section = 0
    max_section = len(functions) - 1
    while 1:
        cls()
        print("Select a function:")
        for i, f in enumerate(functions):
            if i == section:
                print(f"> {f}")
            else:
                print(f"  {f}")
        match wait_resp(["up", "down", "right"]):
            case "up":
                section = (section - 1) % (max_section + 1)
            case "down":
                section = (section + 1) % (max_section + 1)
            case "right":
                return functions[section]
    raise AssertionError("It can't run to here.")


def select_repeat_speed():
    speed = 1
    while 1:
        print(f"Repeat speed: {speed}", end="\r")
        match wait_resp(["up", "down", "right"]):
            case "up":
                speed = min(speed + 1, 15)
            case "down":
                speed = max(speed - 1, 1)
            case "right":
                print(f"Set repeat speed: {speed}")
                return speed
    raise AssertionError("It can't run to here.")
