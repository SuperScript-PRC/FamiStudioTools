from pathlib import Path
import libs.export
import libs.file_constructor
import libs.logic
import libs.cor_export

##### CONFIGURATION #####

# Basic configuration
FAMISTUDIO_VERSION = "4.4.1"



##### CONFIGURATION END ##

# Theses are constants
WAVE_SIZE = 64
WAVE_COUNT = 16
BASE_NOTE = "B2"
FIRST_FINE_PITCH = -4
SAMPLE_RATE = WAVE_SIZE * 60
TOTAL_WAVE_LENGTH = WAVE_COUNT * WAVE_SIZE


# These will be automatically calculated later
PATTERN_LENGTH = 160

thispath = Path(__file__).parent

print("Reading and resampling wave file")
with open(thispath / "input.wav", "rb") as f:
    resampled = libs.logic.resample_audio(f, SAMPLE_RATE)

print("Normalizing wave file to FDS format")
corr_wave = libs.logic.normalize_to_height(resampled, 64)

print("Spliting wave")
corr_waves = libs.logic.to_waves(corr_wave, TOTAL_WAVE_LENGTH)

print("Generating corfile")
with open(thispath / "cor_output.wav", "wb") as f:
    libs.cor_export.corfile(f, corr_wave)

print("Generating instruments and patterns")
instruments, patterns, pattern_instances = libs.export.collect_waves(
    corr_waves,
    BASE_NOTE,
    FIRST_FINE_PITCH,
    pattern_length=PATTERN_LENGTH,
)

print("Constructing file")
file_node = libs.file_constructor.construct_file(FAMISTUDIO_VERSION,
    instruments, patterns, pattern_instances
)

with open(thispath / "output.txt", "w") as f:
    f.write(file_node.marshal())
