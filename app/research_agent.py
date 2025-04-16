from app.brave_client import brave_search
from app.openai_client import generate_openai_summary, generate_followup_questions
from app.web_scraper import WebScraper
from typing import List, Dict

class ResearchAgent:
    def __init__(self):
        self.scraper = WebScraper()
        
    def research(self, query: str) -> Dict:
      
        search_results = brave_search(query)

        urls = [result['url'] for result in search_results]

        scraped_content = self.scraper.batch_fetch(urls)

        summary = generate_openai_summary(query, scraped_content)

        followup_questions = generate_followup_questions(query, summary)
        
        return {
            'summary': summary,
            'sources': scraped_content,
            'search_results': search_results,
            'followup_questions': followup_questions
        }
