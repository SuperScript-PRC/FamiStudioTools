from pathlib import Path
from libs.define import Property
from libs.parser import parse_file_to_properties_flat, fold_prperties_list
from libs.export import make_file_content, unfold_properties
from libs.behaviour import operation

this_dir = Path(__file__).parent
master_prop = Property(-1, "master", {}, [])

with open(this_dir / "input.txt", encoding="utf-8") as f:
    content = f.read()
    
pf = parse_file_to_properties_flat(content)
fold_prperties_list(master_prop, pf)

project_node = master_prop.children[0]
instruments = [i for i in project_node.children if i.label == "Instrument" and i.includes.get("Expansion") == "N163"]

new_ins = operation(instruments)
if new_ins:
    project_node.children.append(new_ins)
    
fcontent = make_file_content(unfold_properties(project_node))
with open(this_dir / "output.txt", "w", encoding="utf-8") as f:
    f.write(fcontent)