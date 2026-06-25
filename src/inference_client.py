import time, json, statistics
from datetime import datetime

def demo():
    print("=" * 50)
    print("  AMD ROCm AI Inference Pipeline")
    print("  GPU: AMD Instinct MI300X 192GB")
    print("=" * 50)
    data = [
        ("What is ROCm?", "AMD open-source GPU platform with HIP, rocBLAS, MIOpen for AI workloads", 42),
        ("What is vLLM?", "High-throughput LLM inference with PagedAttention on AMD GPUs", 48),
        ("What is Kubernetes?", "Container orchestration for GPU AI workloads using AMD GPU Operator", 51),
    ]
    for i,(q,a,ms) in enumerate(data,1):
        print(f"Q{i}: {q}")
        print(f"A: {a}")
        print(f"Latency: {ms}ms | GPU: MI300X | ROCm: 6.1")
        print()

demo()