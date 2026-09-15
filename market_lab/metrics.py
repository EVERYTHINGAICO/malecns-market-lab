"""Small audited metric primitives, not a fill simulator or backtest engine."""
from math import sqrt, isfinite
from statistics import mean, stdev


def summarize(equity, closed_net_pnl, *, periods_per_year=365, risk_per_trade=None):
    """Equally spaced equity, including idle periods; no deposits or withdrawals.

    Returns Sharpe/Sortino with zero benchmark/MAR. PnL must already include ALL
    costs. Missing/undefined ratios are None, never fabricated as zero or infinity.
    These assumptions are examples; the financial experiment must freeze its own
    benchmark and policies before using these primitives.
    """
    if len(equity) < 2 or any(not isfinite(v) or v <= 0 for v in equity):
        raise ValueError('At least two finite positive equity observations required')
    if any(not isfinite(v) for v in closed_net_pnl):
        raise ValueError('Non-finite trade PnL')
    if not isfinite(periods_per_year) or periods_per_year <= 0:
        raise ValueError('Invalid annualization')
    returns = [b / a - 1 for a, b in zip(equity, equity[1:])]
    peak, max_dd = equity[0], 0.0
    for value in equity:
        peak = max(peak, value)
        max_dd = max(max_dd, 1 - value / peak)
    wins = [x for x in closed_net_pnl if x > 0]
    losses = [x for x in closed_net_pnl if x < 0]
    sigma = stdev(returns) if len(returns) > 1 else 0
    downside = sqrt(mean(min(x, 0) ** 2 for x in returns))
    r_mean = None
    if risk_per_trade is not None:
        if len(risk_per_trade) != len(closed_net_pnl):
            raise ValueError('Risk and trade lengths differ')
        if any(not isfinite(v) or v <= 0 for v in risk_per_trade):
            raise ValueError('Initial risk must be positive and finite')
        r_mean = mean(p / r for p, r in zip(closed_net_pnl, risk_per_trade)) if closed_net_pnl else None
    return dict(
        net_pnl=equity[-1] - equity[0], return_pct=100 * (equity[-1] / equity[0] - 1),
        max_drawdown_pct=100 * max_dd,
        sharpe=mean(returns) / sigma * sqrt(periods_per_year) if sigma else None,
        sortino=mean(returns) / downside * sqrt(periods_per_year) if downside else None,
        profit_factor=sum(wins) / abs(sum(losses)) if losses else None,
        win_rate=len(wins) / len(closed_net_pnl) if closed_net_pnl else None,
        average_win=mean(wins) if wins else None, average_loss=mean(losses) if losses else None,
        expectancy=mean(closed_net_pnl) if closed_net_pnl else None,
        trades=len(closed_net_pnl), break_even_trades=sum(x == 0 for x in closed_net_pnl),
        mean_r_multiple=r_mean,
    )
