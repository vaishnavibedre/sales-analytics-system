"""
API Handler Module
Handles API requests for product information
"""
import requests


# ================= TASK 3.1(a): FETCH ALL PRODUCTS =================

def fetch_all_products():
    """
    Fetches all products from DummyJSON API
    Returns: list of product dictionaries
    """
    url = "https://dummyjson.com/products?limit=100"

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        data = response.json()
        products = data.get("products", [])

        formatted_products = []

        for product in products:
            formatted_products.append({
                "id": product.get("id"),
                "title": product.get("title"),
                "category": product.get("category"),
                "brand": product.get("brand"),
                "price": product.get("price"),
                "rating": product.get("rating")
            })

        print("✅ Successfully fetched products from DummyJSON API")
        return formatted_products

    except requests.exceptions.RequestException as e:
        print(f"❌ Failed to fetch products: {e}")
        return []


# ================= TASK 3.1(b): CREATE PRODUCT MAPPING =================

def create_product_mapping(api_products):
    """
    Creates a mapping of product IDs to product info
    Returns: dictionary mapping product IDs to info
    """
    product_mapping = {}

    for product in api_products:
        product_id = product.get("id")

        product_mapping[product_id] = {
            "title": product.get("title"),
            "category": product.get("category"),
            "brand": product.get("brand"),
            "rating": product.get("rating")
        }

    return product_mapping


# ================= PRINTING OUTPUTS =================

if __name__ == "__main__":

    print("\n===== FETCHING ALL PRODUCTS =====")
    api_products = fetch_all_products()

    print("\nSample Product Output:")
    if api_products:
        print(api_products[0])

    print("\n===== CREATING PRODUCT MAPPING =====")
    product_mapping = create_product_mapping(api_products)

    print("\nSample Product Mapping Entry:")
    if product_mapping:
        first_key = list(product_mapping.keys())[0]
        print(f"{first_key}: {product_mapping[first_key]}")

import os


# ================= TASK 3.2 : ENRICH SALES DATA =================

def enrich_sales_data(transactions, product_mapping):
    """
    Enriches transaction data with API product information
    Returns: list of enriched transaction dictionaries
    """
    enriched_transactions = []

    for tx in transactions:
        enriched_tx = tx.copy()

        product_id = tx.get("ProductID", "")
        numeric_id = None

        # Extract numeric ID (P101 -> 101, P5 -> 5)
        try:
            numeric_id = int("".join(filter(str.isdigit, product_id)))
        except (ValueError, TypeError):
            numeric_id = None

        api_data = product_mapping.get(numeric_id)

        if api_data:
            enriched_tx["API_Category"] = api_data.get("category")
            enriched_tx["API_Brand"] = api_data.get("brand")
            enriched_tx["API_Rating"] = api_data.get("rating")
            enriched_tx["API_Match"] = True
        else:
            enriched_tx["API_Category"] = None
            enriched_tx["API_Brand"] = None
            enriched_tx["API_Rating"] = None
            enriched_tx["API_Match"] = False

        enriched_transactions.append(enriched_tx)

    print("✅ Sales data enriched successfully")
    return enriched_transactions


# ================= SAVE ENRICHED DATA =================

def save_enriched_data(enriched_transactions, filename="data/enriched_sales_data.txt"):
    """
    Saves enriched transactions back to file in pipe-delimited format
    """
    if not enriched_transactions:
        print("⚠ No enriched data to save")
        return

    os.makedirs(os.path.dirname(filename), exist_ok=True)

    headers = list(enriched_transactions[0].keys())

    try:
        with open(filename, "w", encoding="utf-8") as file:
            # Write header
            file.write("|".join(headers) + "\n")

            # Write rows
            for tx in enriched_transactions:
                row = [
                    str(tx.get(header)) if tx.get(header) is not None else ""
                    for header in headers
                ]
                file.write("|".join(row) + "\n")

        print(f"✅ Enriched data saved to {filename}")

    except IOError as e:
        print(f"❌ Failed to save enriched data: {e}")


# ================= PRINTING OUTPUTS =================

if __name__ == "__main__":

    # Assumes:
    # - `transactions` is already loaded as a list of dictionaries
    # - `product_mapping` is created using create_product_mapping()

    print("\n===== ENRICHING SALES DATA =====")
    enriched_transactions = enrich_sales_data(transactions, product_mapping)

    print("\nSample Enriched Transaction:")
    if enriched_transactions:
        print(enriched_transactions[0])

    print("\n===== SAVING ENRICHED SALES DATA =====")
    save_enriched_data(enriched_transactions)
