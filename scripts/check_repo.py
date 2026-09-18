#!/usr/bin/env python3
"""Read-only local links, JSON and generic sensitive-content checks for this playbook."""
import json
import re
import sys
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
SKIP = {'.git', '__pycache__', '.pytest_cache', 'private', 'artifacts'}
ALLOWED_SUFFIXES = {'.md', '.json', '.py'}
FORBIDDEN_SUFFIXES = {'.p8', '.p12', '.pfx', '.cer', '.key', '.pem', '.mobileprovision', '.provisionprofile', '.ipa', '.m4a', '.caf', '.wav', '.mp3', '.mov', '.mp4'}
ALLOWED_SPECIAL = {'.gitignore', 'LICENSE'}
PATTERNS = {
    'private-key material': r'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----',
    'AWS access-key-shaped value': r'\b(?:AKIA|ASIA)[A-Z0-9]{16}\b',
    'GitHub token-shaped value': r'\b(?:ghp|gho|ghu|ghs|ghr)_[A-Za-z0-9]{20,}\b',
    'local user-home path': r'/(?:Users|home)/[A-Za-z0-9_.-]+/',
    'IPv4 address': r'(?<![\d.])(?:\d{1,3}\.){3}\d{1,3}(?![\d.])',
    'device-identifier-shaped value': r'\b[0-9A-Fa-f]{8}-[0-9A-Fa-f]{16}\b',
}


def collect_files():
    for path in sorted(ROOT.rglob('*')):
        rel = path.relative_to(ROOT)
        if any(part in SKIP for part in rel.parts):
            continue
        if path.is_symlink() or path.is_file():
            yield path


def main():
    errors = []
    paths = list(collect_files())
    for path in paths:
        rel = path.relative_to(ROOT)
        if path.is_symlink():
            errors.append(f'{rel}: symlinks need explicit manual review; not permitted here')
            continue
        if path.suffix in FORBIDDEN_SUFFIXES or (path.suffix not in ALLOWED_SUFFIXES and path.name not in ALLOWED_SPECIAL):
            errors.append(f'{rel}: unexpected or sensitive file type')
            continue
        try:
            content = path.read_text(encoding='utf-8')
        except (UnicodeError, OSError):
            errors.append(f'{rel}: cannot inspect as UTF-8 text')
            continue
        for label, pattern in PATTERNS.items():
            if re.search(pattern, content):
                errors.append(f'{rel}: possible {label}; inspect privately')
        for email in re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b', content):
            if not email.lower().endswith('@example.com'):
                errors.append(f'{rel}: non-example email address; inspect privately')
        if path.suffix == '.json':
            try:
                json.loads(content)
            except json.JSONDecodeError as error:
                errors.append(f'{rel}: invalid JSON at line {error.lineno}')
        if path.suffix == '.md':
            for target in re.findall(r'(?<!!)\[[^\]]*\]\(([^\s)]+)\)', content):
                parts = urlsplit(target.strip('<>'))
                if parts.scheme or parts.netloc or not parts.path:
                    continue
                local = (path.parent / unquote(parts.path)).resolve()
                try:
                    local.relative_to(ROOT)
                except ValueError:
                    errors.append(f'{rel}: local link escapes repository')
                    continue
                if not local.exists():
                    errors.append(f'{rel}: broken local link to {parts.path}')
    metadata_path = ROOT / 'templates/app-store-metadata.json'
    try:
        metadata = json.loads(metadata_path.read_text())
        localizations = metadata['localizations']
        if not isinstance(localizations, dict) or not localizations:
            raise ValueError('localizations must be a nonempty dictionary')
        for locale, values in localizations.items():
            for field, limit in {'name': 30, 'subtitle': 30, 'promotional_text': 170, 'keywords': 100, 'description': 4000}.items():
                value = values[field]
                if not isinstance(value, str) or not value or len(value) > limit:
                    errors.append(f'metadata {locale}/{field}: empty, invalid or longer than {limit} characters')
            for field in ('support_url', 'privacy_url', 'marketing_url'):
                if not isinstance(values[field], str):
                    raise TypeError('metadata URL must be a string')
                url = urlsplit(values[field])
                if url.scheme != 'https' or url.hostname != 'example.com':
                    errors.append(f'metadata {locale}/{field}: template must use HTTPS example.com')
    except (OSError, ValueError, KeyError, TypeError) as error:
        errors.append(f'metadata structure invalid: {type(error).__name__}')
    for error in errors:
        print(f'FAIL: {error}')
    if not errors:
        print(f'PASS: {len(paths)} text files; local link targets, JSON, metadata limits and generic privacy scan checked.')
    print('Manual review remains required, including hidden files, git identity/history, account identifiers and source context.')
    print('External links, Markdown anchors and legal/privacy accuracy are not established by this script.')
    return 1 if errors else 0


if __name__ == '__main__':
    sys.exit(main())
