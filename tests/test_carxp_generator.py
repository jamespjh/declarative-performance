from __future__ import annotations

from pathlib import Path
from lxml import etree

from declarative_performance.carxp_generator import generate_carxp_xml, load_yaml_file, merge_config

FIXTURES = Path(__file__).parent / "fixtures"
REPO_ROOT = Path(__file__).resolve().parents[1]


def test_generate_carxp_matches_reference_structure() -> None:
    defaults = load_yaml_file(REPO_ROOT / "src" / "carla_defaults.yml")
    config = load_yaml_file(FIXTURES / "test1.yml")

    xml_text = generate_carxp_xml(merge_config(defaults, config))

    generated_root = _parse_generated_xml(xml_text)
    fixture_root = etree.parse(str(FIXTURES / "test1.carxp")).getroot()

    assert _extract_engine_settings(generated_root) == _extract_engine_settings(fixture_root)
    assert _extract_transport(generated_root) == _extract_transport(fixture_root)
    assert _extract_plugins(generated_root) == _extract_plugins(fixture_root)
    assert _extract_connections(generated_root, "Patchbay") == _extract_connections(fixture_root, "Patchbay")
    assert _extract_connections(generated_root, "ExternalPatchbay") == _extract_connections(fixture_root, "ExternalPatchbay")


def _parse_generated_xml(xml_text: str) -> etree._Element:
    return etree.fromstring(xml_text.encode("utf-8"))


def _extract_engine_settings(root: etree._Element) -> dict[str, str]:
    return _extract_mapping(root.find("EngineSettings"))


def _extract_transport(root: etree._Element) -> dict[str, str]:
    return _extract_mapping(root.find("Transport"))


def _extract_plugins(root: etree._Element) -> list[dict[str, dict[str, str]]]:
    plugins: list[dict[str, dict[str, str]]] = []
    for plugin in root.findall("Plugin"):
        plugins.append(
            {
                "info": _extract_mapping(plugin.find("Info")),
                "data": _extract_mapping(plugin.find("Data"), normalize_chunk=True),
            }
        )
    return plugins


def _extract_connections(root: etree._Element, section: str) -> list[tuple[str, str]]:
    element = root.find(section)
    if element is None:
        return []

    connections: list[tuple[str, str]] = []
    for connection in element.findall("Connection"):
        source = connection.findtext("Source", default="")
        target = connection.findtext("Target", default="")
        connections.append((source, target))
    return connections


def _extract_mapping(element: etree._Element | None, normalize_chunk: bool = False) -> dict[str, str]:
    if element is None:
        return {}

    mapping = {child.tag: child.text or "" for child in element}
    if normalize_chunk and "Chunk" in mapping:
        mapping["Chunk"] = "".join(mapping["Chunk"].split())
    return mapping
