import wave
from typing import IO
from numpy.typing import NDArray    
from numpy import uint8

def corfile(f: IO[bytes], w: NDArray[uint8]):
    wavefile = wave.open(f, "wb")
    wavefile.setnchannels(1)
    wavefile.setframerate(14400)
    wavefile.setsampwidth(1)
    wl = w * 16 # 0~15
    wavefile.writeframes(wl.tobytes())