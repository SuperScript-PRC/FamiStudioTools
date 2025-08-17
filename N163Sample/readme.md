## About FamiStudio N163

- The N163 instrument in FamiStudio can have up to 240 size.
- A frame in FamiStudio is 1/60 sec.

So we can calculate the max sampling rate of N163 instrument is:

- 1s = 240 * 60 = 14400 Hz = 14.4kHz

## Usage

- Put your input wave file as `input.wav`
- Run `main.py` and it generates `output.txt` and `cor_output.wav`
- Drag the `output.txt` to FamiStudio to generate the project. Your wave sample will be put to the first N163 channel.
- The `cor_output.wav` is the wave file with sample rate to 14400 Hz, the same of the sample rate of N163 instrument.