## About FamiStudio FDS

- The FDS instrument in FamiStudio can have up to 64 size.
- A frame in FamiStudio is 1/60 sec.

So we can calculate the max sampling rate of FDS instrument is:

- 1s = 64 * 60 = 3840 Hz = 3.84kHz

But its depth is better than N163.

## Usage

- Put your input wave file as `input.wav`
- Run `main.py` and it generates `output.txt` and `cor_output.wav`
- Drag the `output.txt` to FamiStudio to generate the project. Your wave sample will be put to the first FDS channel.
- The `cor_output.wav` is the wave file with sample rate to 3840 Hz, the same of the sample rate of FDS instrument.