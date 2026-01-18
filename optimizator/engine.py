import numpy as np
import pandas as pd
from scipy.optimize import minimize
from risk.risk_metrics import (
    ann_factor,
    portfolio_returns,
    risk_contributions,
    max_drawdown,
    cvar_historical,
)


def weight_constraints(n):
    # Fully invested (sum = 1), long-only (0 <= w <= 1)
    cons = ({"type": "eq", "fun": lambda w: np.sum(w) - 1.0},)
    bounds = [(0.0, 1.0)] * n
    return cons, bounds


def initial_weights(n):
    return np.ones(n) / n


def optimize_min_vol(returns_df: pd.DataFrame, freq="D"):
    n = returns_df.shape[1]
    cov = returns_df.cov().values * ann_factor(freq)

    def obj(w):
        return np.sqrt(w @ cov @ w)

    cons, bounds = weight_constraints(n)
    res = minimize(
        obj, initial_weights(n), method="SLSQP", bounds=bounds, constraints=cons
    )
    return res.x


def optimize_max_sharpe(returns_df: pd.DataFrame, freq="D", rf=0.0):
    n = returns_df.shape[1]
    mu = returns_df.mean().values * ann_factor(freq)
    cov = returns_df.cov().values * ann_factor(freq)

    def neg_sharpe(w):
        port_ret = w @ mu
        port_vol = np.sqrt(w @ cov @ w)
        if port_vol == 0:
            return 1e9
        return -(port_ret - rf) / port_vol

    cons, bounds = weight_constraints(n)
    res = minimize(
        neg_sharpe, initial_weights(n), method="SLSQP", bounds=bounds, constraints=cons
    )
    return res.x


def optimize_risk_parity(returns_df: pd.DataFrame, freq="D"):
    n = returns_df.shape[1]
    cov = returns_df.cov().values * ann_factor(freq)

    # Need to import risk_contributions locally or helper above?
    # Helper defined below to act consistently
    def get_rc(w, cov_matrix):
        port_var = w @ cov_matrix @ w
        port_vol = np.sqrt(port_var) if port_var > 0 else 1e-9
        mrc = cov_matrix @ w
        return (w * mrc) / port_vol

    def obj(w):
        rc = get_rc(w, cov)
        target = np.mean(rc)
        return np.sum((rc - target) ** 2)

    cons, bounds = weight_constraints(n)
    res = minimize(
        obj, initial_weights(n), method="SLSQP", bounds=bounds, constraints=cons
    )
    return res.x


def optimize_with_profile(returns_df: pd.DataFrame, profile, freq="D"):
    """
    Optimize portfolio based on a RiskProfile.
    Selects the strategy that best fits the profile's volatility/drawdown constraints
    and applies asset allocation limits.
    """
    # This is a simplified logic:
    # 1. If Conservative, use MinVol.
    # 2. If Moderate, use RiskParity.
    # 3. If Aggressive, use MaxSharpe.

    if profile.label == "Conservative":
        return optimize_min_vol(returns_df, freq)
    elif profile.label == "Aggressive":
        return optimize_max_sharpe(returns_df, freq=freq, rf=0.04)
    else:
        return optimize_risk_parity(returns_df, freq)
