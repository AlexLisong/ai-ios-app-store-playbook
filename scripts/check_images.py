#!/usr/bin/env python3
"""Read-only PNG dimensions/structure checks; not a visual or Apple review test."""
import argparse
import struct
import sys
import zlib
from pathlib import Path

MAX_BYTES = 64 * 1024 * 1024


def png_info(path):
    path = Path(path)
    if path.stat().st_size > MAX_BYTES:
        raise ValueError('PNG exceeds the 64 MiB inspection limit')
    data = path.read_bytes()
    if data[:8] != b'\x89PNG\r\n\x1a\n':
        raise ValueError('not a PNG file')
    pos, chunks, header = 8, [], None
    while pos < len(data):
        if pos + 12 > len(data):
            raise ValueError('truncated PNG chunk')
        length = struct.unpack('>I', data[pos:pos + 4])[0]
        end = pos + 12 + length
        if end > len(data):
            raise ValueError('truncated PNG chunk data')
        kind = data[pos + 4:pos + 8]
        body = data[pos + 8:pos + 8 + length]
        crc = struct.unpack('>I', data[pos + 8 + length:end])[0]
        if zlib.crc32(kind + body) & 0xffffffff != crc:
            raise ValueError('invalid PNG chunk checksum')
        if not chunks and kind != b'IHDR':
            raise ValueError('IHDR must be the first PNG chunk')
        if kind == b'IHDR':
            if header is not None or length != 13:
                raise ValueError('invalid or duplicate IHDR')
            header = struct.unpack('>IIBBBBB', body)
        chunks.append(kind)
        pos = end
        if kind == b'IEND':
            if length or pos != len(data):
                raise ValueError('invalid PNG end/trailing data')
            break
    if not header or not chunks or chunks[-1] != b'IEND' or b'IDAT' not in chunks:
        raise ValueError('incomplete PNG structure')
    width, height, depth, color, compression, filtering, interlace = header
    if not width or not height or compression or filtering or interlace not in (0, 1):
        raise ValueError('invalid PNG header')
    valid_depths = {0: (1, 2, 4, 8, 16), 2: (8, 16), 3: (1, 2, 4, 8), 4: (8, 16), 6: (8, 16)}
    if depth not in valid_depths.get(color, ()):
        raise ValueError('invalid PNG color/depth combination')
    return {'width': width, 'height': height, 'depth': depth, 'color': color,
            'has_alpha': color in (4, 6) or b'tRNS' in chunks}


def validate(path, kind, size=None):
    info = png_info(path)
    expected = size or ((1024, 1024) if kind == 'icon' else (1320, 2868))
    errors = []
    if (info['width'], info['height']) != expected:
        errors.append(f"expected {expected[0]}x{expected[1]}, got {info['width']}x{info['height']}")
    if kind == 'icon' and (info['color'] != 2 or info['depth'] != 8 or info['has_alpha']):
        errors.append('icon must be 8-bit opaque RGB (no alpha/transparency chunk) for this workflow')
    return info, errors


def parse_size(value):
    try:
        width, height = (int(part) for part in value.lower().split('x'))
        if width <= 0 or height <= 0:
            raise ValueError
        return width, height
    except ValueError as error:
        raise argparse.ArgumentTypeError('size must be positive WIDTHxHEIGHT') from error


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--kind', choices=('icon', 'screenshot'), required=True)
    parser.add_argument('--size', type=parse_size, help='override the expected dimensions after checking Apple requirements')
    parser.add_argument('files', type=Path, nargs='+')
    args = parser.parse_args()
    failures = 0
    for path in args.files:
        try:
            info, errors = validate(path, args.kind, args.size)
            if errors:
                failures += 1
                print(f'FAIL {path.name}: {"; ".join(errors)}')
            else:
                print(f'PASS {path.name}: {info["width"]}x{info["height"]}, PNG metadata checked')
        except (OSError, ValueError, struct.error) as error:
            failures += 1
            print(f'FAIL {path.name}: {error}')
    print('Inspect images visually; this check does not decode pixels or establish App Store acceptance.')
    return 1 if failures else 0


if __name__ == '__main__':
    sys.exit(main())
