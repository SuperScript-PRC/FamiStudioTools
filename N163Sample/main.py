from pathlib import Path
import libs.export
import libs.file_constructor
import libs.logic
import libs.cor_export

##### CONFIGURATION #####

# If you want 240 sized wave, use this (the config is recommended)
WAVE_SIZE = 240
BASE_NOTE = "A#4"
FIRST_FINE_PITCH = -13

# If you want 64 sized wave, use this (the config is recommended)
# WAVE_SIZE = 64
# BASE_NOTE = "B2"
# FIRST_FINE_PITCH = -2

##### CONFIGURATION END ##

# These are automatically calculated
SAMPLE_RATE = WAVE_SIZE * 60
WAVE_PAGES = 1024 // WAVE_SIZE
TOTAL_WAVE_LENGTH = WAVE_PAGES * WAVE_SIZE

# These will be automatically calculated later
PATTERN_LENGTH = 160

thispath = Path(__file__).parent

print("Reading and resampling wave file")
with open(thispath / "input.wav", "rb") as f:
    resampled = libs.logic.resample_audio(f, SAMPLE_RATE)

print("Normalizing wave file to N163 format")
corr_wave = libs.logic.normalize_to_height_16(resampled)

print("Spliting wave")
corr_waves = libs.logic.to_n163_waves(corr_wave, TOTAL_WAVE_LENGTH)

print("Generating corfile")
with open(thispath / "cor_output.wav", "wb") as f:
    libs.cor_export.corfile(f, corr_wave)

print("Generating instruments and patterns")
instruments, patterns, pattern_instances = libs.export.collect_waves(
    corr_waves,
    BASE_NOTE,
    FIRST_FINE_PITCH,
    wave_size=WAVE_SIZE,
    wave_count=WAVE_PAGES,
    pattern_length=PATTERN_LENGTH,
)

print("Constructing file")
file_node = libs.file_constructor.construct_file(
    instruments, [*patterns, *pattern_instances]
)

with open(thispath / "output.txt", "w") as f:
    f.write(file_node.marshal())
