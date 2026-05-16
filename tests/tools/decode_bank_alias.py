from __future__ import annotations

import argparse
import base64
import json
import plistlib
import struct
from pathlib import Path

from lxml import etree


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Decode the Bank alias payload from a Carla fixture plugin chunk.",
    )
    parser.add_argument(
        "--input",
        default="tests/fixtures/test1.carxp",
        help="Path to the input .carxp file.",
    )
    parser.add_argument(
        "--output",
        default="tests/fixtures/test1.bank.alias.decoded.json",
        help="Path to the decoded alias report JSON file.",
    )
    return parser.parse_args()


def read_bank_blob(carxp_path: Path) -> bytes:
    root = etree.parse(str(carxp_path)).getroot()
    chunk_element = root.find(".//Plugin/Data/Chunk")
    if chunk_element is None or chunk_element.text is None:
        raise ValueError("No plugin chunk found in input fixture")

    chunk_base64 = "".join(chunk_element.text.split())
    plist_payload = plistlib.loads(base64.b64decode(chunk_base64, validate=True))

    bank = plist_payload.get("Bank")
    if not isinstance(bank, bytes):
        raise ValueError("Chunk plist does not contain a bytes-valued Bank field")

    return bank


def decode_pascal(data: bytes, offset: int, max_len: int) -> str:
    length = data[offset]
    length = min(length, max_len)
    raw = data[offset + 1 : offset + 1 + length]
    return raw.decode("mac_roman", errors="replace")


def ascii_runs(data: bytes, min_len: int = 6) -> list[dict[str, object]]:
    runs: list[dict[str, object]] = []
    start = 0
    while start < len(data):
        while start < len(data) and not (32 <= data[start] <= 126):
            start += 1
        if start >= len(data):
            break
        end = start
        while end < len(data) and (32 <= data[end] <= 126):
            end += 1
        if end - start >= min_len:
            runs.append(
                {
                    "offset": start,
                    "length": end - start,
                    "text": data[start:end].decode("ascii", errors="replace"),
                }
            )
        start = end + 1
    return runs


def parse_tag_records(data: bytes, start_offset: int = 150) -> list[dict[str, object]]:
    records: list[dict[str, object]] = []
    offset = start_offset

    while offset + 4 <= len(data):
        tag = struct.unpack_from(">h", data, offset)[0]
        length = struct.unpack_from(">H", data, offset + 2)[0]
        payload_start = offset + 4
        payload_end = payload_start + length

        if payload_end > len(data):
            break

        payload = data[payload_start:payload_end]
        item: dict[str, object] = {
            "offset": offset,
            "tag": tag,
            "length": length,
            "payload_hex": payload.hex(),
        }

        try:
            text = payload.decode("mac_roman")
            if all((31 < ord(ch) < 127) or ch in "\t\r\n" for ch in text):
                item["payload_text"] = text
        except Exception:
            pass

        records.append(item)

        # End marker for classic Alias tagged records.
        if tag == -1:
            break

        offset = payload_end + (length % 2)

    return records


def decode_alias(bank: bytes) -> dict[str, object]:
    if len(bank) < 150:
        raise ValueError("Bank blob too small to be a classic alias record")

    user_type = struct.unpack_from(">I", bank, 0)[0]
    record_size = struct.unpack_from(">H", bank, 4)[0]
    version = struct.unpack_from(">H", bank, 6)[0]
    alias_kind = struct.unpack_from(">H", bank, 8)[0]

    volume_name = decode_pascal(bank, 10, 27)
    target_name = decode_pascal(bank, 50, 63)

    report: dict[str, object] = {
        "length_bytes": len(bank),
        "header": {
            "user_type": user_type,
            "record_size": record_size,
            "version": version,
            "alias_kind": alias_kind,
            "volume_name": volume_name,
            "target_name": target_name,
            "matches_record_size": record_size == len(bank),
        },
        "tag_records": parse_tag_records(bank, start_offset=150),
        "ascii_runs": ascii_runs(bank),
        "hex": bank.hex(),
    }
    return report


def main() -> int:
    args = parse_args()
    input_path = Path(args.input)
    output_path = Path(args.output)

    bank = read_bank_blob(input_path)
    report = decode_alias(bank)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(f"Wrote bank alias fixture: {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
