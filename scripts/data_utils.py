"""Shared, conservative YAML loading helpers."""
from pathlib import Path

import yaml


class DirectoryLoader(yaml.SafeLoader):
    pass


# Keep ISO dates as strings so the schema can validate their lexical form.
DirectoryLoader.yaml_implicit_resolvers = {
    key: list(value) for key, value in yaml.SafeLoader.yaml_implicit_resolvers.items()
}
for first_char, resolvers in list(DirectoryLoader.yaml_implicit_resolvers.items()):
    DirectoryLoader.yaml_implicit_resolvers[first_char] = [
        (tag, regexp) for tag, regexp in resolvers
        if tag != "tag:yaml.org,2002:timestamp"
    ]


def _construct_mapping(loader, node, deep=False):
    mapping = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=deep)
        if key in mapping:
            raise yaml.constructor.ConstructorError(
                "while constructing a mapping", node.start_mark,
                f"duplicate key {key!r}", key_node.start_mark,
            )
        mapping[key] = loader.construct_object(value_node, deep=deep)
    return mapping


DirectoryLoader.add_constructor(
    yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, _construct_mapping
)


def load_dataset(path: Path) -> dict:
    with path.open(encoding="utf-8") as stream:
        value = yaml.load(stream, Loader=DirectoryLoader)
    if not isinstance(value, dict):
        raise ValueError("dataset root must be a YAML mapping")
    return value
