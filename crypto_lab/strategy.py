from __future__ import annotations

import logging
from typing import Dict, List

from config import DEFAULT_LOOKBACK, LOG_LEVEL, RISK_LIMIT_PER_TRADE
from data_mock import generate_mock_price_data

logging.basicConfig(level=LOG_LEVEL, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)


def risk_management_stub(position_size: float, account_size: float) -> Dict[str, float | bool]:
    """Basic risk guardrail placeholder for future portfolio logic."""
    max_allowed = account_size * RISK_LIMIT_PER_TRADE
    allowed = position_size <= max_allowed
    return {"position_size": position_size, "max_allowed": max_allowed, "allowed": allowed}


def placeholder_strategy(price_rows: List[Dict[str, float]], lookback: int = DEFAULT_LOOKBACK) -> Dict[str, str | float]:
    """Minimal strategy placeholder using moving-average style direction signal."""
    if len(price_rows) < lookback:
        return {"signal": "HOLD", "reason": "Not enough data", "last_price": price_rows[-1]["price"]}

    recent = [row["price"] for row in price_rows[-lookback:]]
    avg_price = sum(recent) / len(recent)
    last_price = price_rows[-1]["price"]
    signal = "BUY" if last_price > avg_price else "SELL"

    return {"signal": signal, "last_price": last_price, "lookback_avg": round(avg_price, 2)}


def run_demo() -> None:
    rows = generate_mock_price_data(points=45)
    strategy_output = placeholder_strategy(rows)
    risk_output = risk_management_stub(position_size=50.0, account_size=10000.0)

    logger.info("Strategy output: %s", strategy_output)
    logger.info("Risk check: %s", risk_output)


if __name__ == "__main__":
    run_demo()
