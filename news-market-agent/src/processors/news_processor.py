"""
News Processor - Combines and processes news from multiple sources
"""
import logging
from typing import List, Dict, Any, Optional
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
from datetime import datetime, timedelta

# Local imports
from ..interfaces.hackernews_interface import HackerNewsInterface
from ..interfaces.reddit_interface import RedditInterface
from ..interfaces.firecrawl_interface import FirecrawlInterface

# Setup NLTK for sentiment analysis
try:
    nltk.data.find('vader_lexicon')
except LookupError:
    nltk.download('vader_lexicon')

logger = logging.getLogger(__name__)

class NewsProcessor:
    """Processes and aggregates news from multiple sources"""
    
    def __init__(self):
        """Initialize news processor and its dependencies"""
        self.hackernews = HackerNewsInterface()
        self.reddit = RedditInterface()
        self.firecrawl = FirecrawlInterface()
        self.sentiment_analyzer = SentimentIntensityAnalyzer()
    
    def get_aggregated_news(self, topics: Optional[List[str]] = None, max_items: int = 50) -> List[Dict[str, Any]]:
        """
        Aggregate news from all sources with optional topic filtering
        
        Args:
            topics: Optional list of topics to filter news by
            max_items: Maximum number of news items to return
            
        Returns:
            List of aggregated news items
        """
        # Get news from all sources
        hackernews_items = self.hackernews.get_top_stories(filter_keywords=topics)
        reddit_items = self.reddit.get_all_hot_posts(filter_keywords=topics)
        
        # Combine all items
        all_items = hackernews_items + reddit_items
        
        # Sort by score/popularity
        sorted_items = sorted(all_items, key=lambda x: x.get('score', 0), reverse=True)
        
        # Limit to max_items
        top_items = sorted_items[:max_items]
        
        # Add sentiment analysis to each item
        for item in top_items:
            item['sentiment'] = self._analyze_sentiment(item.get('title', ''))
            
            # Get timestamp if available, otherwise use current time
            timestamp = item.get('time') or item.get('created_utc')
            if timestamp:
                item['timestamp'] = timestamp
                item['datetime'] = datetime.fromtimestamp(timestamp).isoformat()
            else:
                item['timestamp'] = datetime.now().timestamp()
                item['datetime'] = datetime.now().isoformat()
        
        return top_items
    
    def enrich_news_with_firecrawl(self, news_items: List[Dict[str, Any]], max_related: int = 2) -> List[Dict[str, Any]]:
        """
        Enrich news items with additional content from Firecrawl
        
        Args:
            news_items: List of news items to enrich
            max_related: Maximum number of related articles to add per item
            
        Returns:
            Enriched news items
        """
        enriched_items = []
        
        for item in news_items:
            # Skip items without URLs
            if 'url' not in item:
                enriched_items.append(item)
                continue
            
            # Get expanded content
            expanded_content = self.firecrawl.expand_content(item['url'])
            if expanded_content:
                # Add expanded content to the item
                item['expanded_content'] = expanded_content
                
                # Add key points if available
                if 'key_points' in expanded_content:
                    item['key_points'] = expanded_content['key_points']
                
                # Add entities if available
                if 'entities' in expanded_content:
                    item['entities'] = expanded_content['entities']
            
            # Get related articles
            related_articles = self.firecrawl.find_related_articles(item['url'], max_results=max_related)
            if related_articles:
                item['related_articles'] = related_articles
            
            enriched_items.append(item)
        
        return enriched_items
    
    def filter_news_by_date(self, news_items: List[Dict[str, Any]], days: int = 1) -> List[Dict[str, Any]]:
        """
        Filter news items by recency
        
        Args:
            news_items: List of news items to filter
            days: Number of days to include
            
        Returns:
            Filtered news items
        """
        cutoff_time = datetime.now() - timedelta(days=days)
        cutoff_timestamp = cutoff_time.timestamp()
        
        return [item for item in news_items if item.get('timestamp', 0) >= cutoff_timestamp]
    
    def categorize_news(self, news_items: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
        """
        Categorize news items into topics
        
        Args:
            news_items: List of news items to categorize
            
        Returns:
            Dictionary mapping categories to news items
        """
        categories = {
            "technology": ["ai", "tech", "software", "programming", "hardware", "technology", "cyber", "data"],
            "business": ["business", "economic", "market", "finance", "invest", "stock", "startup"],
            "crypto": ["crypto", "bitcoin", "ethereum", "blockchain", "web3", "nft"],
            "science": ["science", "research", "physics", "biology", "chemistry", "medicine"],
            "policy": ["policy", "regulation", "government", "law", "legal", "compliance"]
        }
        
        categorized = {category: [] for category in categories}
        categorized["other"] = []  # For uncategorized items
        
        for item in news_items:
            title = item.get('title', '').lower()
            
            # Check each category
            categorized_flag = False
            for category, keywords in categories.items():
                if any(keyword in title for keyword in keywords):
                    categorized[category].append(item)
                    categorized_flag = True
                    break
            
            # If not categorized, add to "other"
            if not categorized_flag:
                categorized["other"].append(item)
        
        return categorized
    
    def _analyze_sentiment(self, text: str) -> Dict[str, Any]:
        """
        Analyze sentiment of a text using NLTK's VADER
        
        Args:
            text: Text to analyze
            
        Returns:
            Dictionary with sentiment scores and label
        """
        scores = self.sentiment_analyzer.polarity_scores(text)
        
        # Determine sentiment label
        if scores['compound'] >= 0.05:
            label = "positive"
        elif scores['compound'] <= -0.05:
            label = "negative"
        else:
            label = "neutral"
        
        return {
            "compound": round(scores['compound'], 3),
            "positive": round(scores['pos'], 3),
            "negative": round(scores['neg'], 3),
            "neutral": round(scores['neu'], 3),
            "label": label
        }
