from pathlib import Path

import libs.export
import libs.file_constructor
import libs.logic
import libs.cor_export

thispath = Path(__file__).parent

RATE = 14400

print("Reading and resampling wave file")
with open(thispath / "input.wav", "rb") as f:
    resampled = libs.logic.resample_audio(f, RATE)

print("Normalizing wave file to N163 format")
corr_wave = libs.logic.normalize_to_height_16(resampled)

print("Spliting wave")
corr_waves = libs.logic.to_n163_waves(corr_wave)

print("Generating corfile")
with open(thispath / "cor_output.wav", "wb") as f:
    libs.cor_export.corfile(f, corr_wave)

print("Generating instruments and patterns")
instruments, patterns, pattern_instances = libs.export.collect_waves(corr_waves)

print("Constructing file")
file_node = libs.file_constructor.construct_file(
    instruments, [*patterns, *pattern_instances]
)

with open(thispath / "output.txt", "w") as f:
    f.write(file_node.marshal())
