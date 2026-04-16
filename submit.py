import datetime
import os
import urllib.request
import json
import hmac
import sys
import hashlib
from datetime import timezone

timestamp = datetime.datetime.now(timezone.utc).isoformat(timespec="milliseconds").replace("+00:00", "Z")

server = os.environ["GITHUB_SERVER_URL"]
repo   = os.environ["GITHUB_REPOSITORY"]
run_id = os.environ["GITHUB_RUN_ID"]

payload = {
    "action_run_link": f"{server}/{repo}/actions/runs/{run_id}",
    "email": "abishekjayan98@gmail.com",
    "name": "Abishek Jayan",
    "repository_link": f"{server}/{repo}",
    "resume_link": os.environ["RESUME_LINK"],
    "timestamp": timestamp,
}

body_bytes = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
secret = os.environ["SIGNING_SECRET"].encode("utf-8")
hex_digest = hmac.new(secret, body_bytes, hashlib.sha256).hexdigest()
signature = f"sha256={hex_digest}"

req = urllib.request.Request(
    url="https://b12.io/apply/submission",
    data=body_bytes,
    headers={
        "Content-Type": "application/json",
        "X-Signature-256": signature,
    },
    method="POST",
)

try:
    with urllib.request.urlopen(req) as resp:
        result = json.loads(resp.read().decode("utf-8"))
        print("Submission successful!")
        print(f"Receipt: {result['receipt']}")
except urllib.error.HTTPError as e:
    print(f"HTTP error {e.code}: {e.read().decode()}", file=sys.stderr)
    sys.exit(1)