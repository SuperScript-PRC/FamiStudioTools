from dataclasses import dataclass, field


def construct_file_head(
    version: str,
    tempo_mode: str,
    name: str,
    author: str,
    expansions: str,
    num_n163_channels: int,
):
    return f'Project Version="{version}" TempoMode="{tempo_mode}" Name="{name}" Author="{author}" Expansions="{expansions}" NumN163Channels="{num_n163_channels}"'


@dataclass
class N163Instrument:
    Name: str
    N163WaveSize: int = 16
    Values: list[int] = field(default_factory=list)

    def __str__(self):
        return (
            f'    Instrument Name="{self.Name}" Color="00ffff" Expansion="N163" N163WavePreset="Custom" N163WaveSize="{self.N163WaveSize}" N163WavePos="0" N163WaveCount="1"\n'
            f'        Envelope Type="N163Wave" Length="{self.N163WaveSize}" Values="{",".join(map(str, self.Values))}"\n'
            r'        Envelope Type="Repeat" Length="1" Values="1"'
        )


def make_default_file_with_n163_instruments(name: str, instruments: list[N163Instrument]):
    content = construct_file_head(
        "4.3.2", "FamiStudio", name, "WTConverter", "N163", 1
    )
    content += "\n"
    content += "\n".join(str(i) for i in instruments) + "\n"
    content += (
        '    Song Name="Song 1" Color="5dd2ff" Length="16" LoopPoint="0" PatternLength="16" BeatLength="4" NoteLength="10" Groove="10" GroovePaddingMode="Middle"\n'
        '        Channel Type="Square1"\n'
        '        Channel Type="Square2"\n'
        '        Channel Type="Triangle"\n'
        '        Channel Type="Noise"\n'
        '        Channel Type="DPCM"\n'
        '        Channel Type="N163Wave1"\n'
    )
    return content
