# Research handoff

Read README.md, docs/PROTOCOL.es.md, docs/TRAINABLE_CONNECTOME.md and protocol.json first.

Start with the first unchecked roadmap gate. Work locally and economically; reuse audited cached data. This repository is deliberately incomplete. Do not report sample CLI numbers as market evidence or a completed backtest.

Never connect live trading, read credentials, use paid/private RPC fallbacks, or modify the reference strategy. Keep private snapshots and data outside version control. No automatic downloads of the connectome or paid compute before a resource estimate.

Preserve causal time, shared risk/execution and the frozen final test. All changes to hypotheses, datasets, encoders, seeds or evaluation policies belong in the experiment registry. Phase-two training requires matched trainable random controls and an untouched holdout.

Checks: `python -m unittest discover -s tests -v` and `python -m market_lab demo`.
`python -m market_lab preflight` is expected to exit 2 until all prerequisites exist; do not remove this guard to make CI green.

End each research run with status, evidence, limitations, costs and next unmet gate. Do not claim alpha without OOS evidence and adequate controls.
