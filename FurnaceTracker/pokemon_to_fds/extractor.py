import re
import os

this_dir = os.path.dirname(__file__)

orders_map_block_extractor = re.compile(
    r"orders:\n```\n"
    r"([0-9a-fA-F |\n]+)+"
    r"```"
)
order_map_extractor = re.compile(
    r"(?P<index>[0-9a-fA-F]{2}) \| (?P<c1>[0-9a-fA-F]{2}) (?P<c2>[0-9a-fA-F]{2}) (?P<c3>[0-9a-fA-F]{2}) (?P<c4>[0-9a-fA-F]{2}) (?P<c5>[0-9a-fA-F]{2}) (?P<c6>[0-9a-fA-F]{2})"
)


def get_orders_map(content: str):
    map_content = orders_map_block_extractor.search(content)
    if map_content is None:
        raise ValueError("Order map not found")
    result: dict[int, int] = {}
    for g in order_map_extractor.finditer(map_content.group()):
        index = int(g.group("index"), 16)
        order1 = int(g.group("c1"), 16)
        result[index] = order1
    return result


with open(os.path.join(this_dir, "input.txt")) as f:
    text = f.read()
print(get_orders_map(text))