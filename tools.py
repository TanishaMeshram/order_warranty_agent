import pandas as pd
from langchain_core.tools import tool
from calculator import calculate_window


@tool
def check_order_status(order_id: str):
    """Check the status of an order."""

    orders = pd.read_csv("data/order_status.csv")

    order = orders[
        orders["order_id"].str.upper() == order_id.upper()
    ]

    if order.empty:
        return f"Order {order_id} was not found."

    row = order.iloc[0]

    return (
        f"Order {row['order_id']}: {row['status']}. "
        f"Estimated delivery: {row['estimated_delivery']}. "
        f"Last update: {row['last_update']}."
    )


@tool
def calculate_return_warranty(
    purchase_date: str,
    category: str
):
    """Calculate return and warranty dates."""

    policies = {
        "electronics": (7, 365),
        "clothing": (15, 30),
        "all other products": (7, 30)
    }

    category_key = category.lower()

    if category_key not in policies:
        category_key = "all other products"

    return_days, warranty_days = policies[category_key]

    return_info = calculate_window(
        purchase_date,
        return_days
    )

    warranty_info = calculate_window(
        purchase_date,
        warranty_days
    )

    return (
        f"{category}: "
        f"Return expires on {return_info['expiry_date']} "
        f"with {return_info['days_remaining']} days remaining. "
        f"Warranty expires on {warranty_info['expiry_date']} "
        f"with {warranty_info['days_remaining']} days remaining."
    )


if __name__ == "__main__":

    print("ORDER STATUS")
    print(check_order_status.invoke("ORD-1001"))

    print()
    print("RETURN & WARRANTY")
    print(
        calculate_return_warranty.invoke({
            "purchase_date": "2026-09-18",
            "category": "Clothing"
        })
    )