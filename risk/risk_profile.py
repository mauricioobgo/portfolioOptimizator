from dataclasses import dataclass
from typing import Tuple, Dict


@dataclass
class RiskProfile:
    label: str
    suggested_ann_vol_range: Tuple[float, float]
    suggested_maxdd_range: Tuple[float, float]
    min_bond_allocation: float = 0.0
    max_equity_allocation: float = 1.0


def estimate_risk_profile(answers: Dict) -> RiskProfile:
    """
    Estimate risk profile based on questionnaire answers.

    Args:
        answers (dict): keys [horizon_years, drawdown_comfort_pct, sell_in_crash, income_stability, experience]

    Returns:
        RiskProfile: The estimated risk profile with investment constraints.
    """
    score = 0

    # horizon
    h = answers.get("horizon_years", 3)
    score += 0 if h <= 2 else 1 if h <= 5 else 2

    # drawdown comfort
    dd = answers.get("drawdown_comfort_pct", 20)
    score += 0 if dd <= 15 else 1 if dd <= 30 else 2

    # crash behavior
    crash = answers.get("sell_in_crash", "hold")
    score += {"sell_all": 0, "sell_some": 0, "hold": 1, "buy_more": 2}.get(crash, 1)

    # income stability
    inc = answers.get("income_stability", "stable")
    score += {"unstable": 0, "somewhat": 1, "stable": 2}.get(inc, 1)

    # experience
    exp = answers.get("experience", "some")
    score += {"new": 0, "some": 1, "experienced": 2}.get(exp, 1)

    # Map score to profile
    if score <= 3:
        return RiskProfile(
            label="Conservative",
            suggested_ann_vol_range=(0.04, 0.09),
            suggested_maxdd_range=(-0.10, -0.20),
            min_bond_allocation=0.40,  # Force at least 40% bonds
            max_equity_allocation=0.60,
        )
    elif score <= 6:
        return RiskProfile(
            label="Moderate",
            suggested_ann_vol_range=(0.10, 0.15),
            suggested_maxdd_range=(-0.20, -0.35),
            min_bond_allocation=0.20,
            max_equity_allocation=0.80,
        )
    else:
        return RiskProfile(
            label="Aggressive",
            suggested_ann_vol_range=(0.15, 0.25),
            suggested_maxdd_range=(-0.30, -0.50),
            min_bond_allocation=0.0,
            max_equity_allocation=1.0,
        )
