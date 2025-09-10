import subprocess, sys, pathlib

def test_cli_help():
    r = subprocess.run([sys.executable, "-m", "redactx.cli", "-h"], capture_output=True, text=True)
    assert r.returncode == 0
    assert "redact" in r.stdout
