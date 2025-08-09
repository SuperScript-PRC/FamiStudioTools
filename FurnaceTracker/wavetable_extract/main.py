import os
from libs.constructor import make_default_file_with_n163_instruments
from libs.extractor import extract_wavetables, get_name
from libs.coverter import convert_to_n163_instrument

this_dir = os.path.dirname(__file__)

def main():
    with open(os.path.join(this_dir, "input.txt")) as f:
        content = f.read()
    name = get_name(content)
    wts = extract_wavetables(content)
    print(f"{len(wts)} wavetable(s) extracted")
    with open(os.path.join(this_dir, "output.txt"), "w") as f:
        f.write(
            make_default_file_with_n163_instruments(
                name,
                [
                    convert_to_n163_instrument(f"Wavetable {i}", j)
                    for i, j in enumerate(wts)
                ]
            )
        )
    print("Process finished.")

main()
