"""
File Handler Module
Handles reading and writing files for the sales analytics system
"""

import sys
sys.path.append('.')

def read_file(file_path):
    """
    Read a file and return its contents as a list of lines

    Args:
        file_path: Path to the file to read

    Returns:
        List of lines from the file
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()
        return lines
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        return []
    except Exception as e:
        print(f"Error reading file: {e}")
        return []

#Run the following in different cell, thanks 

def write_file(file_path, content):
    """
    Write content to a file

    Args:
        file_path: Path to the file to write
        content: String content to write to file
    """
    try:
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(content)
        print(f"Successfully wrote to {file_path}")
    except Exception as e:
        print(f"Error writing to file: {e}")


def parse_pipe_delimited(lines):
    """
    Parse pipe-delimited data into a list of dictionaries

    Args:
        lines: List of lines from the file

    Returns:
        List of dictionaries representing each record
    """
    if not lines:
        return []

    # First line is the header
    header = lines[0].strip().split('|')

    records = []
    for line in lines[1:]:
        if line.strip():  # Skip empty lines
            values = line.strip().split('|')
            record = dict(zip(header, values))
            records.append(record)

    return records

#Run the following in different cell, thanks 

!mkdir -p utils

#Run the following in different cell, thanks 

%%writefile utils/file_handler.py

def read_sales_data(file_name):
    """
    Reads sales data from file handling encoding issues.
    Returns: list of raw transaction lines
    """

    encodings_to_try = ['utf-8', 'latin-1', 'cp1252']
    raw_lines = []

    for enc in encodings_to_try:
        try:
            with open(file_name, 'r', encoding=enc) as file:
                raw_lines = file.readlines()
            break
        except UnicodeDecodeError:
            continue
        except FileNotFoundError:
            print(f"❌ Error: File not found -> {file_name}")
            return []

    # Skip header & remove empty lines
    lines = []
    for line in raw_lines[1:]:
        line = line.strip()
        if line:
            lines.append(line)

    return lines

#Run the following in different cell, thanks 

from utils.file_handler import read_sales_data

lines = read_sales_data(file_path)

print("Total transaction lines:", len(lines))
print("First 5 lines:")
for l in lines[:5]:
    print(l)
