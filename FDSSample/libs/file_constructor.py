from .define import Property


def construct_file(
    famistudio_version: str,
    instrument_nodes: list[Property],
    patterns: list[Property],
    pattern_instances: list[Property],
):
    song_node = Property(
        1,
        "Song",
        {
            "Name": "Song 1",
            "Color": "0000FF",
            "Length": str(len(patterns)),
            "LoopPoint": "0",
            "PatternLength": "16",
            "BeatLength": "4",
            "NoteLength": "10",
            "Groove": "10",
            "GroovePaddingMode": "Middle",
        },
        children=[
            Property(2, "Channel", includes={"Type": "Square1"}, children=[]),
            Property(2, "Channel", includes={"Type": "Square2"}, children=[]),
            Property(2, "Channel", includes={"Type": "Triangle"}, children=[]),
            Property(2, "Channel", includes={"Type": "Noise"}, children=[]),
            Property(2, "Channel", includes={"Type": "DPCM"}, children=[]),
            Property(
                2,
                "Channel",
                includes={"Type": "FDS"},
                children=patterns + pattern_instances,
            ),
        ],
    )
    file_node = Property(
        0,
        "Project",
        {
            "Version": famistudio_version,
            "TempoMode": "FamiStudio",
            "Name": "New Project",
            "Author": "FamiStudio",
            "Expansions": "FDS"
        },
        children=[*instrument_nodes, song_node],
    )
    return file_node
