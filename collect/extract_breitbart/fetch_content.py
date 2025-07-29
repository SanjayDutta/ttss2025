import requests
import time
import json
from fetch_sitemaps import run
from lxml import etree
from bs4 import BeautifulSoup
import warnings
from bs4 import XMLParsedAsHTMLWarning
warnings.filterwarnings("ignore", category=XMLParsedAsHTMLWarning)

def fetch_content(html_content):
    """Extract author and article content from HTML response"""
    try:
       
        soup = BeautifulSoup(html_content, 'html.parser')
       
        # Extract author from meta tag
        author = ""
        author_meta = soup.find('meta', attrs={'name': 'author'})
        if author_meta and author_meta.get('content'):
            author = author_meta['content'].strip()
        
        # Extract article content from div.entry-content
        article_content = ""
        entry_content = soup.find('div', class_='entry-content')
        if entry_content:
            # Get all <p> tags within entry-content
            paragraphs = entry_content.find_all('p')
            article_content = ' '.join([p.get_text().strip() for p in paragraphs if p.get_text().strip()])
        
        return {
            'author': author,
            'article_content': article_content
        }
        
    except Exception as e:
        print(f"Error parsing HTML content: {e}")
        return {'author': '', 'article_content': ''}
    
def get_bias(url):
    """Make API call to get Bias"""
    try:
        print("USING API")
        print(url)
        response = requests.post(
            "https://syntopicon.allsides.com/api/4otest/submit_article_for_rating8.php",
            data={
                "url": url,
                "g_t4_event": "QkVlUCt6R2t1c1VHa2tFYlBmUzJtZz09Ojq8nYynYpngoE2nEZmIm/RX"
            },
            headers={
                "Content-Type": "application/x-www-form-urlencoded"
            }
        )
        return response.json()
    except Exception as e:
        print(f"Error getting bias: {e}")
        return {'article-rating': {'rating': 'N/A', 'explanation': 'N/A'}}


def app(extracted_data):
    count = 0
    entry_dump = []
    for entry in extracted_data:    
        print("Processing: ", count)    
        response = requests.get(entry['loc'])        
        result = fetch_content(response.text)   
        
        # Extract genre from URL
        url_parts = entry['loc'].split('/')
        genre = url_parts[3] if len(url_parts) > 3 else ''
        
        # Fetch the date from the url
        date = entry['loc'].split('/')
        #print(date[6])

        #Make API call to get Bias
        bias = get_bias(entry['loc'])

        
        #check if article-rating is in bias
        if 'article-rating' in bias:
            bias_score = bias['article-rating']['rating']
            bias_analysis = bias['article-rating']['explanation']
        else:
            bias_score = 'N/A'
            bias_analysis = 'N/A'

        print("--------------------------------")
        print({
                'url': entry['loc'],
                'title': entry['news_title'],
                'author': result['author'],
                'content': result['article_content'],
                'genre': genre,
                "date": date[6]+"-"+date[5]+"-"+date[4],
                "bias_score": bias_score,
                "bias_analysis": bias_analysis,
                "keywords": entry['news_keywords'],
                "source": "Breitbart News Network"
            })
        
        entry_dump.append(
            {
                'url': entry['loc'],
                'title': entry['news_title'],
                'author': result['author'],
                'content': result['article_content'],
                'genre': genre,
                "date": date[6]+"-"+date[5]+"-"+date[4],
                "bias_score": bias_score,
                "bias_analysis": bias_analysis,
                "keywords": entry['news_keywords'],
                "source": "Breitbart News Network"
            }
        )
        #0.5s second delay
        time.sleep(0.5)
        count += 1
    with open('result.json', 'a', encoding='utf-8') as f:
        for entry in entry_dump:
            f.write(json.dumps(entry, ensure_ascii=False))
            f.write(',\n')
if __name__ == "__main__":
    app()