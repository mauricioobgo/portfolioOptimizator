# Project Context & Domain Knowledge

## Overview
This project, **Portfolio Optimizator**, is a quantitative finance application designed to optimize investment portfolios using Modern Portfolio Theory (MPT) and advanced risk metrics. It is built in Python and uses `yfinance` for market data.

## Domain Knowledge

### Risk Metrics
1.  **Annualized Volatility**: The standard deviation of returns * sqrt(252). Measures the dispersion of returns.
2.  **Sharpe Ratio**: (Mean Return - Risk Free Rate) / Volatility. Measures risk-adjusted return.
3.  **Max Drawdown**: The maximum observed loss from a peak to a trough of a portfolio, before a new peak is attained.
4.  **CVaR (Conditional Value at Risk)**: Also known as Expected Shortfall. The average loss in the worst $\alpha\%$ of cases (tail risk).

### Optimization Strategies
1.  **Min Volatility**: Minimize portfolio standard deviation.
2.  **Max Sharpe**: Maximize the Sharpe Ratio.
3.  **Risk Parity (ERC)**: Find weights such that each asset contributes equally to the total portfolio risk.
4.  **Min Max Drawdown**: Minimize the worst historical drawdown.

## Architecture
-   **`assets/`**: Source of truth for investable universe (YAML files).
-   **`risk/`**: Logic for calculating metrics and assessing user risk limits.
-   **`optimizator/`**: Core engine that fetches data and runs `scipy.optimize` routines.
-   **`Notebooks/`**: Interactive playground.

## Agent Guidelines
-   When adding new features, ensure they are modular.
-   Always update `assets/` YAMLs for new tickers; avoid hardcoding.
-   Use `uv` for dependency management.
