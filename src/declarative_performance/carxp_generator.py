"""Generate Carla project files from declarative YAML."""

from __future__ import annotations

from copy import deepcopy
from importlib import resources
from pathlib import Path
from typing import Any

from jinja2 import Environment, PackageLoader, select_autoescape
import yaml

TEMPLATE_ENVIRONMENT = Environment(
    loader=PackageLoader("declarative_performance", "templates"),
    autoescape=select_autoescape(enabled_extensions=("xml", "j2"), default_for_string=True),
    trim_blocks=True,
    lstrip_blocks=True,
)
CARXP_TEMPLATE = "carxp.xml.j2"


def load_yaml_file(path: str | Path) -> dict[str, Any]:
    with Path(path).open("r", encoding="utf-8") as handle:
        data = yaml.safe_load(handle) or {}

    if not isinstance(data, dict):
        raise ValueError("Expected a mapping at the top level of the YAML file")

    return data


def merge_config(defaults: dict[str, Any], config: dict[str, Any]) -> dict[str, Any]:
    merged = deepcopy(defaults)

    for key, value in config.items():
        if isinstance(value, dict) and isinstance(merged.get(key), dict):
            merged[key] = merge_config(merged[key], value)
        else:
            merged[key] = deepcopy(value)

    return merged


def generate_carxp_xml(config: dict[str, Any]) -> str:
    template = TEMPLATE_ENVIRONMENT.get_template(CARXP_TEMPLATE)
    renderable = _normalize_for_render(config)
    return template.render(config=renderable)


def write_carxp_file(config: dict[str, Any], output_path: str | Path) -> Path:
    output = Path(output_path)
    output.write_text(generate_carxp_xml(config), encoding="utf-8")
    return output


def _normalize_for_render(value: Any) -> Any:
    if isinstance(value, dict):
        return {key: _normalize_for_render(item) for key, item in value.items()}
    if isinstance(value, list):
        return [_normalize_for_render(item) for item in value]
    return _stringify_scalar(value)


def _stringify_scalar(value: Any) -> str:
    if isinstance(value, bool):
        return str(value).lower()
    return str(value)
