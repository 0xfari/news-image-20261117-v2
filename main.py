#!/usr/bin/env python3
"""Entry point for news-image-20261117-v2.

Decodes the bundled base64 image (entry.png.b64, next to this file) and
writes it as entry.png into $MAKEFUN_OUTPUT_DIR (default /output).

Stdlib only, no network, no clock, no randomness: the same input always
produces the same bytes. The output is checked before it is written:
PNG signature, IHDR dimensions (at most 1024x1024) and a 1 MiB size cap.
"""
import base64
import os
import struct
import sys

MAX_BYTES = 1_048_576
MAX_DIM = 1024
PNG_SIG = b"\x89PNG\r\n\x1a\n"


def fail(msg):
    print(f"main.py: {msg}", file=sys.stderr)
    return 1


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "entry.png.b64")
    try:
        with open(src, "rb") as fh:
            raw = fh.read()
    except OSError as exc:
        return fail(f"cannot read entry.png.b64: {exc}")
    # base64 text: ignore any surrounding whitespace/newlines.
    raw = b"".join(raw.split())
    try:
        data = base64.b64decode(raw, validate=True)
    except Exception as exc:
        return fail(f"entry.png.b64 is not valid base64: {exc}")
    if len(data) > MAX_BYTES:
        return fail(f"image is {len(data)} bytes, over the 1 MiB cap")
    if not data.startswith(PNG_SIG):
        return fail("decoded bytes are not a PNG")
    if len(data) < 33 or data[12:16] != b"IHDR":
        return fail("PNG has no IHDR chunk")
    width, height = struct.unpack(">II", data[16:24])
    if width == 0 or height == 0 or width > MAX_DIM or height > MAX_DIM:
        return fail(f"bad dimensions {width}x{height}")
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "entry.png")
    with open(out_path, "wb") as fh:
        fh.write(data)
    print(f"wrote {out_path} ({len(data)} bytes, {width}x{height})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
