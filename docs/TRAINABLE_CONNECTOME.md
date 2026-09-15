# Phase two: can training the fly improve the strategy?

This is a separate preregistered experiment, not a silent modification of frozen arm C. The primary target is a filter on the existing strategy's entries. Its stops, sizes and exits remain unchanged.

## Matched arms

- **E:** MaleCNS initialization with a constrained trainable parameterization, then the same readout.
- **F:** randomized initialization/control with the identical trainable parameterization and readout.
- Retain frozen C/D and simple B. An additional small recurrent model is a useful secondary compute baseline.

Choose a parameterization before testing: for example, low-rank updates or fixed-group gains. Record which parameters can change, their count, rank, masks and constraints. Apply the same parameter count, optimizer, update count, data, loss, regularization, early-stopping rule, seed schedule and hyperparameter search budget to E and F. If the implementation is not differentiable, use a validated training method and budget its search equally; do not assume gradients exist through a spiking simulator.

Do not compare an extensively tuned E with an untuned F. Preserve sign constraints consistently where applicable. Archive initialization and final weights; measure how far the trained network departs from the original connectome. A heavily rewired trained network is not evidence that an untouched biological brain predicts prices.

## Labels and causality

Train on the net outcome of the reference entry under its frozen risk and execution rules, using only matured labels. Train/validation/test remain chronological with purging. Threshold calibration happens in validation, never test. If online updates are tested, register their schedule; only outcomes already known at the update time are available.

## Attribution

1. E > C: training helps this representation, not necessarily biological wiring.
2. E > F under matched budgets: evidence for biological initialization or constraints, conditional on the tested null.
3. A+E > A and alternative filters OOS: evidence for practical filtering utility.
4. E ≈ F: no specific justification for biological initialization, even if both learn useful patterns.

All comparisons count in the experiment registry and multiple-testing family. If phase one has already revealed final-test outcomes, phase two needs a new untouched test period. Do not reuse it as confirmatory evidence.

Resource gate: first validate the data, execution engine and baseline, then benchmark compute. No paid infrastructure or real orders are part of this phase.
