"""
flash-sale-optimizer-skill: Client SDK
Optimize flash sale timing, discount depth, inventory, and urgency messaging.
"""
from __future__ import annotations
from typing import Optional

BEST_TIMES = {
    "monday":    {"hour": 12, "score": 0.72, "note": "Start-of-week deal seekers"},
    "tuesday":   {"hour": 14, "score": 0.68, "note": "Mid-week engagement peak"},
    "wednesday": {"hour": 12, "score": 0.75, "note": "Hump day deal motivation"},
    "thursday":  {"hour": 19, "score": 0.80, "note": "Pre-weekend shopping spike"},
    "friday":    {"hour": 10, "score": 0.88, "note": "TGIF buying mood -- highest intent"},
    "saturday":  {"hour": 11, "score": 0.82, "note": "Weekend browsing peak"},
    "sunday":    {"hour": 20, "score": 0.78, "note": "Sunday prep shopping"},
}

URGENCY_TEMPLATES = [
    "Only {stock} left -- sale ends in {hours}h {mins}m!",
    "Flash Sale: {discount}% OFF -- Hurry, {stock} units remaining!",
    "Last chance! {hours} hours left to save {discount}%",
    "{pct_sold}% of stock already claimed -- grab yours now",
    "Today only: Save {discount}% -- offer ends at midnight",
    "You are saving ${savings} right now -- do not wait!",
    "{stock} units left at this price. Restock at full price tomorrow.",
]

SCARCITY_THRESHOLDS = [
    (0.90, "CRITICAL: Only {n} left!"),
    (0.75, "Almost gone: {n} remaining"),
    (0.50, "Selling fast: {n} in stock"),
    (0.25, "Limited stock: {n} available"),
    (0.0,  "In stock: {n} units"),
]


class FlashSaleClient:
    """
    SDK for optimizing e-commerce flash sales.
    Calculates optimal discount depths, inventory caps, timing, and urgency copy.
    """

    def optimize(
        self,
        products: list[dict],
        sale_duration_hours: int = 24,
        target_revenue_usd: Optional[float] = None,
        audience_size: int = 10000,
        preferred_day: str = "friday",
    ) -> dict:
        """
        Generate a complete flash sale optimization plan.

        Args:
            products:            List of {name, regular_price, cost, current_stock}.
            sale_duration_hours: Sale window in hours.
            target_revenue_usd:  Revenue target (optional).
            audience_size:       Reachable audience for conversion estimation.
            preferred_day:       Preferred day of week for the sale.

        Returns:
            dict with sale_plan, timing_recommendation, urgency_messages, revenue_projection
        """
        sale_plan = []
        total_projected_revenue = 0.0
        total_projected_units = 0

        for product in products:
            name = product.get("name", "Product")
            regular_price = float(product.get("regular_price", 0))
            cost = float(product.get("cost", regular_price * 0.4))
            stock = int(product.get("current_stock", 100))

            if regular_price <= 0:
                continue

            # Calculate optimal discount
            discount_pct = self._optimal_discount(regular_price, cost)
            sale_price = round(regular_price * (1 - discount_pct / 100), 2)

            # Inventory cap (sell at most 70% of stock in a flash sale)
            inventory_cap = max(1, int(stock * 0.70))

            # Conversion estimate
            base_cvr = 0.03  # 3% base
            discount_boost = discount_pct / 100 * 0.5
            urgency_boost = min(sale_duration_hours / 48, 1) * 0.02
            est_cvr = min(base_cvr + discount_boost + urgency_boost, 0.25)
            est_units = min(int(audience_size * est_cvr * 0.1), inventory_cap)
            est_revenue = round(est_units * sale_price, 2)
            est_margin = round((sale_price - cost) * est_units, 2)

            total_projected_revenue += est_revenue
            total_projected_units += est_units

            pct_stock_sold = round(est_units / max(stock, 1) * 100, 1)

            sale_plan.append({
                "product": name,
                "regular_price": regular_price,
                "discount_pct": discount_pct,
                "sale_price": sale_price,
                "savings_usd": round(regular_price - sale_price, 2),
                "inventory_cap": inventory_cap,
                "estimated_units_sold": est_units,
                "estimated_revenue": est_revenue,
                "estimated_margin": est_margin,
                "pct_stock_allocated": pct_stock_sold,
            })

        timing = self._timing_recommendation(preferred_day, sale_duration_hours)
        urgency_msgs = self._generate_urgency(sale_plan, sale_duration_hours)
        revenue_proj = {
            "total_projected_revenue": round(total_projected_revenue, 2),
            "total_projected_units": total_projected_units,
            "avg_discount_pct": round(sum(p["discount_pct"] for p in sale_plan) / max(len(sale_plan), 1), 1),
            "target_achieved": total_projected_revenue >= (target_revenue_usd or 0),
            "target_revenue_usd": target_revenue_usd,
        }

        return {
            "sale_plan": sale_plan,
            "timing_recommendation": timing,
            "urgency_messages": urgency_msgs,
            "revenue_projection": revenue_proj,
            "sale_duration_hours": sale_duration_hours,
        }

    @staticmethod
    def _optimal_discount(price: float, cost: float) -> float:
        margin = (price - cost) / price if price > 0 else 0.5
        if margin >= 0.7: return 40.0
        if margin >= 0.5: return 30.0
        if margin >= 0.3: return 20.0
        if margin >= 0.2: return 15.0
        return 10.0

    @staticmethod
    def _timing_recommendation(day: str, hours: int) -> dict:
        day = day.lower()
        best = BEST_TIMES.get(day, BEST_TIMES["friday"])
        end_hour = (best["hour"] + hours) % 24
        return {
            "recommended_day": day.title(),
            "start_time": f"{best['hour']:02d}:00",
            "end_time": f"{end_hour:02d}:00",
            "engagement_score": best["score"],
            "rationale": best["note"],
        }

    @staticmethod
    def _generate_urgency(sale_plan: list[dict], hours: int) -> list[str]:
        msgs = []
        for tmpl in URGENCY_TEMPLATES[:5]:
            if sale_plan:
                p = sale_plan[0]
                msg = tmpl.format(
                    stock=p.get("inventory_cap", 50),
                    hours=hours,
                    mins=0,
                    discount=int(p.get("discount_pct", 20)),
                    pct_sold=int(p.get("pct_stock_allocated", 30)),
                    savings=p.get("savings_usd", 10),
                    n=p.get("inventory_cap", 50),
                )
                msgs.append(msg)
        return msgs
