import numpy as np
import pandas as pd


def ann_factor(freq: str) -> int:
    """
    Get the annualization factor for a given frequency.

    Args:
        freq (str): Frequency string ('D' for Daily, 'W' for Weekly, 'M' for Monthly).

    Returns:
        int: Annualization factor (252, 52, or 12).
    """
    if freq == "D":
        return 252
    if freq == "W":
        return 52
    if freq == "M":
        return 12
    raise ValueError("freq must be D/W/M")


def portfolio_returns(returns: pd.DataFrame, w: np.ndarray) -> pd.Series:
    """
    Calculate the time series of portfolio returns given weights.

    Args:
        returns (pd.DataFrame): Asset returns.
        w (np.ndarray): Portfolio weights.

    Returns:
        pd.Series: Portfolio returns.
    """
    return returns @ w


def annualized_vol(returns: pd.Series, freq="D") -> float:
    """
    Calculate the annualized volatility (standard deviation) of returns.

    Formula: std(returns) * sqrt(annualization_factor)
    """
    af = ann_factor(freq)
    return returns.std(ddof=1) * np.sqrt(af)


def annualized_return(returns: pd.Series, freq="D") -> float:
    """
    Calculate the annualized geometric mean return.
    """
    af = ann_factor(freq)
    log_r = np.log1p(returns)
    return np.expm1(log_r.mean() * af)


def sharpe_ratio(returns: pd.Series, rf=0.0, freq="D") -> float:
    """
    Calculate the Sharpe Ratio.

    Formula: (Mean Return - Risk Free Rate) / Volatility
    """
    af = ann_factor(freq)
    excess = returns - (rf / af)
    vol = excess.std(ddof=1)
    if vol == 0:
        return np.nan
    return (excess.mean() / vol) * np.sqrt(af)


def max_drawdown(returns: pd.Series) -> float:
    """
    Calculate the Maximum Drawdown.

    The maximum observed loss from a peak to a trough of a portfolio, before a new peak is attained.
    Returns a negative number (e.g., -0.20 for a 20% drawdown).
    """
    equity = (1 + returns).cumprod()
    peak = equity.cummax()
    dd = (equity / peak) - 1.0
    return dd.min()


def cvar_historical(returns: pd.Series, alpha=0.05) -> float:
    """
    Calculate the Conditional Value at Risk (CVaR) or Expected Shortfall.

    This is the average loss in the worst alpha% of cases.
    Returns a positive number representing the loss (e.g., 0.05 means 5% average tail loss).
    """
    losses = -returns.values
    var = np.quantile(losses, 1 - (1 - alpha))
    tail_losses = losses[losses >= var]
    if len(tail_losses) == 0:
        return 0.0
    return float(tail_losses.mean())


def risk_contributions(w: np.ndarray, cov: np.ndarray) -> np.ndarray:
    """
    Calculate the risk contributions of each asset.

    Args:
        w (np.ndarray): Portfolio weights.
        cov (np.ndarray): Covariance matrix of returns.

    Returns:
        np.ndarray: Risk contribution in volatility terms.
    """
    port_var = float(w @ cov @ w)
    port_vol = np.sqrt(port_var) if port_var > 0 else 0.0
    mrc = cov @ w
    # contribution to variance: w_i * mrc_i
    rc_var = w * mrc
    # contribution to vol: rc_var / port_vol
    rc_vol = rc_var / (port_vol + 1e-12)
    return rc_vol
