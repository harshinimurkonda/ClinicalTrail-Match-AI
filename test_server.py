"""Test live server startup and HTTP response."""
import subprocess
import time
import urllib.request
import json
import sys

def probe():
    proc = subprocess.Popen([sys.executable, "run.py"], cwd=r"C:\Users\HARSHINI\.gemini\antigravity\scratch\clinical-trial-match-ai")
    try:
        time.sleep(2.5)
        # Check health
        req = urllib.request.Request("http://127.0.0.1:5000/api/health")
        with urllib.request.urlopen(req, timeout=5) as resp:
            data = json.loads(resp.read().decode())
            print("Server /api/health returned:")
            print(json.dumps(data, indent=2))
        
        # Check index html
        req_index = urllib.request.Request("http://127.0.0.1:5000/")
        with urllib.request.urlopen(req_index, timeout=5) as resp_index:
            html = resp_index.read().decode()
            print(f"Index HTML fetched successfully: {len(html)} bytes, title found: {'ClinicalTrial Match AI' in html}")
    finally:
        proc.terminate()
        proc.wait(timeout=5)
        print("Live server process terminated cleanly.")

if __name__ == "__main__":
    probe()
