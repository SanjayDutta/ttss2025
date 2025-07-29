import os
from dotenv import load_dotenv
from json_reader import read_json_file
from kg_operation import KnowledgeGraphOperations

def main():
    """
    Main function to demonstrate the JSON reader functionality.
    """
    # Load environment variables from .env file
    load_dotenv()
    
    # Initialize Knowledge Graph Operations
    kg_ops = KnowledgeGraphOperations()
    
    # Example usage of the read_json_file function
    try:
        # Get the JSON file path from environment variable
        json_file_path = os.getenv('NEWS_FILEJSON')
        data = read_json_file(json_file_path)
        print("Successfully read JSON file:")
        print(data)
        
        # Insert data into knowledge graph
        success = kg_ops.insert_data(data)
        if success:
            print("Data successfully inserted into knowledge graph")
        else:
            print("Failed to insert data into knowledge graph")
    except FileNotFoundError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"Error reading JSON file: {e}")

if __name__ == "__main__":
    main() 