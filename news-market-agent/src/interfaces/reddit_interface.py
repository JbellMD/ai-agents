"""
Reddit Interface - Connects to Reddit API to retrieve news and discussions
"""
import praw
import logging
from typing import List, Dict, Any, Optional
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

class RedditInterface:
    """Interface for retrieving data from Reddit"""
    
    def __init__(self, subreddits: List[str] = None, post_limit: int = 25):
        """
        Initialize the Reddit interface
        
        Args:
            subreddits: List of subreddits to monitor
            post_limit: Maximum number of posts to retrieve per subreddit
        """
        # Default business and tech subreddits if none provided
        self.subreddits = subreddits or [
            'technology', 'business', 'economics', 'investing', 
            'finance', 'stocks', 'CryptoCurrency', 'startups'
        ]
        self.post_limit = post_limit
        
        # Setup Reddit client using environment variables
        # Note: In a real implementation, you'd need to set these env variables
        try:
            self.reddit = praw.Reddit(
                client_id=os.getenv('REDDIT_CLIENT_ID', 'demo_client_id'),
                client_secret=os.getenv('REDDIT_CLIENT_SECRET', 'demo_client_secret'),
                user_agent="NewsMarketAgent/1.0",
                username=os.getenv('REDDIT_USERNAME', None),  # Optional
                password=os.getenv('REDDIT_PASSWORD', None)   # Optional
            )
            # For demo purposes, read-only mode is fine
            self.reddit.read_only = True
        except Exception as e:
            logger.error(f"Error initializing Reddit client: {e}")
            self.reddit = None
    
    def get_hot_posts(self, subreddit_name: str) -> List[Dict[str, Any]]:
        """Get hot posts from a specific subreddit"""
        if not self.reddit:
            logger.error("Reddit client not initialized")
            return []
        
        try:
            subreddit = self.reddit.subreddit(subreddit_name)
            posts = []
            
            for post in subreddit.hot(limit=self.post_limit):
                # Skip stickied posts
                if post.stickied:
                    continue
                    
                posts.append({
                    'id': post.id,
                    'title': post.title,
                    'url': post.url,
                    'permalink': f"https://www.reddit.com{post.permalink}",
                    'score': post.score,
                    'comments': post.num_comments,
                    'created_utc': post.created_utc,
                    'created_date': datetime.fromtimestamp(post.created_utc).isoformat(),
                    'author': str(post.author),
                    'is_self': post.is_self,
                    'selftext': post.selftext if post.is_self else "",
                    'subreddit': subreddit_name,
                    'source': 'reddit'
                })
                
            return posts
        except Exception as e:
            logger.error(f"Error retrieving posts from r/{subreddit_name}: {e}")
            return []
    
    def get_all_hot_posts(self, filter_keywords: Optional[List[str]] = None) -> List[Dict[str, Any]]:
        """
        Retrieve hot posts from all monitored subreddits
        
        Args:
            filter_keywords: Optional list of keywords to filter posts by
            
        Returns:
            List of post details
        """
        all_posts = []
        
        for subreddit in self.subreddits:
            posts = self.get_hot_posts(subreddit)
            
            # Apply keyword filtering if provided
            if filter_keywords:
                filtered_posts = []
                for post in posts:
                    if any(keyword.lower() in post['title'].lower() for keyword in filter_keywords):
                        filtered_posts.append(post)
                all_posts.extend(filtered_posts)
            else:
                all_posts.extend(posts)
                
        # Sort by score (descending)
        return sorted(all_posts, key=lambda x: x['score'], reverse=True)
    
    def search_posts(self, query: str, subreddits: Optional[List[str]] = None, time_filter: str = 'week') -> List[Dict[str, Any]]:
        """
        Search for posts matching a query
        
        Args:
            query: Search query
            subreddits: List of subreddits to search in (defaults to all monitored subreddits)
            time_filter: Time filter ('hour', 'day', 'week', 'month', 'year', 'all')
            
        Returns:
            List of post details
        """
        if not self.reddit:
            logger.error("Reddit client not initialized")
            return []
            
        search_subreddits = subreddits or self.subreddits
        all_results = []
        
        for subreddit_name in search_subreddits:
            try:
                subreddit = self.reddit.subreddit(subreddit_name)
                search_results = subreddit.search(query, time_filter=time_filter, limit=self.post_limit)
                
                for post in search_results:
                    all_results.append({
                        'id': post.id,
                        'title': post.title,
                        'url': post.url,
                        'permalink': f"https://www.reddit.com{post.permalink}",
                        'score': post.score,
                        'comments': post.num_comments,
                        'created_utc': post.created_utc,
                        'created_date': datetime.fromtimestamp(post.created_utc).isoformat(),
                        'author': str(post.author),
                        'is_self': post.is_self,
                        'selftext': post.selftext if post.is_self else "",
                        'subreddit': subreddit_name,
                        'source': 'reddit'
                    })
            except Exception as e:
                logger.error(f"Error searching in r/{subreddit_name}: {e}")
                
        # Sort by score (descending)
        return sorted(all_results, key=lambda x: x['score'], reverse=True)
