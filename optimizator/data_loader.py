import yfinance as yf
import pandas as pd


def download_prices(
    tickers: list, start: str = "2015-01-01", end: str = None
) -> pd.DataFrame:
    """
    Download adjusted close prices for a list of tickers.

    Args:
        tickers (list): List of ticker symbols.
        start (str, optional): Start date YYYY-MM-DD.
        end (str, optional): End date YYYY-MM-DD.

    Returns:
        pd.DataFrame: DataFrame of adjusted close prices, cleaned of NaNs.
    """
    if not tickers:
        return pd.DataFrame()

    # yfinance auto_adjust=True gives us the Adjusted Close in the "Close" column
    df = yf.download(tickers, start=start, end=end, auto_adjust=True, progress=False)[
        "Close"
    ]

    if isinstance(df, pd.Series):
        df = df.to_frame()

    # Drop tickers that failed to download (all NaNs)
    df = df.dropna(axis=1, how="all")
    # Drop rows where all tickers are missing
    df = df.dropna(axis=0, how="all")

    return df


def to_returns(prices: pd.DataFrame, freq: str = "D") -> pd.DataFrame:
    """
    Convert prices to returns.
    """
    rets = prices.pct_change().dropna()
    if freq == "M":
        # Compounding monthly returns
        rets = (1 + rets).resample("M").prod() - 1
    return rets
