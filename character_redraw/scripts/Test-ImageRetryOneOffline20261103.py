"""Exercise the installed curl's retry budget against a local fake HTTP server."""
from pathlib import Path
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from threading import Thread
import hashlib
import json
import subprocess

root = Path(__file__).resolve().parents[1]
folder = root / 'art/full_character_redraw_1080p_v01/review/api_retry1_update_20261103_v01/offline_retry_test_v02'
folder.mkdir(exist_ok=False)
seen = {}
payload = b'{"test":"offline-no-image-generation","n":1}'
request = folder / 'request.json'
request.write_bytes(payload)
class Handler(BaseHTTPRequestHandler):
    def do_POST(self):
        body = self.rfile.read(int(self.headers['Content-Length']))
        seen.setdefault(self.path, []).append(hashlib.sha256(body).hexdigest())
        index = len(seen[self.path])
        status = 400 if self.path == '/rejection' else 502 if self.path == '/exhausted' or index == 1 else 200
        response = json.dumps({'status': status, 'attempt': index}).encode()
        self.send_response(status)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Content-Length', str(len(response)))
        self.end_headers()
        self.wfile.write(response)
    def log_message(self, *args):
        pass
server = ThreadingHTTPServer(('127.0.0.1', 0), Handler)
thread = Thread(target=server.serve_forever, daemon=True)
thread.start()
results = []
try:
    for name, expected_requests, expected_status in [('transient', 2, 200), ('rejection', 1, 400), ('exhausted', 2, 502)]:
        response = folder / f'{name}.response.json'
        headers = folder / f'{name}.headers.txt'
        args = ['curl.exe', '--silent', '--show-error', '--retry', '1', '--connect-timeout', '30',
                '--max-time', '900', '--http1.1', '--request', 'POST', '--url',
                f'http://127.0.0.1:{server.server_port}/{name}', '--header', 'Content-Type: application/json',
                '--data-binary', '@' + str(request), '--output', str(response), '--dump-header', str(headers),
                '--write-out', '%{json}']
        run = subprocess.run(args, capture_output=True, text=True, timeout=30)
        (folder / f'{name}.curl_metrics.json').write_text(run.stdout, encoding='utf-8')
        (folder / f'{name}.stderr.txt').write_text(run.stderr, encoding='utf-8')
        metrics = json.loads(run.stdout)
        assert run.returncode == 0 and metrics['http_code'] == expected_status
        assert metrics['num_retries'] == expected_requests - 1
        assert len(seen['/' + name]) == expected_requests
        assert set(seen['/' + name]) == {hashlib.sha256(payload).hexdigest()}
        assert json.loads(response.read_text())['status'] == expected_status
        results.append({'case': name, 'actual_HTTP_requests': len(seen['/' + name]),
                        'actual_retries': metrics['num_retries'], 'final_status': metrics['http_code'],
                        'request_body_identical': True, 'passed': True})
finally:
    server.shutdown()
    server.server_close()
record = {'passed': True, 'scope': 'Installed curl real POST requests to local fake HTTP only',
          'official_API_calls': 0, 'credentials_loaded': False, 'generation_calls': 0, 'cases': results}
(folder / 'RESULT.json').write_text(json.dumps(record, indent=2) + '\n', encoding='utf-8')
print(json.dumps(record))
