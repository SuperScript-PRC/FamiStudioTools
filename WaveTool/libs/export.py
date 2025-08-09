from .define import Property


def make_property_line(prop: Property):
    return "\t" * prop.indent + " ".join(
        [prop.label] + [f'{name}="{value}"' for name, value in prop.includes.items()]
    )

def make_file_content(unfolded_properties: list[Property]) -> str:
    return "\n".join(i.str() for i in unfolded_properties)

def unfold_properties(p: Property):
    res: list[Property] = [p]
    for child in p.children:
        res.extend(unfold_properties(child))
    return res
