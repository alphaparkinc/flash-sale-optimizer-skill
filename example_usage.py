"""
example_usage.py -- Demonstrates the FlashSaleClient SDK.
"""
from client import FlashSaleClient

def main():
    client = FlashSaleClient()

    products = [
        {"name": "Vitamin C Serum 30ml", "regular_price": 34.99, "cost": 7.00, "current_stock": 200},
        {"name": "Hyaluronic Moisturizer", "regular_price": 28.99, "cost": 6.50, "current_stock": 150},
        {"name": "SPF 50 Sunscreen", "regular_price": 19.99, "cost": 5.00, "current_stock": 300},
        {"name": "Retinol Night Cream", "regular_price": 44.99, "cost": 12.00, "current_stock": 80},
    ]

    print("[Flash Sale Optimizer]")
    result = client.optimize(
        products=products,
        sale_duration_hours=24,
        target_revenue_usd=5000,
        audience_size=25000,
        preferred_day="friday",
    )

    timing = result["timing_recommendation"]
    print(f"\nTiming: {timing['recommended_day']} at {timing['start_time']} (Score: {timing['engagement_score']})")
    print(f"Rationale: {timing['rationale']}")

    print(f"\nSale Plan:")
    for p in result["sale_plan"]:
        print(f"  {p['product']}")
        print(f"    ${p['regular_price']} -> ${p['sale_price']} (-{p['discount_pct']}%) | Cap: {p['inventory_cap']} units | Est: {p['estimated_units_sold']} sold = ${p['estimated_revenue']:.2f}")

    proj = result["revenue_projection"]
    print(f"\nRevenue Projection:")
    print(f"  Total: ${proj['total_projected_revenue']:,.2f}")
    print(f"  Units: {proj['total_projected_units']}")
    print(f"  Avg Discount: {proj['avg_discount_pct']}%")
    print(f"  Target ${proj['target_revenue_usd']:,.0f} achieved: {proj['target_achieved']}")

    print(f"\nUrgency Messages:")
    for msg in result["urgency_messages"][:3]:
        print(f"  - {msg}")

if __name__ == "__main__":
    main()
