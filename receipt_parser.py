import re
from pathlib import Path


def read_receipt(file_path):
    """Read a text receipt from a file."""

    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(
            f"Receipt not found: {file_path}"
        )

    return path.read_text(encoding="utf-8")


def parse_receipt(text):
    """Extract important information from a receipt."""

    order_match = re.search(
        r"Order\s*ID\s*:\s*(.+)",
        text,
        re.IGNORECASE
    )

    date_match = re.search(
        r"Purchase\s*Date\s*:\s*(\d{4}-\d{2}-\d{2})",
        text,
        re.IGNORECASE
    )

    customer_match = re.search(
        r"Customer\s*:\s*(.+)",
        text,
        re.IGNORECASE
    )

    if not date_match:
        raise ValueError("Purchase date was not found.")

    items = []

    item_pattern = re.compile(
        r"^\s*\d+\.\s*"
        r"(.*?)\s*\|\s*"
        r"Category\s*:\s*(.*?)\s*\|\s*"
        r"Quantity\s*:\s*(\d+)\s*\|\s*"
        r"Price\s*:\s*(.+?)\s*$",
        re.IGNORECASE | re.MULTILINE
    )

    for match in item_pattern.finditer(text):

        price_text = match.group(4)

        # Find the numeric price.
        price_match = re.search(
            r"\d+(?:\.\d+)?",
            price_text
        )

        if not price_match:
            raise ValueError(
                f"Invalid price: {price_text}"
            )

        price = float(price_match.group())

        quantity = int(match.group(3))

        items.append({
            "name": match.group(1).strip(),
            "category": match.group(2).strip(),
            "quantity": quantity,
            "unit_price": price,
            "line_total": price * quantity
        })

    total_match = re.search(
        r"Total\s*Paid\s*:\s*(.+)",
        text,
        re.IGNORECASE
    )

    total_paid = None

    if total_match:

        total_match_number = re.search(
            r"\d+(?:\.\d+)?",
            total_match.group(1)
        )

        if total_match_number:
            total_paid = float(
                total_match_number.group()
            )

    return {
        "order_id": (
            order_match.group(1).strip()
            if order_match
            else None
        ),

        "purchase_date": date_match.group(1),

        "customer": (
            customer_match.group(1).strip()
            if customer_match
            else None
        ),

        "items": items,

        "total_paid": total_paid
    }


if __name__ == "__main__":

    # Test receipt
    sample_receipt = """
ORDER CONFIRMATION

Order ID: ORD-1001
Purchase Date: 2026-09-18
Customer: Demo Shopper

ITEMS

1. Cotton Oversized T-Shirt | Category: Clothing | Quantity: 2 | Price: INR 799 each

Subtotal: INR 1598
Tax: INR 288
Total Paid: INR 1886
"""

    result = parse_receipt(sample_receipt)

    print("Receipt parser is working! ✅")
    print()

    print("Order ID:", result["order_id"])
    print("Purchase Date:", result["purchase_date"])
    print("Customer:", result["customer"])
    print("Total Paid:", result["total_paid"])

    print()
    print("Items:")

    for item in result["items"]:
        print(
            "-",
            item["name"],
            "|",
            item["category"],
            "| Quantity:",
            item["quantity"],
            "| Price:",
            item["unit_price"]
        )
