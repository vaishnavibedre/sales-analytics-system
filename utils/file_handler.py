"""
File Handler Module
Handles reading and writing files for the sales analytics system
"""

def read_file(filepath):
    """
    Read a file and return its contents as a list of lines
    
    Args:
        filepath: Path to the file to read
        
    Returns:
        List of lines from the file
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            lines = file.readlines()
        return lines
    except FileNotFoundError:
        print(f"Error: File '{filepath}' not found.")
        return []
    except Exception as e:
        print(f"Error reading file: {e}")
        return []


def write_file(filepath, content):
    """
    Write content to a file
    
    Args:
        filepath: Path to the file to write
        content: String content to write to file
    """
    try:
        with open(filepath, 'w', encoding='utf-8') as file:
            file.write(content)
        print(f"Successfully wrote to {filepath}")
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
