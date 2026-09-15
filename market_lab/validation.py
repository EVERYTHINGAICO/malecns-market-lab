"""Fail-closed preregistration and information-availability checks."""
REQUIRED = (
    'baseline_sha256', 'dataset_manifest_sha256', 'actual_date_boundaries',
    'capital', 'risk_policy_sha256', 'execution_policy_sha256',
    'cost_model_sha256', 'minimum_practical_effect',
    'max_label_horizon_seconds', 'max_feature_lookback_seconds',
    'hypothesis_registry_sha256',
)


def readiness(spec):
    if spec.get('live_trading') is not False:
        raise ValueError('Live trading must be explicitly disabled')
    if spec.get('private_rpc_allowed') is not False:
        raise ValueError('Private RPC must be explicitly disabled')
    return [key for key in REQUIRED if spec.get(key) is None]


def assert_available(decision_time, available_times):
    if not available_times:
        raise ValueError('Missing feature provenance')
    if any(t is None or t > decision_time for t in available_times):
        raise ValueError('Feature unavailable at decision time')


def purged_train(records, validation_start):
    """Only past observations whose complete label interval ends before validation.

    Records: decision_time, label_end. Timestamps use the same UTC units.
    Split/embargo dates must be supplied externally, not selected by this helper.
    """
    if any(r['label_end'] < r['decision_time'] for r in records):
        raise ValueError('Invalid label interval')
    return [r for r in records
            if r['decision_time'] < validation_start
            and r['label_end'] < validation_start]
