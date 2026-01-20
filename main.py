"""
Main Module
Entry point for the Sales Data Analytics System
"""

import os
from utils.file_handler import read_file, write_file, parse_pipe_delimited
from utils.data_processor import (
    process_sales_data, 
    calculate_total_revenue,
    get_sales_by_region,
    get_top_products
)
from utils.api_handler import enrich_records_with_api_data, get_api_status


def generate_report(valid_records, invalid_records, stats):
    """
    Generate a comprehensive sales report
    
    Args:
        valid_records: List of valid sales records
        invalid_records: List of invalid records with reasons
        stats: Dictionary with processing statistics
        
    Returns:
        String containing the formatted report
    """
    report = []
    report.append("=" * 80)
    report.append("SALES DATA ANALYTICS REPORT")
    report.append("=" * 80)
    report.append("")
    
    # Data Processing Summary
    report.append("DATA PROCESSING SUMMARY")
    report.append("-" * 80)
    report.append(f"Total records processed: {stats['total_records']}")
    report.append(f"Valid records: {stats['valid_records']}")
    report.append(f"Invalid records removed: {stats['invalid_records']}")
    report.append("")
    
    # Invalid Records Details
    if invalid_records:
        report.append("INVALID RECORDS (Removed)")
        report.append("-" * 80)
        for idx, invalid in enumerate(invalid_records[:10], 1):  # Show first 10
            record = invalid['record']
            reason = invalid['reason']
            transaction_id = record.get('TransactionID', 'N/A')
            report.append(f"{idx}. {transaction_id} - {reason}")
        
        if len(invalid_records) > 10:
            report.append(f"... and {len(invalid_records) - 10} more invalid records")
        report.append("")
    
    # Revenue Analysis
    report.append("REVENUE ANALYSIS")
    report.append("-" * 80)
    total_revenue = calculate_total_revenue(valid_records)
    report.append(f"Total Revenue: ${total_revenue:,.2f}")
    report.append("")
    
    # Sales by Region
    report.append("SALES BY REGION")
    report.append("-" * 80)
    region_stats = get_sales_by_region(valid_records)
    for region, data in sorted(region_stats.items(), 
                               key=lambda x: x[1]['total_revenue'], 
                               reverse=True):
        report.append(f"{region}:")
        report.append(f"  Total Revenue: ${data['total_revenue']:,.2f}")
        report.append(f"  Transactions: {data['total_transactions']}")
        report.append(f"  Units Sold: {data['total_quantity']}")
        report.append("")
    
    # Top Products
    report.append("TOP 5 PRODUCTS BY REVENUE")
    report.append("-" * 80)
    top_products = get_top_products(valid_records, 5)
    for idx, (product, revenue) in enumerate(top_products, 1):
        report.append(f"{idx}. {product}: ${revenue:,.2f}")
    report.append("")
    
    # Customer Insights
    report.append("CUSTOMER INSIGHTS")
    report.append("-" * 80)
    unique_customers = len(set(r.get('CustomerID', '') for r in valid_records))
    avg_transaction = total_revenue / len(valid_records) if valid_records else 0
    report.append(f"Unique Customers: {unique_customers}")
    report.append(f"Average Transaction Value: ${avg_transaction:,.2f}")
    report.append("")
    
    report.append("=" * 80)
    report.append("END OF REPORT")
    report.append("=" * 80)
    
    return "\n".join(report)


def main():
    """
    Main function to run the sales analytics system
    """
    print("=" * 80)
    print("SALES DATA ANALYTICS SYSTEM")
    print("=" * 80)
    print()
    
    # Check API status
    print("Checking API status...")
    api_status = get_api_status()
    print(f"API Status: {api_status['status']}")
    print()
    
    # Read sales data
    input_file = "data/sales_data.txt"
    print(f"Reading sales data from {input_file}...")
    
    if not os.path.exists(input_file):
        print(f"Error: {input_file} not found!")
        print("Please ensure the sales_data.txt file is in the data/ directory.")
        return
    
    lines = read_file(input_file)
    
    if not lines:
        print("No data found in file!")
        return
    
    print(f"Successfully read {len(lines) - 1} records (excluding header)")
    print()
    
    # Parse the data
    print("Parsing pipe-delimited data...")
    records = parse_pipe_delimited(lines)
    print(f"Parsed {len(records)} records")
    print()
    
    # Process and clean data
    print("Processing and cleaning data...")
    valid_records, invalid_records, stats = process_sales_data(records)
    print(f"Valid records: {stats['valid_records']}")
    print(f"Invalid records removed: {stats['invalid_records']}")
    print()
    
    # Enrich with API data
    print("Enriching data with API information...")
    enriched_records = enrich_records_with_api_data(valid_records)
    print(f"Successfully enriched {len(enriched_records)} records")
    print()
    
    # Generate report
    print("Generating comprehensive report...")
    report = generate_report(valid_records, invalid_records, stats)
    
    # Save report to file
    output_dir = "output"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    report_file = os.path.join(output_dir, "sales_report.txt")
    write_file(report_file, report)
    
    # Also print to console
    print()
    print(report)
    
    # Save cleaned data
    print()
    print("Saving cleaned data...")
    cleaned_file = os.path.join(output_dir, "cleaned_sales_data.txt")
    
    # Write header
    header = "TransactionID|Date|ProductID|ProductName|Quantity|UnitPrice|CustomerID|Region|Category|Manufacturer|WarrantyMonths\n"
    cleaned_lines = [header]
    
    for record in enriched_records:
        line = f"{record.get('TransactionID', '')}|"
        line += f"{record.get('Date', '')}|"
        line += f"{record.get('ProductID', '')}|"
        line += f"{record.get('ProductName', '')}|"
        line += f"{record.get('Quantity', '')}|"
        line += f"{record.get('UnitPrice', '')}|"
        line += f"{record.get('CustomerID', '')}|"
        line += f"{record.get('Region', '')}|"
        line += f"{record.get('Category', '')}|"
        line += f"{record.get('Manufacturer', '')}|"
        line += f"{record.get('WarrantyMonths', '')}\n"
        cleaned_lines.append(line)
    
    write_file(cleaned_file, "".join(cleaned_lines))
    
    print()
    print("=" * 80)
    print("PROCESSING COMPLETE!")
    print("=" * 80)
    print(f"Report saved to: {report_file}")
    print(f"Cleaned data saved to: {cleaned_file}")


if __name__ == "__main__":
    main()