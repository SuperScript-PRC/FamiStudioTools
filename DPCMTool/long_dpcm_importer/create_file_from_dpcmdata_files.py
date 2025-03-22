import re
import os
from dataclasses import dataclass

find_dpcms = re.compile(r'DPCMSample Name="(sample-[0-9]*)" Color="([0-9a-z]*)" Data="([0-9a-zA-Z]*)"')

TITLE = 'Project Version="4.2.1" TempoMode="FamiStudio" Name="Sampler output file" Author="Superの采样器"'

CONTENT = \
'''Song Name="Sample Song" Color="88eb8c" Length="128" LoopPoint="0" PatternLength="16" BeatLength="4" NoteLength="10" Groove="10" GroovePaddingMode="Middle"
		Channel Type="Square1"
		Channel Type="Square2"
		Channel Type="Triangle"
		Channel Type="Noise"
		Channel Type="DPCM"'''

@dataclass
class DPCMSampleData:
    name: str
    color: str
    data: str

def generate_dpcm_text(dt: DPCMSampleData):
    return f'	DPCMSample Name="{dt.name}" Color="{dt.color}" Data="{dt.data}"'

def generate_dpcm_instruments_text(dt: list[DPCMSampleData]):
    ins_counter = 0
    basic = '''	Instrument Name="Sampler-0" Color="5ac4ff"'''
    notes = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
    note_basic = 0
    note_index = 0
    used_notes: list[tuple[str, str]] = []
    for d in dt:
        basic += f'\n		DPCMMapping Note="{notes[note_index]}{note_basic}" Sample="{d.name}" Pitch="15" Loop="False"'
        used_notes.append((f"Sampler-{ins_counter}", notes[note_index] + str(note_basic)))
        note_index += 1
        if note_basic > 7 and note_index >= 5:
            ins_counter += 1
            note_index = 0
            note_basic = 0
            basic += f'''\n	Instrument Name="Sampler-{hex(ins_counter)[2:]}" Color="5ac4ff"'''
            # print(f"乐器采样数已达上限, 新建乐器以存放: DPCM乐器{ins_counter}")
        if note_index >= len(notes):
            note_index = 0
            note_basic += 1
    return basic, used_notes

def generate_all_pat_data(used_notes: list[tuple[str, str]]):
    DURATION = 30
    pattern_time_sum = 0
    pattern_counter = 1
    output = '			Pattern Name="Pattern 1" Color="d863ec"'
    output2 = '			PatternInstance Time="0" Pattern="Pattern 1"'
    for ins, n in used_notes:
        output += f'\n				Note Time="{pattern_time_sum}" Value="{n}" Duration="{DURATION}" Instrument="{ins}"'
        pattern_time_sum += DURATION
        if pattern_time_sum >= 160:
            pattern_time_sum -= 160
            pattern_counter += 1
            output += f'\n			Pattern Name="Pattern {pattern_counter}" Color="d863ec"'
            output2 += f'\n			PatternInstance Time="{pattern_counter-1}" Pattern="Pattern {pattern_counter}"'
    return output + "\n" + output2


with open(os.path.join(os.path.dirname(__file__), "input.txt"), "r", encoding="utf-8") as f:
    content = f.read()

all_dpcm_samples = find_dpcms.findall(content)
all_dpcm_datas: list[DPCMSampleData] = []

for name, color, data in all_dpcm_samples:
    all_dpcm_datas.append(DPCMSampleData(name, color, data))

dpcm_text, used_notes = generate_dpcm_instruments_text(all_dpcm_datas)

output_text = (
    TITLE
    + "\n"
    + "\n".join(generate_dpcm_text(i) for i in all_dpcm_datas)
    + "\n" + dpcm_text
    + "\n" + CONTENT
    + "\n" + generate_all_pat_data(used_notes)
)

with open(os.path.join(os.path.dirname(__file__), "output.txt"), "w", encoding="utf-8") as f2:
    f2.write(output_text)

print("FamiStudio Text write finished.")