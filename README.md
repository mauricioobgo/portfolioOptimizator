# Portfolio Optimizator

A quantitative finance application for portfolio optimization, enabling users to analyze risk and construct optimal portfolios using Python.

## Architecture

-   **`assets/`**: Manage investment universe (Stocks, ETFs, Bonds) via YAML files.
-   **`risk/`**: Logic for Risk Calculations (Vol, Sharpe, MaxDD, CVaR).
-   **`optimizator/`**: Optimization Engine (Min Vol, Max Sharpe, Risk Parity).
-   **`Notebooks/`**: Jupyter notebooks for analysis.

## Getting Started

1.  **Install Dependencies**
    ```bash
    uv sync
    # or
    uv add yfinance numpy pandas scipy matplotlib seaborn pyyaml
    ```

2.  **Run Notebooks**
    Open `Notebooks/02_Portfolio_Optimization.ipynb` to try the optimizer.

## Key Features

### Asset Discovery
Modify files in `assets/Stocks`, `assets/ETFs`, etc., to expand the universe. The `AssetManager` will automatically pick them up.

### Risk Metrics
-   **Sharpe Ratio**: ROI relative to risk.
-   **CVaR**: Tail risk assessment.
-   **Max Drawdown**: Worst historical loss.

### Optimization Strategies
-   **Max Sharpe**: The "Tangent Portfolio".
-   **Min Volatility**: The safest portfolio on the efficient frontier.
-   **Risk Parity**: Equal contribution to risk from all assets.
