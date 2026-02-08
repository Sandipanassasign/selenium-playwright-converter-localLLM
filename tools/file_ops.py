
import os

def read_file(filepath):
    """Reads a file and returns its content as a string."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        print(f"Error reading {filepath}: {e}")
        return None

def write_file(filepath, content):
    """Writes content to a file. Creates directories if needed."""
    try:
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Successfully wrote to {filepath}")
        return True
    except Exception as e:
        print(f"Error writing to {filepath}: {e}")
        return False
