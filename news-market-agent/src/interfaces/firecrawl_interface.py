"""
Firecrawl Interface - Connects to Firecrawl API to expand content with related articles
"""
import requests
import logging
from typing import List, Dict, Any, Optional
import os
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

class FirecrawlInterface:
    """Interface for retrieving data from Firecrawl"""
    
    # For demo purposes, we'll mock the API endpoints
    BASE_URL = "https://api.firecrawl.io/v1"
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the Firecrawl interface
        
        Args:
            api_key: Optional API key (defaults to env variable)
        """
        self.api_key = api_key or os.getenv('FIRECRAWL_API_KEY', 'demo_api_key')
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
    
    def search_articles(self, query: str, max_results: int = 10) -> List[Dict[str, Any]]:
        """
        Search for articles related to a query
        
        Args:
            query: Search query
            max_results: Maximum number of results to return
            
        Returns:
            List of article details
        """
        # In a real implementation, this would make an API call to Firecrawl
        # For demo, we'll just return mock data
        try:
            # Simulated API call
            # response = requests.get(
            #     f"{self.BASE_URL}/search",
            #     params={"query": query, "limit": max_results},
            #     headers=self.headers
            # )
            # response.raise_for_status()
            # return response.json()
            
            # Mock data for demo
            return self._get_mock_articles(query, max_results)
        except Exception as e:
            logger.error(f"Error searching articles: {e}")
            return []
    
    def expand_content(self, url: str) -> Dict[str, Any]:
        """
        Expand content from a URL with additional related information
        
        Args:
            url: URL of the article to expand
            
        Returns:
            Dictionary with expanded content
        """
        try:
            # Simulated API call
            # response = requests.get(
            #     f"{self.BASE_URL}/expand",
            #     params={"url": url},
            #     headers=self.headers
            # )
            # response.raise_for_status()
            # return response.json()
            
            # Mock data for demo
            return self._get_mock_expanded_content(url)
        except Exception as e:
            logger.error(f"Error expanding content for {url}: {e}")
            return {}
    
    def find_related_articles(self, article_url: str, max_results: int = 5) -> List[Dict[str, Any]]:
        """
        Find articles related to a specific article
        
        Args:
            article_url: URL of the article to find related content for
            max_results: Maximum number of results to return
            
        Returns:
            List of related article details
        """
        try:
            # Simulated API call
            # response = requests.get(
            #     f"{self.BASE_URL}/related",
            #     params={"url": article_url, "limit": max_results},
            #     headers=self.headers
            # )
            # response.raise_for_status()
            # return response.json()
            
            # Mock data for demo
            return self._get_mock_related_articles(article_url, max_results)
        except Exception as e:
            logger.error(f"Error finding related articles for {article_url}: {e}")
            return []
    
    def _get_mock_articles(self, query: str, max_results: int) -> List[Dict[str, Any]]:
        """Generate mock article data for demo purposes"""
        keywords = query.lower().split()
        articles = []
        
        # Create mock data based on query keywords
        topics = {
            "ai": ["Artificial Intelligence Breakthrough", "Machine Learning Trends", "AI Ethics Debate"],
            "tech": ["Tech Giants Announce New Products", "Technology Sector Update", "Tech Startup Funding"],
            "finance": ["Market Update", "Financial Sector News", "Investment Trends"],
            "crypto": ["Cryptocurrency Market Analysis", "Blockchain Innovation", "DeFi Developments"],
            "startup": ["Startup Funding Rounds", "Emerging Tech Startups", "Venture Capital Trends"]
        }
        
        # Find relevant topics based on keywords
        relevant_titles = []
        for keyword in keywords:
            for topic, titles in topics.items():
                if keyword in topic or topic in keyword:
                    relevant_titles.extend(titles)
        
        # If no relevant topics found, use generic ones
        if not relevant_titles:
            relevant_titles = [
                "Latest Technology News", 
                "Business Updates Today",
                "Market Analysis Report",
                "Industry Trends 2025",
                "Economic Outlook"
            ]
        
        # Create articles
        for i in range(min(max_results, len(relevant_titles))):
            articles.append({
                "id": f"article-{i}",
                "title": relevant_titles[i],
                "url": f"https://firecrawl.io/articles/{i}",
                "summary": f"This article discusses {relevant_titles[i].lower()} and its implications.",
                "published_date": "2025-04-15T12:00:00Z",
                "source": "firecrawl",
                "keywords": [kw for kw in keywords if len(kw) > 2]  # Filter out short words
            })
        
        return articles
    
    def _get_mock_expanded_content(self, url: str) -> Dict[str, Any]:
        """Generate mock expanded content for demo purposes"""
        # Extract an identifier from the URL to create somewhat consistent mocks
        url_parts = url.split('/')
        identifier = url_parts[-1] if url_parts else "unknown"
        
        return {
            "url": url,
            "title": f"Expanded Article {identifier}",
            "content": "This is the full expanded content of the article, including analysis and context.",
            "summary": "A concise summary of the key points in the article.",
            "key_points": [
                "First key insight from the article",
                "Second important point discussed",
                "Critical context for understanding the topic"
            ],
            "sentiment": {
                "score": 0.75,  # -1 to 1 scale
                "label": "positive"
            },
            "entities": [
                {"name": "Company A", "type": "organization"},
                {"name": "Technology X", "type": "product"},
                {"name": "CEO Name", "type": "person"}
            ],
            "source": "firecrawl"
        }
    
    def _get_mock_related_articles(self, article_url: str, max_results: int) -> List[Dict[str, Any]]:
        """Generate mock related articles for demo purposes"""
        # Extract an identifier from the URL to create somewhat consistent mocks
        url_parts = article_url.split('/')
        identifier = url_parts[-1] if url_parts else "unknown"
        
        related_articles = []
        topics = [
            "Follow-up Analysis", 
            "Industry Perspective",
            "Market Reaction",
            "Expert Opinion",
            "Historical Context"
        ]
        
        for i in range(min(max_results, len(topics))):
            related_articles.append({
                "id": f"related-{identifier}-{i}",
                "title": f"{topics[i]}: Related to Article {identifier}",
                "url": f"https://firecrawl.io/articles/related/{identifier}/{i}",
                "summary": f"This article provides {topics[i].lower()} related to the original topic.",
                "published_date": "2025-04-16T12:00:00Z",
                "relevance_score": 0.95 - (i * 0.05),  # Decreasing relevance
                "source": "firecrawl"
            })
        
        return related_articles
