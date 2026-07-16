"""
GPU Metrics for AMD Instinct GPUs (ROCm)

Queries real GPU stats via `rocm-smi`. Falls back to `amd-smi` if rocm-smi
isn't available. Requires ROCm tools installed and a visible AMD GPU.

Usage:
    python3 metrics.py
"""

import json
import shutil
import subprocess
import sys
from datetime import datetime


def run_rocm_smi():
    """Query GPU stats using rocm-smi's JSON output."""
    cmd = ["rocm-smi", "--showuse", "--showtemp", "--showmeminfo", "vram", "--json"]
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
    if result.returncode != 0:
        raise RuntimeError(f"rocm-smi failed: {result.stderr.strip()}")
    return json.loads(result.stdout)


def run_amd_smi():
    """Fallback: query GPU stats using amd-smi's JSON output."""
    cmd = ["amd-smi", "monitor", "--json"]
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
    if result.returncode != 0:
        raise RuntimeError(f"amd-smi failed: {result.stderr.strip()}")
    return json.loads(result.stdout)


def main():
    timestamp = datetime.now().strftime("%H:%M:%S")
    print(f"GPU Monitor - {timestamp}")

    if shutil.which("rocm-smi"):
        try:
            data = run_rocm_smi()
            print(json.dumps(data, indent=2))
            return
        except Exception as e:
            print(f"rocm-smi query failed: {e}", file=sys.stderr)

    if shutil.which("amd-smi"):
        try:
            data = run_amd_smi()
            print(json.dumps(data, indent=2))
            return
        except Exception as e:
            print(f"amd-smi query failed: {e}", file=sys.stderr)

    print(
        "No ROCm GPU tooling found (rocm-smi / amd-smi). "
        "This script must run on a machine with an AMD Instinct GPU and ROCm installed.",
        file=sys.stderr,
    )
    sys.exit(1)


if __name__ == "__main__":
    main()
