import json
with open(
    "data/normalized_catalog.json",
    "r",
    encoding="utf-8"
) as f:
    CATALOG = json.load(f)
def find_assessment(name):
    target = name.lower()
    for item in CATALOG:
        if target in item["name"].lower():
            return item
    return None