from pathlib import Path

path = Path(__file__).parent.joinpath("Source")

def build(path: Path):
    items = []
    for child in path.iterdir():
        print(child)
        node = {"id": str(child), "name": child.name}
        if child.is_dir():
            node["children"] = build(child)
        items.append(node)
    return items

print(build(path))
