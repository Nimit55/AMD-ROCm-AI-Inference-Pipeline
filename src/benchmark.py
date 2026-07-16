"""
Benchmark for the AMD ROCm vLLM inference endpoint.

Sends real requests to a running vLLM server and measures actual latency,
rather than using hardcoded sample data. Requires the vLLM server to be
up and reachable (e.g. via `kubectl port-forward` to the deployment).

Usage:
    python3 benchmark.py --url http://localhost:8000/v1/completions \
        --model Qwen/Qwen2-7B-Instruct --num-requests 100
"""

import argparse
import json
import statistics
import time

import requests


def send_request(url: str, model: str, prompt: str) -> float:
    """Send one completion request and return latency in milliseconds."""
    payload = {
        "model": model,
        "prompt": prompt,
        "max_tokens": 64,
    }
    start = time.perf_counter()
    response = requests.post(url, json=payload, timeout=60)
    response.raise_for_status()
    elapsed_ms = (time.perf_counter() - start) * 1000
    return elapsed_ms


def percentile(data: list, pct: float) -> float:
    """Compute a percentile without requiring numpy."""
    sorted_data = sorted(data)
    idx = int(len(sorted_data) * pct) - 1
    idx = max(0, min(idx, len(sorted_data) - 1))
    return sorted_data[idx]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", required=True, help="vLLM completions endpoint")
    parser.add_argument("--model", required=True, help="Model name as served by vLLM")
    parser.add_argument("--num-requests", type=int, default=100)
    parser.add_argument(
        "--prompt", default="Explain what ROCm is in one sentence.",
        help="Prompt to send for each benchmark request",
    )
    parser.add_argument("--output", default="results.json")
    args = parser.parse_args()

    print("AMD ROCm Benchmark")
    print(f"Endpoint: {args.url}")
    print(f"Model: {args.model}")
    print(f"Requests: {args.num_requests}")
    print("-" * 40)

    latencies = []
    errors = 0
    for i in range(args.num_requests):
        try:
            latency_ms = send_request(args.url, args.model, args.prompt)
            latencies.append(latency_ms)
        except Exception as e:
            errors += 1
            print(f"Request {i + 1} failed: {e}")

    if not latencies:
        print("No successful requests — nothing to report.")
        return

    p50 = statistics.median(latencies)
    p99 = percentile(latencies, 0.99)
    avg = statistics.mean(latencies)

    print("-" * 40)
    print(f"Successful requests: {len(latencies)} / {args.num_requests}")
    print(f"Errors: {errors}")
    print(f"Average latency: {avg:.1f}ms")
    print(f"p50 latency: {p50:.1f}ms")
    print(f"p99 latency: {p99:.1f}ms")

    results = {
        "endpoint": args.url,
        "model": args.model,
        "num_requests": args.num_requests,
        "successful": len(latencies),
        "errors": errors,
        "avg_ms": avg,
        "p50_ms": p50,
        "p99_ms": p99,
        "raw_latencies_ms": latencies,
    }
    with open(args.output, "w") as f:
        json.dump(results, f, indent=2)
    print(f"Saved {args.output}")


if __name__ == "__main__":
    main()
