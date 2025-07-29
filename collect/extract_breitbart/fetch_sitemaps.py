#!/usr/bin/env python3
"""
Date Filtered Locs Extractor
Extracts all <loc> values from XML where the date in the URL ranges from 
January 1, 2020 to June 1, 2025.
"""

import re
from datetime import datetime
from lxml import etree
import sys


def extract_locs_by_date_range(xml_file_path, start_date, end_date):   
    try:
        # Parse the XML file
        parser = etree.XMLParser(remove_blank_text=True)
        tree = etree.parse(xml_file_path, parser)
        root = tree.getroot()
        
        # Extract all <loc> elements using local-name() to handle default namespace
        loc_elements = root.xpath("//*[local-name()='loc']")
        
        
        # Extract text content from each <loc> element
        urls = []
        for element in loc_elements:
            if element.text and element.text.strip():
                urls.append(element.text.strip())
        
        # Filter URLs by date range
        filtered_urls = []
        for url in urls:
            # Extract date from URL using regex
            # Pattern: sitemap_news-YYYY-MM-DD
            match = re.search(r'sitemap_news-(\d{4})-(\d{2})-(\d{2})', url)
            if match:
                try:
                    year = int(match.group(1))
                    month = int(match.group(2))
                    day = int(match.group(3))
                    url_date = datetime(year, month, day)
                    
                    # Check if date is within range
                    if start_date <= url_date <= end_date:
                        filtered_urls.append(url)
                except ValueError:
                    # Skip URLs with invalid dates
                    continue
        
        return filtered_urls
        
    except Exception as e:
        print(f"Error processing XML file: {e}")
        return []


def run():
    """Main function to execute the date-filtered loc extraction."""
    
    # Configuration
    xml_file = "breitbart_sitemap.xml"
    start_date = datetime(2025, 1, 1)  # January 1, 2025
    end_date = datetime(2025, 6, 22)    # June 22, 2025
    
    print("=== Date Filtered Locs Extractor ===")
    print(f"XML File: {xml_file}")
    print(f"Date Range: {start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}")
    print("-" * 50)
    
    # Extract and filter URLs
    filtered_urls = extract_locs_by_date_range(xml_file, start_date, end_date)
    
    # Display results
    if filtered_urls:
        output_file = "daily_sitemaps.txt"
        with open(output_file, 'w') as f:            
            for url in filtered_urls:                
                f.write(url + "\n")
        
        print(f"\nResults saved to: {output_file}")
        
    else:
        print("No URLs found within the specified date range.")
    
    print("\nExtraction completed!")
    return filtered_urls


if __name__ == "__main__":
    run() 