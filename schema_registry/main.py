import json
from pathlib import Path
from typing import Any

import jsonschema


class SchemaRegistry:
    def __init__(self, path: Path | str):
        self._root = Path(path)
        self._cache = {}

    def get_schema(self, name, version) -> dict[str, Any]:
        path = self._root.joinpath(*name.split("."), f"{version}.json")
        if schema := self._cache.get(path):
            return schema

        with open(path, 'r') as file:
            return json.load(file)

    def validate(self, data, name, version=1):
        schema = self.get_schema(name, version)
        return jsonschema.validate(data, schema)
