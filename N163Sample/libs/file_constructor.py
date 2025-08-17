from .define import Property


def construct_file(
    instrument_nodes: list[Property], n163_channel_subnodes: list[Property]
):
    song_node = Property(
        1,
        "Song",
        {
            "Name": "Song 1",
            "Color": "0000FF",
            "Length": "64",
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
            Property(2, "Channel", includes={"Type": "N163Wave1"}, children=n163_channel_subnodes),
        ],
    )
    file_node = Property(
        0,
        "Project",
        {
            "Version": "4.4.1",
            "TempoMode": "FamiStudio",
            "Name": "New Project",
            "Author": "FamiStudio",
            "Expansions": "N163",
            "NumN163Channels": "1",
        },
        children=[
            *instrument_nodes,
            song_node
        ],
    )
    return file_node
