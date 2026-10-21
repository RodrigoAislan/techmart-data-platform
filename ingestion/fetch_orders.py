import json
from pathlib import Path

import requests


API_URL = "https://dummyjson.com/carts"
MAX_RECORDS = 1000


def fetch_orders():
    response = requests.get(
        API_URL,
        params={"limit": MAX_RECORDS, "skip": 0},
        timeout=30,
    )
    response.raise_for_status()

    data = response.json()

    if "carts" not in data or not isinstance(data["carts"], list):
        raise ValueError(
            "The API response does not contain a valid carts list."
        )

    data["carts"] = data["carts"][:MAX_RECORDS]

    print(f"Orders extracted: {len(data['carts'])}")

    return data


def save_orders_locally(data):
    output_dir = Path("data/raw")
    output_dir.mkdir(parents=True, exist_ok=True)

    output_file = output_dir / "orders.json"

    with output_file.open("w", encoding="utf-8") as file:
        json.dump(data, file, indent=2, ensure_ascii=False)

    print(f"Orders saved: {len(data['carts'])}")
    print(f"File: {output_file.resolve()}")


if __name__ == "__main__":
    orders_data = fetch_orders()
    save_orders_locally(orders_data)
