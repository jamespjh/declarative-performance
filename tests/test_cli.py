from __future__ import annotations

from pathlib import Path
from lxml import etree

from declarative_performance.cli import default_carla_defaults_path, main

FIXTURES = Path(__file__).parent / "fixtures"


def test_cli_writes_default_outfile(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.chdir(tmp_path)

    exit_code = main([str(FIXTURES / "test1.yml")])

    assert exit_code == 0
    output_path = tmp_path / "out.carxp"
    assert output_path.exists()
    assert etree.parse(str(output_path)).getroot().tag == "CARLA-PROJECT"


def test_cli_supports_explicit_defaults_and_outfile(tmp_path: Path) -> None:
    output_path = tmp_path / "example.carxp"

    exit_code = main(
        [
            "--carla",
            "--defaults",
            str(default_carla_defaults_path()),
            str(FIXTURES / "test1.yml"),
            "--outfile",
            str(output_path),
        ]
    )

    assert exit_code == 0
    assert output_path.exists()
    assert etree.parse(str(output_path)).getroot().tag == "CARLA-PROJECT"
