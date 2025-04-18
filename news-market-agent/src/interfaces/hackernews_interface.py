"""
HackerNews Interface - Connects to HackerNews API to retrieve tech news stories
"""
import requests
import logging
from typing import List, Dict, Any, Optional

logger = logging.getLogger(__name__)

class HackerNewsInterface:
    """Interface for retrieving data from HackerNews"""

    BASE_URL = "https://hacker-news.firebaseio.com/v0"
    ITEM_URL = f"{BASE_URL}/item"
    TOP_STORIES_URL = f"{BASE_URL}/topstories.json"
    
    def __init__(self, max_stories: int = 30):
        """
        Initialize the HackerNews interface
        
        Args:
            max_stories: Maximum number of stories to retrieve
        """
        self.max_stories = max_stories
    
    def get_top_story_ids(self) -> List[int]:
        """Get IDs of top stories from HackerNews"""
        try:
            response = requests.get(self.TOP_STORIES_URL)
            response.raise_for_status()
            
            story_ids = response.json()
            return story_ids[:self.max_stories]
        except Exception as e:
            logger.error(f"Error retrieving top story IDs: {e}")
            return []
    
    def get_story_details(self, story_id: int) -> Optional[Dict[str, Any]]:
        """Get details for a specific story by ID"""
        try:
            response = requests.get(f"{self.ITEM_URL}/{story_id}.json")
            response.raise_for_status()
            
            story = response.json()
            if not story or 'title' not in story:
                return None
                
            return {
                'id': story.get('id'),
                'title': story.get('title'),
                'url': story.get('url'),
                'score': story.get('score', 0),
                'by': story.get('by'),
                'time': story.get('time'),
                'descendants': story.get('descendants', 0),
                'source': 'hackernews'
            }
        except Exception as e:
            logger.error(f"Error retrieving story {story_id}: {e}")
            return None
    
    def get_top_stories(self, filter_keywords: Optional[List[str]] = None) -> List[Dict[str, Any]]:
        """
        Retrieve top stories from HackerNews
        
        Args:
            filter_keywords: Optional list of keywords to filter stories by
            
        Returns:
            List of story details
        """
        story_ids = self.get_top_story_ids()
        stories = []
        
        for story_id in story_ids:
            story = self.get_story_details(story_id)
            if story:
                # Apply keyword filtering if provided
                if filter_keywords:
                    if any(keyword.lower() in story['title'].lower() for keyword in filter_keywords):
                        stories.append(story)
                else:
                    stories.append(story)
                    
        return stories
