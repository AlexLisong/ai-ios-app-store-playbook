"""Synthetic local fixtures only. No account/device data or provider requests."""
import contextlib
import importlib.util
import io
import json
import plistlib
import struct
import tempfile
import unittest
from unittest import mock
import zlib
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1] / 'scripts'


def load(name):
    spec = importlib.util.spec_from_file_location(name, SCRIPTS / f'{name}.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


images = load('check_images')
preflight = load('preflight')
repository = load('check_repo')


def chunk(kind, body):
    return struct.pack('>I', len(body)) + kind + body + struct.pack('>I', zlib.crc32(kind + body) & 0xffffffff)


def write_png(path, width=1024, height=1024, color=2, transparency=False):
    channels = {2: 3, 6: 4}[color]
    header = struct.pack('>IIBBBBB', width, height, 8, color, 0, 0, 0)
    data = b'\x89PNG\r\n\x1a\n' + chunk(b'IHDR', header)
    if transparency:
        data += chunk(b'tRNS', b'\x00' * 6)
    data += chunk(b'IDAT', zlib.compress((b'\x00' + b'\x00' * width * channels) * height))
    path.write_bytes(data + chunk(b'IEND', b''))


class ImageTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.image = Path(self.temp.name) / 'synthetic.png'

    def test_opaque_rgb_icon_passes_without_modification(self):
        write_png(self.image)
        before = self.image.read_bytes()
        info, errors = images.validate(self.image, 'icon')
        self.assertEqual(errors, [])
        self.assertFalse(info['has_alpha'])
        self.assertEqual(before, self.image.read_bytes())

    def test_alpha_icon_fails_even_if_pixels_are_opaque(self):
        write_png(self.image, color=6)
        self.assertTrue(images.validate(self.image, 'icon')[1])

    def test_transparency_chunk_icon_fails(self):
        write_png(self.image, transparency=True)
        self.assertTrue(images.validate(self.image, 'icon')[1])

    def test_wrong_size_fails(self):
        write_png(self.image, 64, 64)
        self.assertIn('expected 1024x1024', images.validate(self.image, 'icon')[1][0])

    def test_native_screenshot_size_and_override(self):
        write_png(self.image, 1320, 2868)
        self.assertEqual(images.validate(self.image, 'screenshot')[1], [])
        self.assertTrue(images.validate(self.image, 'screenshot', (2868, 1320))[1])
        write_png(self.image, 2868, 1320)
        self.assertEqual(images.validate(self.image, 'screenshot', (2868, 1320))[1], [])

    def test_corrupt_checksum_rejected(self):
        write_png(self.image)
        data = bytearray(self.image.read_bytes())
        data[29] ^= 1
        self.image.write_bytes(data)
        with self.assertRaisesRegex(ValueError, 'checksum'):
            images.png_info(self.image)

    def test_truncated_structure_rejected(self):
        write_png(self.image)
        self.image.write_bytes(self.image.read_bytes()[:-5])
        with self.assertRaisesRegex(ValueError, 'truncated'):
            images.png_info(self.image)

    def test_non_png_rejected(self):
        self.image.write_bytes(b'not an image')
        with self.assertRaisesRegex(ValueError, 'not a PNG'):
            images.png_info(self.image)


class BundleTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.bundle = Path(self.temp.name) / 'ExampleApp.app'
        self.bundle.mkdir()
        self.info = {'CFBundleIdentifier': 'com.example.app', 'CFBundleExecutable': 'ExampleApp',
                     'CFBundleShortVersionString': '1.0', 'CFBundleVersion': '1',
                     'MinimumOSVersion': '26.0', 'CFBundlePackageType': 'APPL',
                     'UIDeviceFamily': [1], 'ITSAppUsesNonExemptEncryption': False}
        (self.bundle / 'ExampleApp').write_bytes(b'synthetic executable placeholder')
        self.save()

    def save(self):
        (self.bundle / 'Info.plist').write_bytes(plistlib.dumps(self.info))

    def test_valid_structure_is_read_only(self):
        before = {p.name: p.read_bytes() for p in self.bundle.iterdir()}
        errors, warnings = preflight.inspect_bundle(self.bundle)
        self.assertEqual(errors, [])
        self.assertTrue(any('no root privacy manifest' in message for message in warnings))
        self.assertEqual(before, {p.name: p.read_bytes() for p in self.bundle.iterdir()})

    def test_root_resources_problem_detected(self):
        (self.bundle / 'Resources').mkdir()
        self.assertTrue(any('root Resources' in message for message in preflight.inspect_bundle(self.bundle)[0]))

    def test_unresolved_build_setting_detected(self):
        self.info['CFBundleIdentifier'] = '$(PRODUCT_BUNDLE_IDENTIFIER)'
        self.save()
        self.assertTrue(any('resolved' in message for message in preflight.inspect_bundle(self.bundle)[0]))

    def test_missing_executable_detected(self):
        (self.bundle / 'ExampleApp').unlink()
        self.assertIn('declared executable is missing', preflight.inspect_bundle(self.bundle)[0])

    def test_executable_must_not_escape_bundle(self):
        self.info['CFBundleExecutable'] = '../outside'
        self.save()
        self.assertTrue(any('bundle-local' in message for message in preflight.inspect_bundle(self.bundle)[0]))

    def test_malformed_privacy_type_detected(self):
        (self.bundle / 'PrivacyInfo.xcprivacy').write_bytes(plistlib.dumps({'NSPrivacyTracking': 'false'}))
        self.assertIn('NSPrivacyTracking must be a boolean', preflight.inspect_bundle(self.bundle)[0])

    def test_invalid_info_plist_fails(self):
        (self.bundle / 'Info.plist').write_bytes(b'not a plist')
        self.assertTrue(any('cannot read Info.plist' in message for message in preflight.inspect_bundle(self.bundle)[0]))

    def test_truncated_xml_info_fails_cleanly(self):
        (self.bundle / 'Info.plist').write_bytes(b'<?xml version="1.0"?><plist><dict>')
        self.assertIn('cannot read Info.plist: ExpatError', preflight.inspect_bundle(self.bundle)[0])

    def test_truncated_xml_privacy_fails_cleanly(self):
        (self.bundle / 'PrivacyInfo.xcprivacy').write_bytes(b'<?xml version="1.0"?><plist><dict>')
        self.assertIn('cannot read PrivacyInfo.xcprivacy: ExpatError', preflight.inspect_bundle(self.bundle)[0])

    def test_wrong_package_type_detected(self):
        self.info['CFBundlePackageType'] = 'BNDL'
        self.save()
        self.assertIn('CFBundlePackageType must be APPL', preflight.inspect_bundle(self.bundle)[0])


class RepositoryTests(unittest.TestCase):
    def test_wrong_type_url_fails_cleanly(self):
        fixture = json.loads((repository.ROOT / 'templates' / 'app-store-metadata.json').read_text())
        fixture['localizations']['en-US']['privacy_url'] = 123
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / 'templates').mkdir()
            (root / 'templates' / 'app-store-metadata.json').write_text(json.dumps(fixture))
            captured = io.StringIO()
            with mock.patch.object(repository, 'ROOT', root), contextlib.redirect_stdout(captured):
                result = repository.main()
            self.assertEqual(result, 1)
            self.assertIn('metadata structure invalid: TypeError', captured.getvalue())

    def test_invalid_localization_shapes_fail_cleanly(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / 'templates').mkdir()
            metadata = root / 'templates' / 'app-store-metadata.json'
            for invalid in ([], None, 'invalid', {}):
                with self.subTest(shape=invalid):
                    metadata.write_text(json.dumps({'localizations': invalid}))
                    captured = io.StringIO()
                    with mock.patch.object(repository, 'ROOT', root), contextlib.redirect_stdout(captured):
                        result = repository.main()
                    self.assertEqual(result, 1)
                    self.assertIn('metadata structure invalid: ValueError', captured.getvalue())
                    self.assertEqual(list(root.rglob('*.json')), [metadata])


if __name__ == '__main__':
    unittest.main()
