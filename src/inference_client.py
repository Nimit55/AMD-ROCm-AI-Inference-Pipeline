"""
Inference client for the AMD ROCm AI Inference Pipeline.

Sends real questions to the running vLLM endpoint and prints the actual
model responses and measured latency, rather than printing canned text.

Usage:
    python3 inference_client.py --url http://localhost:8000/v1/completions \
        --model Qwen/Qwen2-7B-Instruct
"""

import argparse
import time

import requests

QUESTIONS = [
    "What is ROCm?",
    "What is vLLM?",
    "What is Kubernetes?",
]


def ask(url: str, model: str, question: str):
    payload = {
        "model": model,
        "prompt": question,
        "max_tokens": 100,
    }
    start = time.perf_counter()
    response = requests.post(url, json=payload, timeout=60)
    response.raise_for_status()
    latency_ms = (time.perf_counter() - start) * 1000
    answer = response.json()["choices"][0]["text"].strip()
    return answer, latency_ms


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", required=True, help="vLLM completions endpoint")
    parser.add_argument("--model", required=True, help="Model name as served by vLLM")
    args = parser.parse_args()

    print("=" * 50)
    print("  AMD ROCm AI Inference Pipeline — Inference Client")
    print(f"  Model: {args.model}")
    print("=" * 50)

    for i, question in enumerate(QUESTIONS, 1):
        try:
            answer, latency_ms = ask(args.url, args.model, question)
        except Exception as e:
            print(f"Q{i}: {question}")
            print(f"  Request failed: {e}\n")
            continue

        print(f"Q{i}: {question}")
        print(f"A: {answer}")
        print(f"Latency: {latency_ms:.1f}ms\n")


if __name__ == "__main__":
    main()
