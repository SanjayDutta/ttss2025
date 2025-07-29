import re
import json
import time
import html
from datetime import datetime

import requests
from bs4 import BeautifulSoup

GUARDIAN_API_KEY = "4708ec41-326f-47f8-8f41-4add2f086c4d"

def format_date(date_str):
    try:
        dt = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%SZ")
    except ValueError:
        try:
            dt = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S%z")
        except ValueError:
            try:
                dt = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S.%fZ")
            except:
                return "Unknown"
    return dt.strftime("%d-%m-%Y")

def clean_html(raw_html):
    """Removes HTML tags, unescapes entities, strips problematic Unicode, and normalizes spaces while preserving line breaks."""
    soup = BeautifulSoup(raw_html, "html.parser")
    text = soup.get_text(separator=' ')
    text = html.unescape(text)
    text = text.replace('\u2028', '\n').replace('\u2029', '\n').replace('\u00A0', ' ')
    text = re.sub(r' +', ' ', text)
    return text.strip()


def fetch_guardian_articles(query, from_date, to_date, start_page=1, max_pages=500, page_size=200):
    endpoint = "https://content.guardianapis.com/search"
    all_articles = []

    for page in range(start_page, start_page + max_pages):
        params = {
            'api-key': GUARDIAN_API_KEY,
            'from-date': from_date,
            'to-date': to_date,
            'show-fields': 'byline,body,trailText',
            'show-tags': 'keyword',
            'page-size': page_size,
            'page': page
        }

        if query:
            params['q'] = query

        try:
            print(f"Fetching page {page}...")
            response = requests.get(endpoint, params=params)
            response.raise_for_status()
            data = response.json()

            results = data['response'].get('results', [])
            if not results:
                print("No more results.")
                break

            for result in results:
                raw_content = result.get('fields', {}).get('body') or result.get('fields', {}).get('trailText') or ""
                clean_content = clean_html(raw_content)
                keywords = [tag.get('webTitle', "") for tag in result.get('tags', []) if tag.get('type') == 'keyword']

                all_articles.append({
                    "id": result.get("id"),
                    "source": "The Guardian",
                    "url": result.get("webUrl"),
                    "title": result.get("webTitle"),
                    "author": result.get('fields', {}).get('byline', "N/A"),
                    "content": clean_content,
                    "genre": result.get("sectionName", "N/A"),
                    "date": format_date(result.get("webPublicationDate")),
                    "keywords": keywords
                })

            print(f"Page {page} fetched: {len(results)} articles")

            if page >= data['response'].get('pages', page):
                print("Reached the last page available.")
                break

            time.sleep(2)  

        except Exception as e:
            print(f"Error on page {page}: {e}")
            break

    return all_articles

if __name__ == "__main__":
    from_date = "2023-01-01"
    to_date = "2025-06-22"
    start_page = int(input("Enter starting page (default 1): ") or 1)
    max_pages = int(input("Enter number of pages to fetch (max 500): ") or 2)
    max_pages = min(max_pages, 500)

    articles = fetch_guardian_articles(
        query=None,
        from_date=from_date,
        to_date=to_date,
        start_page=start_page,
        max_pages=max_pages
    )

    output_file = "guardian_articles.json"

    try:
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(articles, f, ensure_ascii=False, indent=4)
        print(f"{len(articles)} articles saved to '{output_file}'.")
    except Exception as e:
        print("Error writing to file:", e)
