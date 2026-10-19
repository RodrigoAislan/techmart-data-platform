import json
from pathlib import Path
import requests

API_URL = "https://dummyjson.com/users"
MAX_RECORDS = 1000


def fetch_customers():
    """Fetch up to 1,000 customers from DummyJSON."""

    response = requests.get(
        API_URL,
        params={"limit": MAX_RECORDS, "skip": 0},
        timeout=30,
    )

    response.raise_for_status()

    data = response.json()

    if "users" not in data or not isinstance(data["users"], list):
        raise ValueError(
            "The API response does not contain a valid users list."
        )

    data["users"] = data["users"][:MAX_RECORDS]

    print(f"Customers extracted: {len(data['users'])}")

    return data


def save_customers_locally(data):
    """Save the extracted response as a local JSON file."""

    output_dir = Path("data/raw")
    output_dir.mkdir(parents=True, exist_ok=True)

    output_file = output_dir / "customers.json"

    with output_file.open("w", encoding="utf-8") as file:
        json.dump(data, file, indent=2, ensure_ascii=False)

    print(f"Customers saved: {len(data['users'])}")
    print(f"File: {output_file.resolve()}")


if __name__ == "__main__":
    customers_data = fetch_customers()
    save_customers_locally(customers_data)