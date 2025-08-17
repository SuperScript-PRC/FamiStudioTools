import keyboard
from .define import Property

WAVETABLE = " ▁▂▃▄▅▆▇▉"

def cls():
    print("\033c")
    
def wait_resp(accept_events: list[str]):
    while 1:
        resp = keyboard.read_event()
        if resp.event_type == keyboard.KEY_DOWN:
            evt_name = resp.name
            if evt_name in accept_events:
                return evt_name

def make_wavetable_print(wave: list[int]):
    up = "".join([WAVETABLE[max(0, i%16-8)] for i in wave])
    down = "".join([WAVETABLE[min(8, i%16)] for i in wave])
    return up, down

def get_wavetable_data(instrument_comp: Property):
    w = instrument_comp.children[0]
    # r = instrument_comp.children[1]
    N163WaveSize = int(instrument_comp["N163WaveSize"])
    N163WaveCount = int(instrument_comp["N163WaveCount"])
    Values = [int(i) for i in w["Values"].split(",")]
    return N163WaveSize, N163WaveCount, Values


def set_wavetable_data(
    instrument_comp: Property, N163WaveSize: int, N163WaveCount: int, Values: list[int], repeat: int = 1, loop: int | None = None
):
    wave_comp = instrument_comp.children[0]
    loop_comp = instrument_comp.children[1]
    instrument_comp["N163WaveSize"] = str(N163WaveSize)
    instrument_comp["N163WaveCount"] = str(N163WaveCount)
    instrument_comp["Length"] = str(N163WaveSize * N163WaveCount)
    wave_comp["Values"] = ",".join(map(str, Values))
    loop_comp["Length"] = str(N163WaveCount)
    loop_comp["Values"] = ",".join(str(repeat) for _ in range(N163WaveCount))
    if loop is not None:
        wave_comp["Loop"] = "0"
        loop_comp["Loop"] = "0"

