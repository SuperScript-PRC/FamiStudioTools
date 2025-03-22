# WaveTable Extract

This function allows you extract wavetables in FurnaceTracker and export to FamiStudio N163 instruments.

- Step.1
Open a furnace tracker file (.fur) and select "File" -> "export" and choose Export Text, and export it as `input.txt`

- Step.2
Move the `input.txt` to this workspace and run `main.py` by Python 3, the `output.txt` file will be written in this workspace.

- Step.3
Open FamiStudio and drag `output.txt` into it, and you get it!