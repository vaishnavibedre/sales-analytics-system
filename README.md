# Sales Analytics System

## Author  
**Vaishnavi Bedre**  
**Student ID:** bitsom_ba_25071050  

---

## 📌 Project Overview

The **Sales Analytics System** is a modular Python application designed to process raw sales data, enrich it using a simulated API, and generate a comprehensive analytical report.  
The project follows a clean, maintainable architecture suitable for academic evaluation and real‑world extensibility.

---

## 🗂️ Repository Structure

```
sales-analytics-system/
│
├── README.md
├── main.py
├── requirements.txt
│
├── utils/
│   ├── file_handler.py
│   ├── data_processor.py
│   ├── api_handler.py
│   └── report_generator.py
│
├── data/
│   ├── sales_data.txt
│   └── enriched_sales_data.txt
│
└── output/
    ├── report.txt
    └── sales_report.txt
```

---

## 🔧 Module Responsibilities

### **utils/file_handler.py**
Handles all file operations:
- Reads raw sales data from `data/sales_data.txt`
- Writes enriched data to `data/enriched_sales_data.txt`
- Saves the final report to `output/report.txt`
- Provides safe error handling for missing or corrupted files

---

### **utils/data_processor.py**
Transforms and validates raw data:
- Parses text rows into structured Python dictionaries
- Cleans malformed or incomplete entries
- Converts numeric fields (price, quantity)
- Computes derived metrics such as revenue
- Prepares data for enrichment and reporting

---

### **utils/api_handler.py**
Simulates an external API:
- Adds mock metadata (region, category, discount flags)
- Introduces artificial latency to mimic real API calls
- Ensures consistent enrichment fields for each transaction

---

### **utils/report_generator.py**
Generates a structured analytical report:
- Total revenue and transaction summary
- Region-wise sales distribution
- Top-performing products
- Daily sales trends and peak sales day
- Clean, readable text output saved to `output/report.txt`

---

### **main.py**
The orchestrator of the entire workflow:
1. Load raw data using `file_handler`
2. Process and validate data using `data_processor`
3. Enrich data using `api_handler`
4. Generate analytics using `report_generator`
5. Save the final report to `output/report.txt`
6. Display progress logs in the console

---

## ▶️ How to Run the System

### **1. Install Dependencies**
```bash
pip install -r requirements.txt
```

### **2. Run the Application**
```bash
python main.py
```

### **3. Output Files Generated**
- Enriched dataset: `data/enriched_sales_data.txt`
- Final report: `output/report.txt`

Console logs will show each stage of the workflow.

---

## 📊 Sample Report Output (Excerpt)

```
=== SALES ANALYTICS REPORT ===

Total Valid Transactions: 100
Total Revenue: ₹1,234,560

Top 5 Products by Revenue:
1. Wireless Mouse – ₹45,000
2. Laptop Stand – ₹38,200
...

Region-wise Sales:
North: ₹320,000
South: ₹280,000
East: ₹310,000
West: ₹324,560

Peak Sales Day:
2024-12-15 with 18 transactions
```

*(Values shown are illustrative.)*

---

## ⭐ Key Features

- Robust parsing and cleaning of raw sales data  
- Graceful handling of malformed rows  
- API‑style enrichment with mock metadata  
- Revenue, region, and product‑level analytics  
- Daily trend analysis and peak sales detection  
- Modular architecture for easy extension  
- Clear, human‑readable final report  

---

## 🧪 Included Test Data

- `data/sales_data.txt` — raw input  
- `data/enriched_sales_data.txt` — enriched output  
- `output/report.txt` — final analytics report
---