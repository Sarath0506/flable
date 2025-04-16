import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import time
from typing import List, Dict
import logging

class WebScraper:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
    def fetch_content(self, url: str) -> Dict:
        """Fetch and parse content from a URL"""
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
 
            for element in soup(['script', 'style', 'nav', 'footer', 'header']):
                element.decompose()
  
            content = {
                'title': self._get_title(soup),
                'text': self._get_main_text(soup),
                'url': url,
                'domain': urlparse(url).netloc
            }
            
            return content
            
        except Exception as e:
            logging.error(f"Error scraping {url}: {str(e)}")
            return None

    def _get_title(self, soup) -> str:
        """Extract title from the page"""
        title = soup.find('title')
        return title.text.strip() if title else "No title found"

    def _get_main_text(self, soup) -> str:
        """Extract main text content from the page"""
       
        main_content = soup.find('main') or soup.find('article') or soup.find('div', class_='content')
        
        if main_content:
            return ' '.join(main_content.stripped_strings)
 
        return ' '.join(soup.body.stripped_strings) if soup.body else "No content found"

    def batch_fetch(self, urls: List[str], max_workers: int = 5) -> List[Dict]:
        """Fetch content from multiple URLs with rate limiting"""
        results = []
        for url in urls:
            content = self.fetch_content(url)
            if content:
                results.append(content)
            time.sleep(1)
        return results 