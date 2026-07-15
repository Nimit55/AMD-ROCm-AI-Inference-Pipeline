# AMD ROCm AI Inference Pipeline

> A reference architecture and deployment scaffold for serving LLMs on AMD Instinct GPUs, using ROCm, vLLM, and Kubernetes.

## Why this exists

Most LLM inference tooling and tutorials assume an NVIDIA/CUDA stack. This project designs the deployment
side of running an LLM inference service on **AMD Instinct GPUs** instead — the Kubernetes deployment
spec, GPU resource scheduling, health checks, and monitoring/benchmarking approach you'd need for a
production ROCm-based serving pipeline.

**Status: architecture and scaffold, not yet run on live hardware.** I don't currently have access to an
AMD Instinct GPU or ROCm cloud credits, so the monitoring, benchmarking, and demo scripts here use
placeholder/simulated data to illustrate the intended output format and workflow — they are not real
measurements. This is called out explicitly in each script (see below) and in this README, rather than
presented as real results.

## What's real vs. simulated

| Component | File | Status |
|---|---|---|
| Kubernetes deployment | `kubernetes/vllm-deployment.yaml` | **Real config** — deploys vLLM on ROCm, requests 1 AMD GPU via `amd.com/gpu`, serves Qwen2-7B-Instruct |
| Health check | `scripts/health_check.sh` | **Real** — checks disk space and RAM availability |
| GPU monitor | `scripts/gpu_monitor.py` | **Simulated** — prints example output format; not wired to `rocm-smi`/`amd-smi` yet |
| Benchmark | `scripts/benchmark.py` | **Simulated** — uses a fixed sample list to demonstrate the p50/p99 reporting format, not measured from live requests |
| Demo | `src/demo.py` | **Simulated** — shows the intended Q&A output format; not calling a live model endpoint |

## Architecture

```
Client
  |
  v
Kubernetes Service (vLLM Deployment)
  |
  v
vLLM pod on AMD Instinct GPU (ROCm backend)
  - Model: Qwen/Qwen2-7B-Instruct
  - GPU: amd.com/gpu resource request (1 GPU)
  |
  v
Monitoring layer (planned): rocm-smi / amd-smi metrics -> dashboard
Benchmarking layer (planned): real request timing -> p50/p99 latency
```

## Components

### Kubernetes deployment (`kubernetes/vllm-deployment.yaml`)
Deploys the `rocm/vllm:latest` image as a single-replica Deployment, requesting one AMD GPU via the
`amd.com/gpu` resource, with the model set via the `MODEL` environment variable.

### Health check (`scripts/health_check.sh`)
Bash script reporting date, Python version, disk space free, and RAM available. Real, functioning checks.

### GPU monitor (`scripts/gpu_monitor.py`)
Prints GPU name, memory, utilization, and temperature in the format a real monitor would report.
**Next step:** replace hardcoded values with real output from `rocm-smi --showuse --showtemp --showmeminfo vram --json`.

### Benchmark (`scripts/benchmark.py`)
Computes and saves p50/p99 latency stats to `results.json`, currently from a fixed sample list.
**Next step:** replace with real request timing against a live vLLM endpoint (e.g. `requests` + `time.perf_counter()`
over 100+ calls), and compute p99 properly from that larger sample rather than `max()` of 10 values.

### Demo (`src/demo.py`)
Prints example Q&A output in the format a live demo would produce.
**Next step:** call the actual vLLM API instead of printing canned text.

## Roadmap to "production-ready"

- [ ] Get access to AMD Instinct GPU (AMD Developer Cloud free credits, or a cloud provider offering MI300X/MI250 instances)
- [ ] Wire `gpu_monitor.py` to real `rocm-smi`/`amd-smi` output
- [ ] Wire `benchmark.py` to real HTTP requests against the deployed vLLM endpoint
- [ ] Wire `demo.py` to the live model API
- [ ] Add Prometheus/Grafana for continuous monitoring
- [ ] Add autoscaling (HPA) based on GPU utilization or queue depth
- [ ] Publish real benchmark numbers once measured

## Setup

```bash
git clone https://github.com/Nimit55/AMD-ROCm-AI-Inference-Pipeline.git
cd AMD-ROCm-AI-Inference-Pipeline
pip install -r requirements.txt
kubectl apply -f kubernetes/vllm-deployment.yaml
```

Requires a Kubernetes cluster with AMD GPU device plugin configured, and access to an AMD Instinct GPU node.

## License

*(add one — MIT is a common default for portfolio projects)*
