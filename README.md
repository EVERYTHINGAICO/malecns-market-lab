# MaleCNS Market Lab

**An Everything AI research project testing whether biological connectivity adds useful market information.**

> Status: preregistration and research scaffolding. **No demonstrated trading alpha. No live trading.** Current integration decision: **NEED MORE DATA**.

The question is not whether a simulated fly can produce trading signals. It is whether those signals add predictive or economic value beyond a simple learned baseline and equivalent random networks, on unseen data and under the same execution constraints.

## Experimental design

| Arm | Signal source | Purpose |
|---|---|---|
| A | Existing strategy, frozen | Unmodified reference |
| B | Market history → simple readout | Learnable baseline without a connectome |
| C | Market history → frozen MaleCNS → trained readout | Test biological reservoir representation |
| D / D2 | Comparable randomized reservoirs → identical readout | Separate biological wiring from generic reservoir capacity |
| A + C | Existing entries accepted only when C agrees | Test incremental filtering value |
| E / F, phase two | Trainable MaleCNS / equally trainable random network | Test whether biological initialization helps learning |

All arms share the universe, timestamps, available information, capital, execution model, costs and risk policy. Filter controls include A+B, A+D and random rejection at comparable retention rates. Both winners and losers remain in the study.

## What exists today

- A detailed [Spanish experimental protocol](docs/PROTOCOL.es.md).
- A machine-readable [draft specification](protocol.json), with unresolved inputs explicitly marked `null`.
- A [controlled trainable-connectome extension](docs/TRAINABLE_CONNECTOME.md).
- Tested primitives for information availability, label-interval purging and financial metrics.
- A synthetic CLI demonstration and CI tests.
- A staged [roadmap](docs/ROADMAP.md) and [research handoff](AGENTS.md).

**Not implemented:** baseline replay adapter, real market dataset, fill simulator, model training, reservoir construction, walk-forward runner, bootstrap inference or live execution. The primitives are not a completed backtest engine. Tests establish software behavior, not investment performance.

## Quick start

Python 3.12+, no third-party dependencies for the scaffolding:

```bash
python -m unittest discover -s tests -v
python -m market_lab demo
python -m market_lab preflight
```

`demo` prints **synthetic** metrics, not a trading result. `preflight` intentionally exits with code **2** while the scientific prerequisites are incomplete. Supplying fields later will not by itself validate their scientific content.

## Scientific safeguards

1. Preregister hypotheses, practical effect size, model budgets, seeds and splits before opening the final test.
2. Use chronological train/validation/test and purged walk-forward validation. Fit preprocessing only within training windows.
3. Keep per-token reservoir state causal; do not leak future samples through reset/warm-up or cross-token state reuse.
4. Match random controls in capacity, inputs, dynamics and training budget. Do not choose a weak random seed as the comparator.
5. Compare paired out-of-sample returns with temporal dependence and multiple comparisons accounted for.
6. Report uncertainty, drawdown, exposure, missed winners, rejected losers, regime stability and compute latency—not just P&L.
7. Publish negative findings and corrections. Never relabel an inspected test set as untouched OOS.

The initial market context is Pons V2 on Robinhood Chain. Executable shorts and hypothetical dividend allocations are **not established**. Unsupported short P&L and R-multiples without a defined initial stop risk must remain N/A. Unknown dividend entitlement must not become fabricated income.

## Decision criteria

A positive biological claim requires beating both the simple baseline and suitable randomized controls OOS. A positive filter claim requires beating the unchanged strategy **and** alternative filters at comparable risk/exposure.

The final decision must be one of `YES`, `NO`, `ONLY AS FILTER`, or `NEED MORE DATA`, supported by the evidence and limitations in the preregistered protocol. A failure to reject a null is not automatically evidence of equivalence.

See the [results register](reports/RESULTS.md). No market performance is reported yet.

## Provenance and attribution

- [MaleCNS dataset, Janelia/FlyEM](https://male-cns.janelia.org/): biological connectivity data, separately licensed. Not redistributed here.
- [fly.ai](https://github.com/alextitonis/fly.ai), reference commit `0aa078055f7a975075ba5baf1156430f9e606356`: candidate simulation implementation. No upstream code is vendored. Its default readout cross-validation is not appropriate for causal financial validation without replacement.
- [Deflated Sharpe Ratio, Bailey & López de Prado](https://www.davidhbailey.com/dhbpapers/deflated-sharpe.pdf): additional selection-bias diagnostic; not a substitute for OOS tests.

Independent research by **Everything AI**. Not affiliated with or endorsed by the upstream projects. Private strategy code, account data, credentials and raw market captures are excluded from this repository.

Original scaffolding is MIT licensed; third-party data/software retain their own licenses.
