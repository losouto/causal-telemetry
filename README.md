# Causal Telemetry Framework

Benchmark-driven causal inference framework on multivariate hardware telemetry time series to estimate operational interventions and counterfactual execution times in compute workloads.

Based on dissertation research by Leandro de Oliveira Souto.

---

## Architecture Overview

```text
src/
├── ingestion/      # Download and parse benchmark datasets (Reveal Hardware Telemetry)
├── preprocessing/  # Timestamp alignment, resample, normalize, window segmentation
├── discovery/      # Temporal causal discovery (PCMCI, Granger) with domain constraints
├── inference/      # SCM formulation, do-calculus, counterfactual estimation
├── baselines/      # Non-causal baselines (ARIMA, ITSA, static heuristics)
└── utils/          # Common helpers, logging, metrics, determinism
```

## Getting Started

1. **Review Rules & Standards:**
   Consult [`RULES.md`](RULES.md) for architecture rules, code simplicity principles, and testing guidelines.

2. **Environment Setup:**
   ```bash
   pip install -e .
   ```

3. **Running Essential Tests:**
   ```bash
   pytest tests/
   ```
