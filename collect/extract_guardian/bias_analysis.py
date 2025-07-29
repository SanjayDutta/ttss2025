import asyncio
import aiohttp
import json
import os
import time
from typing import List, Dict, Any
from pathlib import Path
import logging
from tqdm import tqdm

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class GuardianArticleProcessor:
    def __init__(self, max_concurrent_requests: int = 50, timeout: int = 30):
        """
        Initialize the processor with concurrency and timeout settings.
        
        Args:
            max_concurrent_requests: Maximum number of concurrent API requests
            timeout: Timeout for each API request in seconds
        """
        self.max_concurrent_requests = max_concurrent_requests
        self.timeout = timeout
        self.semaphore = asyncio.Semaphore(max_concurrent_requests)
        self.session = None
        
    async def __aenter__(self):
        """Async context manager entry."""
        timeout_config = aiohttp.ClientTimeout(total=self.timeout)
        connector = aiohttp.TCPConnector(limit=self.max_concurrent_requests)
        self.session = aiohttp.ClientSession(
            timeout=timeout_config,
            connector=connector,
            headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
        )
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        if self.session:
            await self.session.close()
    
    async def fetch_article_content(self, url: str) -> Dict[str, Any]:
        """
        Fetch content from a single URL with rate limiting and error handling.
        
        Args:
            url: The URL to fetch content from
            
        Returns:
            Dictionary containing the response data or error information
        """
        async with self.semaphore:  # Rate limiting
            # Add a small delay to be respectful to the API
            await asyncio.sleep(0.1)
            try:
                # Prepare the payload for the API call
                payload = {
                    "url": url,
                    "g_t4_event": "QkVlUCt6R2t1c1VHa2tFYlBmUzJtZz09Ojq8nYynYpngoE2nEZmIm/RX"
                }
                
                # Prepare headers
                headers = {
                    "Content-Type": "application/x-www-form-urlencoded"
                }
                
                # Make POST request to the API endpoint
                async with self.session.post(
                    "https://syntopicon.allsides.com/api/4otest/submit_article_for_rating8.php",
                    data=payload,
                    headers=headers
                ) as response:
                    if response.status == 200:
                        content = await response.text()
                        
                        # Try to parse JSON response to extract article-rating
                        try:
                            json_response = await response.json()
                            
                            # Check if the API returned a failure response
                            if json_response.get('ack') == 'fail':
                                logger.debug(f"API failed for URL {url}: {json_response}")
                                return {
                                    'success': True,
                                    'content': content,
                                    'rating': None,
                                    'explanation': None,
                                    'status_code': response.status,
                                    'url': url,
                                    'api_error': json_response.get('line', 'Unknown error')
                                }
                            
                            # Extract rating data if available
                            rating_data = json_response.get('article-rating', {})
                            rating = rating_data.get('rating')
                            explanation = rating_data.get('explanation')
                            
                            return {
                                'success': True,
                                'content': content,
                                'rating': rating,
                                'explanation': explanation,
                                'status_code': response.status,
                                'url': url
                            }
                        except (json.JSONDecodeError, KeyError) as e:
                            # If response is not JSON or doesn't have expected structure
                            logger.debug(f"JSON parsing error for URL {url}: {e}")
                            return {
                                'success': True,
                                'content': content,
                                'rating': None,
                                'explanation': None,
                                'status_code': response.status,
                                'url': url
                            }
                    else:
                        return {
                            'success': False,
                            'error': f'HTTP {response.status}',
                            'status_code': response.status,
                            'url': url
                        }
            except asyncio.TimeoutError:
                return {
                    'success': False,
                    'error': 'Timeout',
                    'status_code': None,
                    'url': url
                }
            except Exception as e:
                return {
                    'success': False,
                    'error': str(e),
                    'status_code': None,
                    'url': url
                }
    
    async def process_articles_batch(self, articles: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Process a batch of articles by fetching content for each URL.
        
        Args:
            articles: List of article objects with URLs
            
        Returns:
            List of articles with fetched content and bias analysis added (excluding those with None bias_score)
        """
        # Create tasks for all URLs
        tasks = []
        for article in articles:
            if 'url' in article:
                task = self.fetch_article_content(article['url'])
                tasks.append((article, task))
        
        # Execute all tasks concurrently
        results = []
        for article, task in tasks:
            result = await task
            if result['success']:
                article['fetched_content'] = result['content']
                article['bias_score'] = result['rating']
                article['bias_analysis'] = result['explanation']
                article['fetch_status'] = 'success'
                
                # Only include articles that have a valid bias_score
                if article['bias_score'] is not None:
                    print(f"Bias score for article {article.get('id', article.get('url', 'unknown'))}: {article['bias_score']}")
                    results.append(article)
                else:
                    logger.debug(f"Skipping article {article.get('id', 'unknown')} - no bias score received")
            else:
                article['fetch_status'] = 'failed'
                article['fetch_error'] = result['error']
                article['bias_score'] = None
                article['bias_analysis'] = None
                # Skip failed requests as well
                logger.debug(f"Skipping article {article.get('id', 'unknown')} - API request failed: {result['error']}")
        
        return results
    
    def load_json_file(self, file_path: str) -> List[Dict[str, Any]]:
        """
        Load and parse a JSON file containing articles.
        
        Args:
            file_path: Path to the JSON file
            
        Returns:
            List of article objects
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Error loading {file_path}: {e}")
            return []
    
    def save_json_file(self, articles: List[Dict[str, Any]], output_path: str):
        """
        Save processed articles to a JSON file.
        
        Args:
            articles: List of processed article objects
            output_path: Path to save the output file
        """
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(articles, f, indent=2, ensure_ascii=False)
            logger.info(f"Saved {len(articles)} articles to {output_path}")
        except Exception as e:
            logger.error(f"Error saving {output_path}: {e}")
    
    def append_to_json_file(self, articles: List[Dict[str, Any]], output_path: str):
        """
        Append processed articles to a JSON file, creating it if it doesn't exist.
        
        Args:
            articles: List of processed article objects
            output_path: Path to append to
        """
        try:
            # Load existing articles if file exists
            existing_articles = []
            if os.path.exists(output_path):
                try:
                    with open(output_path, 'r', encoding='utf-8') as f:
                        existing_articles = json.load(f)
                except (json.JSONDecodeError, FileNotFoundError):
                    existing_articles = []
            
            # Append new articles
            existing_articles.extend(articles)
            
            # Save back to file
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(existing_articles, f, indent=2, ensure_ascii=False)
            
            logger.info(f"Appended {len(articles)} articles to {output_path} (total: {len(existing_articles)})")
        except Exception as e:
            logger.error(f"Error appending to {output_path}: {e}")
    
    async def process_file(self, input_file: str, output_file: str = None, batch_size: int = 100):
        """
        Process a single JSON file with progress tracking.
        
        Args:
            input_file: Path to input JSON file
            output_file: Path to output JSON file (optional)
            batch_size: Number of articles to process in each batch
        """
        if output_file is None:
            output_file = 'guardian_articles_with_bias_analysis.json'
        
        logger.info(f"Processing {input_file}")
        
        # Load articles
        articles = self.load_json_file(input_file)
        if not articles:
            logger.error(f"No articles found in {input_file}")
            return
        
        logger.info(f"Loaded {len(articles)} articles from {input_file}")
        
        # Process articles in batches
        with tqdm(total=len(articles), desc=f"Processing {os.path.basename(input_file)}") as pbar:
            for i in range(0, len(articles), batch_size):
                batch = articles[i:i + batch_size]
                processed_batch = await self.process_articles_batch(batch)
                pbar.update(len(batch))
                
                # Append processed batch to output file
                self.append_to_json_file(processed_batch, output_file)
                
                # Optional: Save intermediate results
                if (i // batch_size + 1) % 10 == 0:  # Save every 10 batches
                    temp_output = output_file.replace('.json', f'_temp_{i//batch_size}.json')
                    self.save_json_file(processed_batch, temp_output)
        
        # Print statistics
        total_processed = len(processed_batch)
        successful = sum(1 for article in processed_batch if article.get('fetch_status') == 'success')
        failed = sum(1 for article in processed_batch if article.get('fetch_status') == 'failed')
        skipped = len(articles) - total_processed  # Articles that were skipped due to None bias_score
        
        logger.info(f"Processing complete: {successful} saved, {failed} failed, {skipped} skipped (no bias score)")

async def main():
    """Main function to process only filtered_articles_part1.json."""
    # Configuration
    max_concurrent_requests = 10  # Reduced for API rate limiting
    timeout = 30  # seconds
    batch_size = 50  # Smaller batches for better control
    input_file = 'guardian_articles.json'
    output_file = 'guardian_articles_with_bias_analysis.json'
    
    # Check if the specific file exists
    if not os.path.exists(input_file):
        logger.error(f"File {input_file} not found in current directory")
        logger.error("Please run filter.py first to generate the filtered articles files.")
        return
    
    logger.info(f"Processing only {input_file}")
    logger.info(f"Output will be saved to: {output_file}")
    
    # Process the specific file
    async with GuardianArticleProcessor(
        max_concurrent_requests=max_concurrent_requests,
        timeout=timeout
    ) as processor:
        start_time = time.time()
        await processor.process_file(input_file, output_file, batch_size=batch_size)
        end_time = time.time()
        logger.info(f"Completed {input_file} in {end_time - start_time:.2f} seconds")
    
    logger.info(f"Processing complete! Results saved to: {output_file}")

if __name__ == "__main__":
    # Run the async main function
    asyncio.run(main())
