from datetime import datetime, date, timedelta


def calculate_window(purchase_date, policy_days):
    """
    Calculate the return/warranty expiry date and remaining days.

    The window starts from the purchase date and lasts for
    the number of days specified by the store policy.
    """

    if isinstance(purchase_date, str):
        purchase_date = datetime.strptime(
            purchase_date,
            "%Y-%m-%d"
        ).date()

    expiry_date = purchase_date + timedelta(days=policy_days)

    today = date.today()
    days_remaining = (expiry_date - today).days

    return {
        "expiry_date": expiry_date,
        "days_remaining": days_remaining,
        "expiring_soon": 0 <= days_remaining < 7,
        "expired": days_remaining < 0
    }


if __name__ == "__main__":
    # Simple test
    result = calculate_window(
        "2026-09-20",
        30
    )

    print("Expiry date:", result["expiry_date"])
    print("Days remaining:", result["days_remaining"])

    if result["expired"]:
        print("❌ Window has expired.")
    elif result["expiring_soon"]:
        print("⚠️ Window expires in less than 7 days.")
    else:
        print("✅ Window is still active.")