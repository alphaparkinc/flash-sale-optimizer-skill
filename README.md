# flash-sale-optimizer-skill

> **GenPark AI Agent Skill** -- Optimize flash sale timing, discount depth, inventory allocation, and urgency messaging.

## Features

- Margin-aware optimal discount calculation per product
- 70% inventory cap rule to protect base stock
- Day/time timing recommendations with engagement scores
- Conversion rate estimation based on discount depth and urgency
- 7 urgency message templates with dynamic variable injection
- Revenue projection against target

## Quick Start

```python
from client import FlashSaleClient

client = FlashSaleClient()
result = client.optimize(
    products=[{"name": "Serum", "regular_price": 35, "cost": 7, "current_stock": 200}],
    sale_duration_hours=24,
    audience_size=20000,
)
print(result["sale_plan"])
print(result["urgency_messages"])
```

## Installation

```bash
python example_usage.py  # No external dependencies
```

---
Built by [GenPark](https://genpark.ai) | [alphaparkinc](https://github.com/alphaparkinc)
