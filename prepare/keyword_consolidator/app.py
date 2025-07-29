import json
import os
from keyword_mapper import KeywordMapper


def load_datasets():
    """
    Load the Breitbart and Guardian datasets from JSON files.
    
    Returns:
        Dict containing two keys:
        - 'breitbart': List of Breitbart articles
        - 'guardian': List of Guardian articles
    """
    datasets = {}
    
    # Define the dataset files
    dataset_files = {
        'breitbart': 'breitbart.json',
        'guardian': 'guardian.json'
    }
    
    for dataset_name, filename in dataset_files.items():
        try:
            # Check if file exists
            if not os.path.exists(filename):
                raise FileNotFoundError(f"Dataset file '{filename}' not found")
            
            # Load and parse JSON
            with open(filename, 'r', encoding='utf-8') as file:
                data = json.load(file)
                
            datasets[dataset_name] = data
            print(f"✓ Successfully loaded {dataset_name} dataset: {len(data)} articles")
            
        except FileNotFoundError as e:
            print(f"✗ Error loading {dataset_name} dataset: {e}")
            raise
        except json.JSONDecodeError as e:
            print(f"✗ Error parsing {dataset_name} dataset JSON: {e}")
            raise
        except Exception as e:
            print(f"✗ Unexpected error loading {dataset_name} dataset: {e}")
            raise
    
    return datasets


def keywords_collector(datasets):
    """
    Collect all unique keywords from all articles in both datasets.
    
    Args:
        datasets: Dictionary containing 'breitbart' and 'guardian' datasets
        
    Returns:
        List of unique keywords from all articles
    """
    all_keywords = set()  # Using set to automatically handle uniqueness
    
    for dataset_name, articles in datasets.items():
        for article in articles:
            # Check if article has keywords field and it's not empty
            if 'keywords' in article and article['keywords']:
                # Add each keyword to the set
                for keyword in article['keywords']:
                    all_keywords.add(keyword)
    
    # Convert set to sorted list for consistent output
    unique_keywords = sorted(list(all_keywords))
    print(f"✓ Collected {len(unique_keywords)} unique keywords from both datasets")
    
    return unique_keywords


if __name__ == "__main__":
    datasets = load_datasets()
    keywords = keywords_collector(datasets)
    with open('keywords.json', 'w', encoding='utf-8') as f:
        json.dump(keywords, f, indent=2, ensure_ascii=False)
    
    # Create KeywordMapper instance and call keyword_determiner
    mapper = KeywordMapper()
    mapper.keyword_determiner(datasets, keywords) 