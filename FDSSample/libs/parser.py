from .define import Property


def split_line(line: str):
    is_string = False
    cached_string = ""
    output: list[str] = []
    for char in line:
        if char == '"':
            is_string = not is_string
        if not is_string and char == " ":
            output.append(cached_string)
            cached_string = ""
        else:
            cached_string += char
    if cached_string:
        output.append(cached_string)
    return output


def parse_property(line: str):
    indent = line.count("\t")
    args = split_line(line.strip())
    properties: dict[str, str] = {}
    property_label = args[0]
    if not property_label.isalpha():
        raise ValueError("Invalid property label: " + property_label)
    for property_str in args[1:]:
        property_name, property_value = property_str.split("=")
        if not (property_value.startswith('"') and property_value.endswith('"')):
            raise ValueError("Invalid property value: " + property_value)
        properties[property_name] = property_value[1:-1]
    return Property(indent, property_label, properties, [])


def parse_file_to_properties_flat(content: str):
    flat_list: list[Property] = []
    for line in content.splitlines():
        prop = parse_property(line)
        flat_list.append(prop)
    return flat_list


def fold_prperties_list(current_prop: Property, ls: list[Property]):
    current_indent = current_prop.indent + 1
    last_prop: Property | None = None
    while len(ls) > 0:
        prop = ls[0]
        if prop.indent < current_indent:
            return
        elif prop.indent == current_indent:
            current_prop.children.append(prop)
            ls.pop(0)
        elif prop.indent == current_indent + 1:
            if last_prop is not None:
                fold_prperties_list(last_prop, ls)
            else:
                current_prop.children.append(prop)
                fold_prperties_list(current_prop, ls)
        else:
            raise ValueError(
                f"Invalid indent, current={current_indent}, prop={prop.indent} ({prop.label})"
            )
        last_prop = prop
