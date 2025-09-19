from pathlib import Path
import libs.export
import libs.file_constructor
import libs.logic
import libs.cor_export

##### CONFIGURATION #####

# Basic configuration
FAMISTUDIO_VERSION = (
    "4.4.1"  # FamiStudio file version. Too low or too high will cause problems
)
SILENT_THRESHOLD = (
    20  # When a local int volume is below this threshold, it will be considered silent
)
VOLUME_FIX_VALUE = 1.1  # Add it when you find the instrument volumes are all below 15

# If you want 240 sized wave, use this (the config is recommended)
WAVE_SIZE = 240
BASE_NOTE = "A#4"
FIRST_FINE_PITCH = -13

# If you want 128 sized wave, use this (the config is recommended)
# WAVE_SIZE = 128
# BASE_NOTE = "B3"
# FIRST_FINE_PITCH = -5

# If you want 64 sized wave, use this (the config is recommended)
# WAVE_SIZE = 64
# BASE_NOTE = "B2"
# FIRST_FINE_PITCH = -2

# If you want 32 sized wave, use this (the config is recommended) [That's CRAZY!!!!!!]
# WAVE_SIZE = 32
# BASE_NOTE = "B1"
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
volumes, corr_waves = libs.logic.normalize_to_height_and_get_volume(
    resampled,
    WAVE_SIZE,
    15,
    15,
    volume_fix_value=VOLUME_FIX_VALUE,
    silent_threshold=SILENT_THRESHOLD,
)


print("Generating instruments and patterns")
instruments, patterns, pattern_instances = libs.export.collect_waves(
    volumes,
    corr_waves,
    BASE_NOTE,
    FIRST_FINE_PITCH,
    wave_size=WAVE_SIZE,
    wave_count=WAVE_PAGES,
    pattern_length=PATTERN_LENGTH,
)

print("Constructing file")
file_node = libs.file_constructor.construct_file(
    FAMISTUDIO_VERSION, instruments, patterns, pattern_instances
)

with open(thispath / "output.txt", "w") as f:
    f.write(file_node.marshal())
