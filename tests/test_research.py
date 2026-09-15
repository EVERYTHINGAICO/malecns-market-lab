import unittest
from market_lab.metrics import summarize
from market_lab.validation import assert_available, purged_train, readiness


class ResearchTests(unittest.TestCase):
    def test_unavailable_features_rejected(self):
        with self.assertRaises(ValueError):
            assert_available(10, [5, 11])
        assert_available(10, [5, 10])

    def test_unknown_availability_rejected(self):
        for times in ([], [None]):
            with self.assertRaises(ValueError):
                assert_available(10, times)

    def test_labels_crossing_validation_are_purged(self):
        rows = [dict(decision_time=1, label_end=5), dict(decision_time=3, label_end=10),
                dict(decision_time=11, label_end=12)]
        self.assertEqual(purged_train(rows, 10), rows[:1])

    def test_invalid_label_interval(self):
        with self.assertRaises(ValueError):
            purged_train([dict(decision_time=5, label_end=2)], 10)

    def test_incomplete_protocol_is_not_ready(self):
        self.assertIn('capital', readiness(dict(live_trading=False, private_rpc_allowed=False)))

    def test_live_or_private_access_rejected(self):
        for spec in ({}, dict(live_trading=True, private_rpc_allowed=False),
                     dict(live_trading=False, private_rpc_allowed=True)):
            with self.assertRaises(ValueError):
                readiness(spec)

    def test_metrics_drawdown_and_trade_ledger(self):
        m = summarize([100, 110, 105, 105, 108], [10, -5, 0, 3], risk_per_trade=[5, 5, 5, 3])
        self.assertEqual(m['net_pnl'], 8)
        self.assertAlmostEqual(m['max_drawdown_pct'], 100 * 5 / 110)
        self.assertEqual(m['expectancy'], 2)
        self.assertEqual(m['win_rate'], .5)
        self.assertEqual(m['profit_factor'], 2.6)
        self.assertEqual(m['mean_r_multiple'], .5)

    def test_no_trades_or_variance_is_undefined(self):
        m = summarize([100, 100, 100], [])
        for key in ('profit_factor', 'win_rate', 'sharpe', 'sortino', 'expectancy', 'mean_r_multiple'):
            self.assertIsNone(m[key])

    def test_initial_risk_cannot_be_invented(self):
        with self.assertRaises(ValueError):
            summarize([100, 99], [-1], risk_per_trade=[0])

    def test_bad_equity_rejected(self):
        with self.assertRaises(ValueError):
            summarize([100, float('nan')], [])


if __name__ == '__main__':
    unittest.main()
