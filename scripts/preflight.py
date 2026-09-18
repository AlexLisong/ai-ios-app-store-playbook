#!/usr/bin/env python3
"""Read-only iOS .app structure/plist checks. Does not sign or contact Apple."""
import argparse
import plistlib
import re
import sys
from pathlib import Path
from xml.parsers.expat import ExpatError


def read_plist(path):
    with Path(path).open('rb') as stream:
        value = plistlib.load(stream)
    if not isinstance(value, dict):
        raise ValueError('plist root must be a dictionary')
    return value


def inspect_bundle(bundle):
    bundle = Path(bundle)
    errors, warnings = [], []
    if not bundle.is_dir() or bundle.suffix != '.app':
        return ['provide an existing .app directory'], warnings
    if (bundle / 'Resources').exists():
        errors.append('root Resources directory can confuse iOS bundle classification; inspect copied resource layout')
    try:
        info = read_plist(bundle / 'Info.plist')
    except (OSError, ValueError, plistlib.InvalidFileException, ExpatError) as error:
        return errors + [f'cannot read Info.plist: {type(error).__name__}'], warnings
    for field in ('CFBundleIdentifier', 'CFBundleExecutable', 'CFBundleShortVersionString', 'CFBundleVersion', 'MinimumOSVersion'):
        value = info.get(field)
        if not isinstance(value, str) or not value.strip() or '$(' in value or '${' in value:
            errors.append(f'{field} must contain a resolved nonempty string')
    identifier = info.get('CFBundleIdentifier', '')
    if isinstance(identifier, str) and identifier and not re.fullmatch(r'[A-Za-z0-9-]+(?:\.[A-Za-z0-9-]+)+', identifier):
        errors.append('CFBundleIdentifier has an unexpected format')
    if info.get('CFBundlePackageType') != 'APPL':
        errors.append('CFBundlePackageType must be APPL')
    executable = info.get('CFBundleExecutable')
    if isinstance(executable, str) and executable and '/' not in executable and executable not in ('.', '..'):
        if not (bundle / executable).is_file():
            errors.append('declared executable is missing')
    else:
        errors.append('CFBundleExecutable must be a bundle-local filename')
    families = info.get('UIDeviceFamily')
    if not isinstance(families, list) or not families or any(type(item) is not int for item in families):
        errors.append('UIDeviceFamily must be a nonempty integer array')
    if 'ITSAppUsesNonExemptEncryption' not in info:
        warnings.append('export-compliance declaration absent; answer accurately during release if required')
    privacy_path = bundle / 'PrivacyInfo.xcprivacy'
    if privacy_path.exists():
        try:
            privacy = read_plist(privacy_path)
            if 'NSPrivacyTracking' in privacy and type(privacy['NSPrivacyTracking']) is not bool:
                errors.append('NSPrivacyTracking must be a boolean')
            for key in ('NSPrivacyCollectedDataTypes', 'NSPrivacyAccessedAPITypes', 'NSPrivacyTrackingDomains'):
                if key in privacy and not isinstance(privacy[key], list):
                    errors.append(f'{key} must be an array')
        except (OSError, ValueError, plistlib.InvalidFileException, ExpatError) as error:
            errors.append(f'cannot read PrivacyInfo.xcprivacy: {type(error).__name__}')
    else:
        warnings.append('no root privacy manifest found; assess current app/SDK/API requirements rather than assuming exemption')
    warnings.append('manually inspect icons, permission localization, embedded frameworks, entitlements, signing and data-flow disclosures')
    return errors, warnings


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('bundle', type=Path)
    args = parser.parse_args()
    errors, warnings = inspect_bundle(args.bundle)
    for message in errors:
        print(f'FAIL: {message}')
    for message in warnings:
        print(f'REVIEW: {message}')
    if not errors:
        print('PASS: basic bundle checks only; this is not signing validation or App Review approval.')
    return 1 if errors else 0


if __name__ == '__main__':
    sys.exit(main())
