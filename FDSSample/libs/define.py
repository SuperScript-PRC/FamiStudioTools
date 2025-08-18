from dataclasses import dataclass


@dataclass
class Property:
    indent: int
    label: str
    includes: dict[str, str]
    children: list["Property"]

    def __getitem__(self, key: str) -> str:
        return self.includes[key]

    def __setitem__(self, name: str, value: str):
        self.includes[name] = value

    def str(self):
        includes = []
        for k, v in self.includes.items():
            includes.append(f'{k}="{v}"')
        return "\t" * self.indent + f"{self.label} {' '.join(includes)}"
    
    def marshal(self):
        line = self.str()
        sub_lines = "\n".join(child.marshal() for child in self.children)
        return line + "\n" + sub_lines

    def copy(self):
        return Property(
            self.indent,
            self.label,
            self.includes.copy(),
            [i.copy() for i in self.children],
        )