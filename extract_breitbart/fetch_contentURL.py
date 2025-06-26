import requests
import time
from fetch_sitemaps import run
from fetch_content import app as fetch_content
from lxml import etree

def extract_xml_content(xml_content):
    """Extract specific content from XML response"""
    try:
        # Parse the XML content
        parser = etree.XMLParser(remove_blank_text=True)
        root = etree.fromstring(xml_content.encode('utf-8'), parser)
        
        # Define the namespace for news elements
        namespaces = {
            'news': 'http://www.google.com/schemas/sitemap-news/0.9',
            'sitemap': 'http://www.sitemaps.org/schemas/sitemap/0.9'
        }
        
        extracted_data = []
        
        # Extract all URL entries
        url_elements = root.xpath("//sitemap:url", namespaces=namespaces)
        
        for url_elem in url_elements:
            entry = {}
            
            # Extract <loc> tag content
            loc_elem = url_elem.xpath(".//sitemap:loc", namespaces=namespaces)
            if loc_elem:
                entry['loc'] = loc_elem[0].text.strip()
            
            # Extract <news:title> tag content
            title_elem = url_elem.xpath(".//news:title", namespaces=namespaces)
            if title_elem:
                entry['news_title'] = title_elem[0].text.strip()
            
            # Extract <news:language> tag content
            language_elem = url_elem.xpath(".//news:language", namespaces=namespaces)
            if language_elem:
                entry['news_language'] = language_elem[0].text.strip()

            # Extract <news:keywords> tag content
            keywords_elem = url_elem.xpath(".//news:keywords", namespaces=namespaces)
            if keywords_elem:
                keywords_string= keywords_elem[0].text.strip()
                keywords_list = keywords_string.split(', ')
                entry['news_keywords'] = keywords_list
            
            if entry:  # Only add if we found some data
                extracted_data.append(entry)
        
        return extracted_data
        
    except Exception as e:
        print(f"Error parsing XML content: {e}")
        return []
    
def write_to_file(extracted_data):
    output_file = "extracted_content.txt"
    with open(output_file, 'a', encoding='utf-8') as f:
        for entry in extracted_data:
            f.write("--- Entry ---\n")
            f.write(f"Location: {entry['loc']}\n")
            f.write(f"Title: {entry['news_title']}\n")
            f.write(f"Language: {entry['news_language']}\n")
            f.write("\n")

def app():
    urls = run()
    print(f"Processing {len(urls)} URLs...")
    
    all_extracted_data = []
    #add [ to result.json
    with open('result.json', 'w') as f:
        f.write('[')

    for i, url in enumerate(urls, 1):
        print(f"Processing URL {i}/{len(urls)}: {url}")
        
        try:
            response = requests.get(url)
            response.raise_for_status()  # Raise an exception for bad status codes
            xml_content = response.text
            
            # Extract the specific content we need
            extracted_data = extract_xml_content(xml_content)
            
            if extracted_data:
                all_extracted_data.extend(extracted_data)
                print(f"  Found {len(extracted_data)} entries")                
                fetch_content(extracted_data)
                break
                #write_to_file(extracted_data)
            else:
                print(f"  No relevant data found")
            #one second delay
            time.sleep(1)    
        except requests.RequestException as e:
            print(f"  Error fetching URL: {e}")
        except Exception as e:
            print(f"  Error processing URL: {e}")
        
        # Uncomment the break below if you want to test with just one URL
        #return extracted_data
        #break
    #add ] to result.json
    with open('result.json', 'a') as f:
        f.write('{"news-organization": "Breitbart"}')
        f.write(']')
    print(f"Results saved to: result.json")
    print(f"Extracted {len(all_extracted_data)} entries total")
   
"""
if __name__ == "__main__":
    all_extracted_data =app()
    output_file = "extracted_content.txt"
    with open(output_file, 'w', encoding='utf-8') as f:
        for entry in all_extracted_data:
            f.write("--- Entry ---\n")
            if 'loc' in entry:
                f.write(f"Location: {entry['loc']}\n")
            if 'news_title' in entry:
                f.write(f"Title: {entry['news_title']}\n")
            if 'news_language' in entry:
                f.write(f"Language: {entry['news_language']}\n")
            f.write("\n")
        
    print(f"\nExtracted {len(all_extracted_data)} entries total")
    print(f"Results saved to: {output_file}")"""

if __name__ == "__main__":
    app()