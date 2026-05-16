"""CLI entry point for declarative performance workflows."""

from __future__ import annotations

import argparse


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="declarative-performance",
        description="Declarative musical performance toolkit.",
    )
    parser.add_argument(
        "--mode",
        choices=["practice", "performance"],
        default="practice",
        help="Select workflow mode.",
    )
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    # Stub output to confirm wiring while implementation is in progress.
    print(f"declarative-performance: mode={args.mode}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
