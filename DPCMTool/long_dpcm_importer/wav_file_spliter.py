# by SuperScript#2528622340@qq.com
import os
import shutil
import wave
from array import array
from typing import TypeVar

VT = TypeVar("VT")

this_path = os.path.dirname(__file__)

try:
    f: wave.Wave_read = wave.open(os.path.join(this_path, "input.wav"), "rb")
except FileNotFoundError:
    input("Missing file input.wav in current folder, press enter to exit.")
    exit()

if f.getnchannels() != 1:
    print("Warning: multi channels not supported, only first channel will be used.")
print("sample rate:", f.getframerate())
print("sample width:", f.getsampwidth())
nframes = f.getparams().nframes
frames = array("h", f.readframes(nframes))

def split_list(lst: "array[int]", length: int) -> list["array[int]"]:
    return [lst[i:i+length] for i in range(0, len(lst), length)]

final_arrs: list["array[int]"] = []
for chunk in split_list(frames, f.getframerate()):
    final_arrs.append(chunk)

if os.path.isdir(output_path := os.path.join(this_path, "output")):
    shutil.rmtree(output_path)

os.mkdir(output_path)

counter = 0
for chunk in final_arrs:
    counter += 1
    with wave.open(os.path.join(this_path, "output", f"sample-{counter}.wav"), "wb") as f1:
        f1.setframerate(f.getframerate())
        f1.setsampwidth(4)
        f1.setnchannels(1)
        f1.writeframes(chunk)

print("WAV file was splited successfully. Now check the ./output/ folder.")