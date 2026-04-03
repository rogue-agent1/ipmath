#!/usr/bin/env python3
"""Tests for ipmath."""
import subprocess, sys

def run(args):
    r = subprocess.run([sys.executable, "ipmath.py"] + args, capture_output=True, text=True)
    return r.stdout, r.returncode

def test_info_v4():
    out, rc = run(["info", "192.168.1.0/24"])
    assert rc == 0
    assert "255.255.255.0" in out
    assert "254" in out
    assert "192.168.1.255" in out

def test_info_v6():
    out, rc = run(["info", "2001:db8::/32"])
    assert rc == 0
    assert "IPv6" in out
    assert "ffff:ffff::" in out

def test_contains_yes():
    out, rc = run(["contains", "10.0.0.0/8", "10.5.3.1"])
    assert "Yes" in out

def test_contains_no():
    out, rc = run(["contains", "10.0.0.0/8", "192.168.1.1"])
    assert "NOT in" in out

def test_add():
    out, rc = run(["add", "192.168.1.1", "100"])
    assert "192.168.1.101" in out

def test_range():
    out, rc = run(["range", "192.168.1.0/30"])
    lines = out.strip().split("\n")
    assert len(lines) == 4
    assert "192.168.1.0" in lines[0]
    assert "192.168.1.3" in lines[3]

def test_single_ip():
    out, rc = run(["info", "8.8.8.8"])
    assert "8.8.8.8" in out
    assert "/32" in out

if __name__ == "__main__":
    tests = [f for f in dir() if f.startswith("test_")]
    for t in tests:
        globals()[t]()
        print(f"  ✓ {t}")
    print(f"\n{len(tests)} tests passed")
