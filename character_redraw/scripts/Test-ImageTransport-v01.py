"""Unauthenticated, non-generating official endpoint probes; never use API keys."""
import json
import subprocess
import time
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'art/full_character_redraw_1080p_v01/coverage/decisions/transport_probe_20261031_v01.json'


def main():
    if OUT.exists():
        raise RuntimeError('Probe evidence already exists; inspect it instead of overwriting.')
    choices = [
        Path(r'C:\Windows\System32\curl.exe'),
        Path(r'C:\Program Files\Git\mingw64\bin\curl.exe'),
    ]
    records = []
    for binary in choices:
        if not binary.is_file():
            continue
        version = subprocess.check_output([str(binary), '--version'], text=True, encoding='utf-8').splitlines()[0]
        for i in range(3):
            start = time.monotonic()
            proc = subprocess.run([
                str(binary), '--silent', '--show-error', '--retry', '0',
                '--connect-timeout', '10', '--max-time', '20', '--http1.1',
                '--request', 'GET', '--url', 'https://api.openai.com/v1/models',
                '--output', 'NUL', '--write-out', '%{http_code}'
            ], capture_output=True, text=True, encoding='utf-8')
            record = {'binary': str(binary), 'version': version, 'probe': i + 1,
                      'http_status': proc.stdout.strip(), 'exit_code': proc.returncode,
                      'elapsed_seconds': round(time.monotonic() - start, 3),
                      'error': proc.stderr.strip(),
                      'TLS_to_official_endpoint_received_HTTP_response': proc.returncode == 0 and proc.stdout.strip() != '000'}
            records.append(record)
            print(json.dumps(record, ensure_ascii=False), flush=True)
    result = {'utc': datetime.now(timezone.utc).isoformat(),
              'endpoint': 'https://api.openai.com/v1/models',
              'scope': 'Unauthenticated GET only. HTTP401 is expected; proves transport for this probe, not API authentication, billing or image generation.',
              'image_generation_calls': 0, 'credentials_used': False,
              'certificate_validation_disabled': False, 'records': records}
    OUT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


if __name__ == '__main__':
    main()
