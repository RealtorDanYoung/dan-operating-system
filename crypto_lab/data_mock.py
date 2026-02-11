from __future__ import annotations

import random
from datetime import datetime, timedelta
from typing import List, Dict


def generate_mock_price_data(points: int = 30, start_price: float = 50000.0) -> List[Dict[str, float]]:
    """Generate fake crypto price data for local strategy testing."""
    current_time = datetime.utcnow() - timedelta(days=points)
    price = start_price
    rows: List[Dict[str, float]] = []

    for _ in range(points):
        drift = random.uniform(-0.03, 0.03)
        price *= 1 + drift
        current_time += timedelta(days=1)
        rows.append({"timestamp": current_time.isoformat(), "price": round(price, 2)})

    return rows
