"""
Data Processor Module
Handles data cleaning and validation for sales records
"""
def calculate_total_revenue(transactions):
    """
    Calculates total revenue from all transactions
    Returns: float
    """
    total_revenue = 0.0
    for tx in transactions:
        try:
            quantity = int(tx.get("Quantity", 0))
            unit_price = float(tx.get("UnitPrice", 0))
            total_revenue += quantity * unit_price
        except (ValueError, TypeError):
            continue
    return round(total_revenue, 2)


def region_wise_sales(transactions):
    """
    Analyzes sales by region
    Returns: dictionary sorted by total_sales descending
    """
    region_data = {}
    total_sales_all = 0.0

    for tx in transactions:
        region = tx.get("Region")
        if not region:
            continue

        try:
            quantity = int(tx.get("Quantity", 0))
            unit_price = float(tx.get("UnitPrice", 0))
            sale_value = quantity * unit_price
        except (ValueError, TypeError):
            continue

        if region not in region_data:
            region_data[region] = {
                "total_sales": 0.0,
                "transaction_count": 0
            }

        region_data[region]["total_sales"] += sale_value
        region_data[region]["transaction_count"] += 1
        total_sales_all += sale_value

    for region in region_data:
        total = region_data[region]["total_sales"]
        region_data[region]["total_sales"] = round(total, 2)
        region_data[region]["percentage"] = round(
            (total / total_sales_all) * 100, 2
        ) if total_sales_all else 0

    return dict(
        sorted(
            region_data.items(),
            key=lambda x: x[1]["total_sales"],
            reverse=True
        )
    )


def top_selling_products(transactions, n=5):
    """
    Finds top n products by total quantity sold
    Returns: list of tuples
    (ProductName, TotalQuantity, TotalRevenue)
    """
    product_data = {}

    for tx in transactions:
        product = tx.get("ProductName")
        try:
            quantity = int(tx.get("Quantity", 0))
            unit_price = float(tx.get("UnitPrice", 0))
            revenue = quantity * unit_price
        except (ValueError, TypeError):
            continue

        if product not in product_data:
            product_data[product] = {"quantity": 0, "revenue": 0.0}

        product_data[product]["quantity"] += quantity
        product_data[product]["revenue"] += revenue

    product_list = [
        (product, data["quantity"], round(data["revenue"], 2))
        for product, data in product_data.items()
    ]

    product_list.sort(key=lambda x: x[1], reverse=True)
    return product_list[:n]


def customer_analysis(transactions):
    """
    Analyzes customer purchase patterns
    Returns: dictionary sorted by total_spent descending
    """
    customer_data = {}

    for tx in transactions:
        customer = tx.get("CustomerID")
        if not customer:
            continue

        product = tx.get("ProductName")
        try:
            quantity = int(tx.get("Quantity", 0))
            unit_price = float(tx.get("UnitPrice", 0))
            amount = quantity * unit_price
        except (ValueError, TypeError):
            continue

        if customer not in customer_data:
            customer_data[customer] = {
                "total_spent": 0.0,
                "purchase_count": 0,
                "products_bought": set()
            }

        customer_data[customer]["total_spent"] += amount
        customer_data[customer]["purchase_count"] += 1
        customer_data[customer]["products_bought"].add(product)

    for customer in customer_data:
        total = customer_data[customer]["total_spent"]
        count = customer_data[customer]["purchase_count"]

        customer_data[customer]["total_spent"] = round(total, 2)
        customer_data[customer]["avg_order_value"] = round(
            total / count, 2
        ) if count else 0
        customer_data[customer]["products_bought"] = sorted(
            customer_data[customer]["products_bought"]
        )

    return dict(
        sorted(
            customer_data.items(),
            key=lambda x: x[1]["total_spent"],
            reverse=True
        )
    )


# ------------------- PRINTING OUTPUTS -------------------

if __name__ == "__main__":

    # Assume `transactions` is already loaded as a list of dictionaries

    print("\n===== TOTAL REVENUE =====")
    total_revenue = calculate_total_revenue(transactions)
    print(total_revenue)

    print("\n===== REGION-WISE SALES =====")
    region_sales = region_wise_sales(transactions)
    for region, data in region_sales.items():
        print(f"{region}: {data}")

    print("\n===== TOP SELLING PRODUCTS =====")
    top_products = top_selling_products(transactions, n=5)
    for product in top_products:
        print(product)

    print("\n===== CUSTOMER PURCHASE ANALYSIS =====")
    customers = customer_analysis(transactions)
    for customer_id, data in customers.items():
        print(f"{customer_id}: {data}")

from collections import defaultdict


# ================= TASK 2.2 : DATE-BASED ANALYSIS =================

def daily_sales_trend(transactions):
    """
    Analyzes sales trends by date
    Returns: dictionary sorted by date
    """
    daily_data = {}

    for tx in transactions:
        date = tx.get("Date")
        if not date:
            continue

        try:
            quantity = int(tx.get("Quantity", 0))
            unit_price = float(tx.get("UnitPrice", 0))
            revenue = quantity * unit_price
        except (ValueError, TypeError):
            continue

        customer = tx.get("CustomerID")

        if date not in daily_data:
            daily_data[date] = {
                "revenue": 0.0,
                "transaction_count": 0,
                "unique_customers": set()
            }

        daily_data[date]["revenue"] += revenue
        daily_data[date]["transaction_count"] += 1

        if customer:
            daily_data[date]["unique_customers"].add(customer)

    # Final formatting
    for date in daily_data:
        daily_data[date]["revenue"] = round(daily_data[date]["revenue"], 2)
        daily_data[date]["unique_customers"] = len(
            daily_data[date]["unique_customers"]
        )

    # Sort chronologically
    return dict(sorted(daily_data.items()))


def find_peak_sales_day(transactions):
    """
    Identifies the date with highest revenue
    Returns: tuple (date, revenue, transaction_count)
    """
    daily_sales = daily_sales_trend(transactions)

    peak_date = None
    max_revenue = -float("inf")
    transaction_count = 0

    for date, data in daily_sales.items():
        if data["revenue"] > max_revenue:
            max_revenue = data["revenue"]
            peak_date = date
            transaction_count = data["transaction_count"]

    return (peak_date, round(max_revenue, 2), transaction_count)


# ================= TASK 2.3 : PRODUCT PERFORMANCE =================

def low_performing_products(transactions, threshold=10):
    """
    Identifies products with low sales
    Returns: list of tuples
    (ProductName, TotalQuantity, TotalRevenue)
    """
    product_data = defaultdict(lambda: {"quantity": 0, "revenue": 0.0})

    for tx in transactions:
        product = tx.get("ProductName")

        try:
            quantity = int(tx.get("Quantity", 0))
            unit_price = float(tx.get("UnitPrice", 0))
            revenue = quantity * unit_price
        except (ValueError, TypeError):
            continue

        product_data[product]["quantity"] += quantity
        product_data[product]["revenue"] += revenue

    low_products = []

    for product, data in product_data.items():
        if data["quantity"] < threshold:
            low_products.append(
                (product, data["quantity"], round(data["revenue"], 2))
            )

    # Sort by TotalQuantity ascending
    low_products.sort(key=lambda x: x[1])

    return low_products


# ================= PRINTING OUTPUTS =================

if __name__ == "__main__":

    # Assume `transactions` is already loaded as a list of dictionaries

    print("\n===== DAILY SALES TREND =====")
    daily_trend = daily_sales_trend(transactions)
    for date, data in daily_trend.items():
        print(f"{date}: {data}")

    print("\n===== PEAK SALES DAY =====")
    peak_day = find_peak_sales_day(transactions)
    print(peak_day)

    print("\n===== LOW PERFORMING PRODUCTS =====")
    low_products = low_performing_products(transactions, threshold=10)
    for product in low_products:
        print(product)
