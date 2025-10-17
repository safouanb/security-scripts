# tools/ssl_check.py
# Lightweight SSL check -> outputs JSON (safe, non-exploitative)
import subprocess, json, sys

def run_openssl(host):
    cmd = ["openssl", "s_client", "-connect", f"{host}:443", "-servername", host]
    p = subprocess.run(cmd, capture_output=True, text=True)
    return p.stdout + p.stderr

def parse_and_output(host):
    raw = run_openssl(host)
    ok = "Verify return code: 0 (ok)" in raw
    out = {
        "host": host,
        "valid_chain": ok,
        "snippet": raw.replace("\\n", " ")[:2000]
    }
    print(json.dumps(out, indent=2))

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python ssl_check.py example.com")
        sys.exit(1)
    parse_and_output(sys.argv[1])
