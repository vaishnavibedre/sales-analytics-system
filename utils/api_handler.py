"""
API Handler Module
Handles API requests for product information
"""

import json

def fetch_product_info(product_id):
    """
    Fetch product information from external API
    
    Note: This is a mock implementation since we don't have a real API endpoint.
    In a real implementation, you would use the requests library:
    
    import requests
    response = requests.get(f'https://api.example.com/products/{product_id}')
    return response.json()
    
    Args:
        product_id: Product ID to fetch information for
        
    Returns:
        Dictionary with product information
    """
    # Mock product database
    mock_products = {
        'P101': {
            'product_id': 'P101',
            'name': 'Laptop Premium',
            'category': 'Electronics',
            'manufacturer': 'TechCorp',
            'warranty_months': 24
        },
        'P102': {
            'product_id': 'P102',
            'name': 'Wireless Mouse',
            'category': 'Accessories',
            'manufacturer': 'PeripheralCo',
            'warranty_months': 12
        },
        'P103': {
            'product_id': 'P103',
            'name': 'Mechanical Keyboard',
            'category': 'Accessories',
            'manufacturer': 'KeyMasters',
            'warranty_months': 12
        },
        'P104': {
            'product_id': 'P104',
            'name': 'LED Monitor',
            'category': 'Electronics',
            'manufacturer': 'DisplayTech',
            'warranty_months': 36
        },
        'P105': {
            'product_id': 'P105',
            'name': 'HD Webcam',
            'category': 'Electronics',
            'manufacturer': 'VisionTech',
            'warranty_months': 12
        },
        'P106': {
            'product_id': 'P106',
            'name': 'Headphones',
            'category': 'Audio',
            'manufacturer': 'SoundPro',
            'warranty_months': 18
        },
        'P107': {
            'product_id': 'P107',
            'name': 'USB Cable',
            'category': 'Accessories',
            'manufacturer': 'CableCo',
            'warranty_months': 6
        },
        'P108': {
            'product_id': 'P108',
            'name': 'External Hard Drive 1TB',
            'category': 'Storage',
            'manufacturer': 'DataSafe',
            'warranty_months': 24
        },
        'P109': {
            'product_id': 'P109',
            'name': 'Gaming Wireless Mouse',
            'category': 'Accessories',
            'manufacturer': 'GameGear',
            'warranty_months': 12
        },
        'P110': {
            'product_id': 'P110',
            'name': 'Laptop Charger 65W',
            'category': 'Accessories',
            'manufacturer': 'PowerPlus',
            'warranty_months': 12
        }
    }
    
    return mock_products.get(product_id, {
        'product_id': product_id,
        'name': 'Unknown Product',
        'category': 'Unknown',
        'manufacturer': 'Unknown',
        'warranty_months': 0
    })


def enrich_records_with_api_data(records):
    """
    Enrich sales records with additional product information from API
    
    Args:
        records: List of sales record dictionaries
        
    Returns:
        List of enriched records
    """
    enriched_records = []
    
    for record in records:
        product_id = record.get('ProductID', '')
        
        # Fetch product info from API
        product_info = fetch_product_info(product_id)
        
        # Create enriched record
        enriched = record.copy()
        enriched['Category'] = product_info.get('category', 'Unknown')
        enriched['Manufacturer'] = product_info.get('manufacturer', 'Unknown')
        enriched['WarrantyMonths'] = product_info.get('warranty_months', 0)
        
        enriched_records.append(enriched)
    
    return enriched_records


def get_api_status():
    """
    Check API availability status
    
    Returns:
        Dictionary with API status information
    """
    # In a real implementation, you would ping the actual API
    return {
        'status': 'available',
        'message': 'Mock API is running',
        'products_available': 10
    }
