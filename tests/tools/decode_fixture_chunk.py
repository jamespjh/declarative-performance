from __future__ import annotations

import argparse
import base64
import plistlib
from pathlib import Path

from lxml import etree


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Decode the first Carla plugin Chunk blob from a .carxp fixture.",
    )
    parser.add_argument(
        "--input",
        default="tests/fixtures/test1.carxp",
        help="Path to the input .carxp file.",
    )
    parser.add_argument(
        "--output",
        default="tests/fixtures/test1.chunk.decoded.plist",
        help="Path to the decoded plist output file.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    input_path = Path(args.input)
    output_path = Path(args.output)

    xml_root = etree.parse(str(input_path)).getroot()
    chunk_element = xml_root.find(".//Plugin/Data/Chunk")
    if chunk_element is None or chunk_element.text is None:
        raise ValueError("No plugin chunk found in input fixture")

    chunk_base64 = "".join(chunk_element.text.split())
    decoded = base64.b64decode(chunk_base64, validate=True)

    plist_obj = plistlib.loads(decoded)
    plist_xml = plistlib.dumps(plist_obj, fmt=plistlib.FMT_XML)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_bytes(plist_xml)
    print(f"Wrote decoded chunk fixture: {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
