"""
Data Processor Module
Handles data cleaning and validation for sales records
"""

def clean_numeric_field(value):
    """
    Remove commas from numeric fields and convert to appropriate type
    
    Args:
        value: String value that may contain commas
        
    Returns:
        Cleaned numeric value (int or float)
    """
    if not value:
        return 0
    
    # Remove commas
    cleaned = value.replace(',', '')
    
    # Try to convert to int first, then float
    try:
        if '.' in cleaned:
            return float(cleaned)
        else:
            return int(cleaned)
    except ValueError:
        return 0


def is_valid_transaction_id(transaction_id):
    """
    Check if transaction ID starts with 'T'
    
    Args:
        transaction_id: Transaction ID to validate
        
    Returns:
        Boolean indicating if valid
    """
    return transaction_id and transaction_id.startswith('T')


def clean_product_name(product_name):
    """
    Remove commas from product names
    
    Args:
        product_name: Product name that may contain commas
        
    Returns:
        Cleaned product name
    """
    return product_name.replace(',', ' ') if product_name else product_name


def is_valid_record(record):
    """
    Check if a record should be removed based on cleaning criteria
    
    Args:
        record: Dictionary representing a sales record
        
    Returns:
        Tuple (is_valid, reason) - Boolean and string explaining why invalid
    """
    # Check if TransactionID starts with 'T'
    if not is_valid_transaction_id(record.get('TransactionID', '')):
        return False, "Invalid TransactionID"
    
    # Check if CustomerID is missing
    if not record.get('CustomerID', '').strip():
        return False, "Missing CustomerID"
    
    # Check if Region is missing
    if not record.get('Region', '').strip():
        return False, "Missing Region"
    
    # Check if Quantity <= 0
    quantity = clean_numeric_field(record.get('Quantity', '0'))
    if quantity <= 0:
        return False, "Invalid Quantity"
    
    # Check if UnitPrice <= 0
    unit_price = clean_numeric_field(record.get('UnitPrice', '0'))
    if unit_price <= 0:
        return False, "Invalid UnitPrice"
    
    return True, "Valid"


def clean_record(record):
    """
    Clean a valid record by removing commas from product names and numbers
    
    Args:
        record: Dictionary representing a sales record
        
    Returns:
        Cleaned record dictionary
    """
    cleaned = record.copy()
    
    # Clean ProductName
    if 'ProductName' in cleaned:
        cleaned['ProductName'] = clean_product_name(cleaned['ProductName'])
    
    # Clean numeric fields
    if 'Quantity' in cleaned:
        cleaned['Quantity'] = str(clean_numeric_field(cleaned['Quantity']))
    
    if 'UnitPrice' in cleaned:
        cleaned['UnitPrice'] = str(clean_numeric_field(cleaned['UnitPrice']))
    
    return cleaned


def process_sales_data(records):
    """
    Process sales data: validate and clean records
    
    Args:
        records: List of record dictionaries
        
    Returns:
        Tuple (valid_records, invalid_records, stats)
    """
    valid_records = []
    invalid_records = []
    
    for record in records:
        is_valid, reason = is_valid_record(record)
        
        if is_valid:
            cleaned = clean_record(record)
            valid_records.append(cleaned)
        else:
            invalid_records.append({
                'record': record,
                'reason': reason
            })
    
    stats = {
        'total_records': len(records),
        'valid_records': len(valid_records),
        'invalid_records': len(invalid_records)
    }
    
    return valid_records, invalid_records, stats


def calculate_total_revenue(records):
    """
    Calculate total revenue from valid records
    
    Args:
        records: List of valid record dictionaries
        
    Returns:
        Total revenue as float
    """
    total = 0
    for record in records:
        quantity = clean_numeric_field(record.get('Quantity', '0'))
        unit_price = clean_numeric_field(record.get('UnitPrice', '0'))
        total += quantity * unit_price
    
    return total


def get_sales_by_region(records):
    """
    Calculate sales statistics by region
    
    Args:
        records: List of valid record dictionaries
        
    Returns:
        Dictionary with region as key and stats as value
    """
    region_stats = {}
    
    for record in records:
        region = record.get('Region', 'Unknown')
        quantity = clean_numeric_field(record.get('Quantity', '0'))
        unit_price = clean_numeric_field(record.get('UnitPrice', '0'))
        revenue = quantity * unit_price
        
        if region not in region_stats:
            region_stats[region] = {
                'total_revenue': 0,
                'total_transactions': 0,
                'total_quantity': 0
            }
        
        region_stats[region]['total_revenue'] += revenue
        region_stats[region]['total_transactions'] += 1
        region_stats[region]['total_quantity'] += quantity
    
    return region_stats


def get_top_products(records, top_n=5):
    """
    Get top N products by revenue
    
    Args:
        records: List of valid record dictionaries
        top_n: Number of top products to return
        
    Returns:
        List of tuples (product_name, revenue)
    """
    product_revenue = {}
    
    for record in records:
        product = record.get('ProductName', 'Unknown')
        quantity = clean_numeric_field(record.get('Quantity', '0'))
        unit_price = clean_numeric_field(record.get('UnitPrice', '0'))
        revenue = quantity * unit_price
        
        if product not in product_revenue:
            product_revenue[product] = 0
        
        product_revenue[product] += revenue
    
    # Sort by revenue descending
    sorted_products = sorted(product_revenue.items(), key=lambda x: x[1], reverse=True)
    
    return sorted_products[:top_n]
