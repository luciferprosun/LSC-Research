# Compute Limitations

Target runtime profile:

- dual-core CPU,
- low RAM,
- no high-VRAM GPU.

## Constraints

1. Prefer pure-Python + stdlib where possible.
2. Keep dependency stack minimal.
3. Avoid dense matrix operations unless strictly required.
4. No large framework dependency unless benchmark-justified.
5. Split heavy tasks into deferred/offline stages.

## Implementation policy

- Baseline runner must complete on CPU in lightweight mode.
- Notebook templates must run without GPU assumptions.
- Data loaders should stream/parse incrementally where possible.
- Plots and reports should be generated from processed snapshots, not raw heavy joins.

## Deferred heavy-compute policy

Allowed to postpone:

- global scans over large parameter grids,
- full covariance Monte Carlo with large sampling,
- expensive Bayesian chains.

These tasks must have placeholders and interfaces now, and can be migrated
to stronger hardware later without breaking baseline workflows.
