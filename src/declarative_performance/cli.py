"""CLI entry point for declarative performance workflows."""

from __future__ import annotations

import argparse
from pathlib import Path

from declarative_performance.carxp_generator import load_yaml_file, merge_config, write_carxp_file


def default_carla_defaults_path() -> Path:
    return Path(__file__).resolve().parents[1] / "carla_defaults.yml"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="declarative-performance",
        description="Declarative musical performance toolkit.",
    )
    parser.add_argument(
        "config",
        help="Path to the declarative YAML configuration file.",
    )
    parser.add_argument(
        "--carla",
        action="store_true",
        default=True,
        help="Generate a Carla project file. This is currently the default backend.",
    )
    parser.add_argument(
        "--defaults",
        default=str(default_carla_defaults_path()),
        help="Path to Carla defaults YAML. Defaults to src/carla_defaults.yml.",
    )
    parser.add_argument(
        "--outfile",
        default="out.carxp",
        help="Output Carla project file path.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if not args.carla:
        parser.error("Only Carla output is currently supported.")

    defaults = load_yaml_file(args.defaults)
    config = load_yaml_file(args.config)
    merged = merge_config(defaults, config)
    write_carxp_file(merged, args.outfile)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
