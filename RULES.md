# Engineering & Development Rules (causal-telemetry)

This document establishes the fundamental engineering principles, architecture constraints, and coding standards for this repository. All implementations—whether human or AI-generated—must strictly adhere to these rules.

---

## 1. Core Principles

### 1.1. Python as Default Language
- **Standard:** Python 3.10+ is the official language for all modules, scripts, and pipelines.
- Shell scripts are allowed only for thin automation or environment orchestration (e.g., Docker entrypoints).

### 1.2. English-Only Codebase
- **Standard:** All code, function/variable names, comments, docstrings, commit messages, and documentation within this repository must be written in **English**.
- The only exception is academic reporting/dissertation text when specifically requested in Portuguese.

### 1.3. Radical Simplicity (KISS & YAGNI)
- **Standard:** Avoid writing unnecessary code to solve simple problems.
- Do not create abstract base classes, generic factories, or multi-level inheritance hierarchies unless there are at least three distinct concrete implementations with clear polymorphism needs.
- Prefer simple, pure functions over complex stateful classes whenever state persistence is not required.

### 1.4. Low Cyclomatic Complexity
- **Standard:** Functions must remain concise, focused, and flat.
- Maintain cyclomatic complexity $\le 5$ per function whenever feasible.
- Use **early returns** / guard clauses to avoid deep nesting of `if / else` blocks.
- Aim for functions with fewer than 40 lines of logic. If a function does more, extract sub-functions.

### 1.5. Pragmatic, Essential Testing Only
- **Standard:** Only write tests that are strictly necessary. Avoid test bloat.
- **What to test:**
  - Critical mathematical and statistical routines (e.g., verifying that counterfactual differences match known identities).
  - Data transformation invariants (e.g., ensuring timestamps remain monotonically increasing after downsampling/alignment).
  - Pipeline interface contracts (smoke tests checking that stage outputs match expected column schemas).
- **What NOT to test:**
  - Standard third-party library behavior (e.g., testing that Pandas reads a CSV or that PyTorch runs a forward pass).
  - Trivial getters, setters, or thin wrappers.

---

## 2. Research & Causal Data Science Standards

### 2.1. Strict Reproducibility & Deterministic Seeds
- Every stochastic process (e.g., PCMCI bootstrap tests, MCMC sampling in CausalImpact, train/test splits, permutation tests) **must** accept and propagate an explicit `random_state` / `seed`.
- Global seeds must be centrally configurable.

### 2.2. Vectorized Processing (No Row-by-Row Loops)
- High-frequency telemetry datasets contain millions of rows.
- **Rule:** Never iterate over DataFrame rows using `for index, row in df.iterrows():` or pure Python loops when vectorized operations (`pandas`, `polars`, `numpy`) exist.

### 2.3. Type Hints & Explicit Contracts
- All public functions and pipeline methods must include Python type annotations (`def estimate_effect(data: pd.DataFrame, lag: int) -> CausalResult:`).
- Type hints prevent AI hallucination regressions and keep function contracts explicit.

### 2.4. Pipeline Decoupling & Idempotent Stages
- The pipeline is structured in standalone, decoupled stages:
  1. `ingestion`
  2. `preprocessing`
  3. `discovery`
  4. `inference`
  5. `baselines`
- Each stage must accept files (or DataFrames) as input and write structured intermediate artifacts (e.g., Parquet, JSON, NumPy arrays) to disk.
- You should never have to re-run raw telemetry ingestion just to test a tweak in the counterfactual inference step.

### 2.5. Centralized Configurations (No Magic Numbers)
- Hyperparameters, significance thresholds ($\alpha = 0.05$), lag horizons ($\tau_{\max} = 10$), and dataset paths must live in configuration files (`configs/*.yaml` or config dataclasses).
- Hardcoded constants inside business logic are prohibited.

### 2.6. Lean Dependencies
- Rely on battle-tested domain libraries (e.g., `tigramite`, `statsmodels`, `scipy`, `pandas`) without pulling heavy, unused frameworks.
- Keep requirements clean and minimal.

---

## 3. Directory Structure

```text
causal-telemetry/
├── configs/            # Configuration files (YAML/JSON) for experiments and models
├── data/
│   ├── raw/            # Untouched raw benchmark datasets (ignored by git)
│   └── processed/      # Cleaned, aligned, and sliced telemetry (ignored by git)
├── notebooks/          # Exploratory analysis and visualization notebooks
├── results/
│   ├── figures/        # Generated plots, DAGs, and evaluation curves
│   └── models/         # Serialized SCM models, discovered graphs, and metrics
├── src/
│   ├── ingestion/      # Download, unpack, and parse benchmark datasets (Reveal, etc.)
│   ├── preprocessing/  # Time alignment, resampling, normalization, segmentation
│   ├── discovery/      # Causal discovery engines (PCMCI, Granger, prior constraints)
│   ├── inference/      # SCM formulation, do-calculus, counterfactual estimators
│   ├── baselines/      # Non-causal baselines (ARIMA, LSTM, simple ITSA, static thresholds)
│   └── utils/          # Logging, seed helpers, plotting utilities
├── tests/              # Essential sanity and invariant tests
├── pyproject.toml      # Project metadata and dependencies
└── RULES.md            # This specification file
```
