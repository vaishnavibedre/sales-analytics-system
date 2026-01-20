# Update: report formatting improvements
import os
from datetime import datetime

from utils.data_processor import (
    calculate_total_revenue,
    region_wise_sales,
    top_selling_products,
    customer_analysis,
    daily_sales_trend,
    find_peak_sales_day,
    low_performing_products
)


def generate_sales_report(transactions, enriched_transactions, output_file="output/sales_report.txt"):
    """
    Generates a comprehensive formatted text report with 8 required sections.
    """

    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    # ---------------------------------------------------------
    # 1. HEADER
    # ---------------------------------------------------------
    report = []
    report.append("=" * 60)
    report.append("                 SALES ANALYTICS REPORT")
    report.append(f"           Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report.append(f"           Records Processed: {len(transactions)}")
    report.append("=" * 60)
    report.append("")

    # ---------------------------------------------------------
    # 2. OVERALL SUMMARY
    # ---------------------------------------------------------
    total_revenue = calculate_total_revenue(transactions)
    avg_order_value = total_revenue / len(transactions) if transactions else 0

    dates = sorted(t["Date"] for t in transactions)
    date_range = f"{dates[0]} to {dates[-1]}" if dates else "N/A"

    report.append("OVERALL SUMMARY")
    report.append("-" * 60)
    report.append(f"Total Revenue:        ₹{total_revenue:,.2f}")
    report.append(f"Total Transactions:   {len(transactions)}")
    report.append(f"Average Order Value:  ₹{avg_order_value:,.2f}")
    report.append(f"Date Range:           {date_range}")
    report.append("")

    # ---------------------------------------------------------
    # 3. REGION-WISE PERFORMANCE
    # ---------------------------------------------------------
    region_stats = region_wise_sales(transactions)

    report.append("REGION-WISE PERFORMANCE")
    report.append("-" * 60)
    report.append(f"{'Region':<10}{'Sales':<15}{'% of Total':<15}{'Transactions'}")

    for region, stats in region_stats.items():
        report.append(
            f"{region:<10}₹{stats['total_sales']:,.2f}   "
            f"{stats['percentage']:<15}%{stats['transaction_count']}"
        )
    report.append("")

    # ---------------------------------------------------------
    # 4. TOP 5 PRODUCTS
    # ---------------------------------------------------------
    top_products = top_selling_products(transactions, n=5)

    report.append("TOP 5 PRODUCTS")
    report.append("-" * 60)
    report.append(f"{'Rank':<6}{'Product Name':<20}{'Qty Sold':<12}{'Revenue'}")

    for i, (name, qty, rev) in enumerate(top_products, start=1):
        report.append(f"{i:<6}{name:<20}{qty:<12}₹{rev:,.2f}")
    report.append("")

    # ---------------------------------------------------------
    # 5. TOP 5 CUSTOMERS
    # ---------------------------------------------------------
    customers = customer_analysis(transactions)
    top_customers = list(customers.items())[:5]

    report.append("TOP 5 CUSTOMERS")
    report.append("-" * 60)
    report.append(f"{'Rank':<6}{'Customer ID':<15}{'Total Spent':<18}{'Orders'}")

    for i, (cid, stats) in enumerate(top_customers, start=1):
        report.append(
            f"{i:<6}{cid:<15}₹{stats['total_spent']:,.2f}      {stats['purchase_count']}"
        )
    report.append("")

    # ---------------------------------------------------------
    # 6. DAILY SALES TREND
    # ---------------------------------------------------------
    trend = daily_sales_trend(transactions)

    report.append("DAILY SALES TREND")
    report.append("-" * 60)
    report.append(f"{'Date':<15}{'Revenue':<15}{'Transactions':<15}{'Unique Cust.'}")

    for date, stats in trend.items():
        report.append(
            f"{date:<15}₹{stats['revenue']:,.2f}   "
            f"{stats['transaction_count']:<15}{stats['unique_customers']}"
        )
    report.append("")

    # ---------------------------------------------------------
    # 7. PRODUCT PERFORMANCE ANALYSIS
    # ---------------------------------------------------------
    peak_day, peak_rev, peak_count = find_peak_sales_day(transactions)
    low_products = low_performing_products(transactions)

    # Average transaction value per region
    region_avg = {
        r: stats["total_sales"] / stats["transaction_count"]
        for r, stats in region_stats.items()
    }

    report.append("PRODUCT PERFORMANCE ANALYSIS")
    report.append("-" * 60)
    report.append(f"Best Selling Day: {peak_day} (₹{peak_rev:,.2f}, {peak_count} transactions)")
    report.append("")

    report.append("Low Performing Products (Qty < 10):")
    if low_products:
        for name, qty, rev in low_products:
            report.append(f" - {name}: Qty={qty}, Revenue=₹{rev:,.2f}")
    else:
        report.append(" - None")
    report.append("")

    report.append("Average Transaction Value per Region:")
    for region, avg in region_avg.items():
        report.append(f" - {region}: ₹{avg:,.2f}")
    report.append("")

    # ---------------------------------------------------------
    # 8. API ENRICHMENT SUMMARY
    # ---------------------------------------------------------
    total = len(enriched_transactions)
    enriched = sum(1 for t in enriched_transactions if t["API_Match"])
    failed = total - enriched
    success_rate = (enriched / total * 100) if total else 0

    failed_products = [
        t["ProductID"] for t in enriched_transactions if not t["API_Match"]
    ]

    report.append("API ENRICHMENT SUMMARY")
    report.append("-" * 60)
    report.append(f"Total Products Enriched: {enriched}/{total}")
    report.append(f"Success Rate: {success_rate:.2f}%")
    report.append("Products Not Enriched:")
    if failed_products:
        for pid in failed_products:
            report.append(f" - {pid}")
    else:
        report.append(" - None")
    report.append("")

    # ---------------------------------------------------------
    # WRITE REPORT TO FILE
    # ---------------------------------------------------------
    with open(output_file, "w", encoding="utf-8") as f:
        f.write("\n".join(report))

    print(f"✅ Sales report generated successfully → {output_file}")