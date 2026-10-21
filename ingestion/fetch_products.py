import json
from pathlib import Path

import requests

API_URL = "https://dummyjson.com/products"
MAX_RECORDS = 1000


def fetch_products():
    """Fetch up to 1,000 products from DummyJSON."""

    response = requests.get(
        API_URL,
        params={"limit": MAX_RECORDS, "skip": 0},
        timeout=30,
    )

    response.raise_for_status()

    data = response.json()

    if "products" not in data or not isinstance(data["products"], list):
        raise ValueError(
            "The API response does not contain a valid products list."
        )

    data["products"] = data["products"][:MAX_RECORDS]

    print(f"Products extracted: {len(data['products'])}")

    return data


def save_products_locally(data):
    """Save the extracted response as a local JSON file."""

    output_dir = Path("data/raw")
    output_dir.mkdir(parents=True, exist_ok=True)

    output_file = output_dir / "products.json"

    with output_file.open("w", encoding="utf-8") as file:
        json.dump(data, file, indent=2, ensure_ascii=False)

    print(f"Products saved: {len(data['products'])}")
    print(f"File: {output_file.resolve()}")


if __name__ == "__main__":
    products_data = fetch_products()
    save_products_locally(products_data)