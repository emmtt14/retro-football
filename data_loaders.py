# data_loaders.py
import json
import os

def load_json_data(filepath):
    """
    Loads and returns data from a specified JSON file.
    Handles potential FileNotFoundError and JSON decoding errors.
    """
    if not os.path.exists(filepath):
        print(f"Error: Data file not found at {filepath}")
        return None
    try:
        with open(filepath, 'r') as f:
            data = json.load(f)
        return data
    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON from {filepath}. Check file format.")
        return None
    except Exception as e:
        print(f"An unexpected error occurred while loading {filepath}: {e}")
        return None

def save_json_data(data, filepath):
    """
    Saves data to a specified JSON file.
    """
    try:
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=4)
        print(f"Data saved to {filepath}")
    except Exception as e:
        print(f"Error saving data to {filepath}: {e}")

# Example Usage: (Not typically run directly, but used by other modules)
if __name__ == "__main__":
    # Create a dummy data file for demonstration
    dummy_data = {
        "team_names": ["Redbacks", "Bluebirds", "Greenbacks"],
        "positions": ["QB", "RB", "WR", "DE", "LB"]
    }
    filepath = "dummy_data.json"
    save_json_data(dummy_data, filepath)
    
    # Load the data back
    loaded_data = load_json_data(filepath)
    if loaded_data:
        print("\nSuccessfully loaded data:")
        print(loaded_data)
        
    # Clean up the dummy file
    os.remove(filepath)
