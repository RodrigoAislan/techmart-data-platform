import json
from pathlib import Path

import requests


API_URL = "https://dummyjson.com/carts"
MAX_RECORDS = 1000


def fetch_order_items():
    response = requests.get(
        API_URL,
        params={"limit": MAX_RECORDS, "skip": 0},
        timeout=30,
    )
    response.raise_for_status()

    data = response.json()

    if "carts" not in data or not isinstance(data["carts"], list):
        raise ValueError("The API response does not contain a valid carts list.")

    carts = data["carts"][:MAX_RECORDS]
    order_items = []

    for cart in carts:
        order_id = cart.get("id")
        customer_id = cart.get("userId")
        products = cart.get("products", [])

        if not isinstance(products, list):
            raise ValueError(f"Products for order {order_id} must be a list.")

        for product in products:
            quantity = product.get("quantity")
            price = product.get("price")

            if quantity is None or price is None:
                raise ValueError(
                    f"Missing quantity or price in order {order_id}."
                )

            order_item = {
                "order_id": order_id,
                "customer_id": customer_id,
                "product_id": product.get("id"),
                "product_title": product.get("title"),
                "quantity": quantity,
                "price": price,
                "line_total": round(quantity * price, 2),
                "discount_percentage": product.get("discountPercentage"),
                "discounted_total": product.get("discountedTotal"),
            }

            order_items.append(order_item)

    result = {
        "source": API_URL,
        "order_count": len(carts),
        "order_item_count": len(order_items),
        "order_items": order_items,
    }

    print(f"Orders processed: {result['order_count']}")
    print(f"Order items extracted: {result['order_item_count']}")

    return result


def save_order_items_locally(data):
    output_dir = Path("data/raw")
    output_dir.mkdir(parents=True, exist_ok=True)

    output_file = output_dir / "order_items.json"

    with output_file.open("w", encoding="utf-8") as file:
        json.dump(data, file, indent=2, ensure_ascii=False)

    print(f"Order items saved: {data['order_item_count']}")
    print(f"File: {output_file.resolve()}")


if __name__ == "__main__":
    order_items_data = fetch_order_items()
    save_order_items_locally(order_items_data)