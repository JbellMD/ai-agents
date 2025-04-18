"""
Market Processor - Analyzes market data and correlates with news
"""
import logging
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta

# Local imports
from ..interfaces.market_insights_interface import MarketInsightsInterface
from ..interfaces.company_monitor_interface import CompanyMonitorInterface

logger = logging.getLogger(__name__)

class MarketProcessor:
    """Processes market data and correlates with news"""
    
    def __init__(self):
        """Initialize market processor and its dependencies"""
        self.market_insights = MarketInsightsInterface()
        self.company_monitor = CompanyMonitorInterface()
    
    def get_market_overview(self) -> Dict[str, Any]:
        """
        Get a comprehensive overview of current market conditions
        
        Returns:
            Dictionary with market overview data
        """
        # Get market summary
        market_summary = self.market_insights.get_market_summary()
        
        # Get sector performance
        sector_performance = self.market_insights.get_sector_performance()
        
        # Get economic indicators
        economic_indicators = self.market_insights.get_economic_indicators()
        
        # Compile the overview
        return {
            "summary": market_summary,
            "sector_performance": sector_performance,
            "economic_indicators": economic_indicators,
            "timestamp": datetime.now().isoformat(),
            "source": "market_processor"
        }
    
    def analyze_news_market_impact(self, news_items: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Analyze the potential market impact of news items
        
        Args:
            news_items: List of news items to analyze
            
        Returns:
            News items with added market impact analysis
        """
        # Use market insights to analyze impact
        return self.market_insights.analyze_news_impact(news_items)
    
    def extract_company_mentions(self, news_items: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
        """
        Extract company mentions from news items
        
        Args:
            news_items: List of news items to analyze
            
        Returns:
            Dictionary mapping company tickers to news items
        """
        # Common tech company tickers for demo
        tech_companies = {
            "AAPL": ["Apple", "iPhone", "iPad", "Mac", "Tim Cook"],
            "MSFT": ["Microsoft", "Windows", "Azure", "Office", "Nadella", "Satya"],
            "GOOGL": ["Google", "Alphabet", "Android", "Pixel", "Pichai"],
            "AMZN": ["Amazon", "AWS", "Bezos", "Jassy"],
            "META": ["Meta", "Facebook", "Instagram", "WhatsApp", "Zuckerberg"],
            "TSLA": ["Tesla", "Musk", "Elon"],
            "NVDA": ["Nvidia", "GPU", "Jensen Huang"],
            "NFLX": ["Netflix", "streaming"],
            "IBM": ["IBM", "International Business Machines"],
            "ORCL": ["Oracle", "Ellison"]
        }
        
        # Initialize result
        company_mentions = {ticker: [] for ticker in tech_companies}
        
        # Analyze each news item
        for item in news_items:
            title = item.get('title', '')
            content = item.get('content', '')
            text = title + " " + content
            
            # Check for company mentions
            for ticker, keywords in tech_companies.items():
                for keyword in keywords:
                    if keyword in text:
                        if item not in company_mentions[ticker]:
                            company_mentions[ticker].append(item)
                        break
        
        # Remove companies with no mentions
        return {ticker: mentions for ticker, mentions in company_mentions.items() if mentions}
    
    def get_companies_data(self, tickers: List[str]) -> Dict[str, Dict[str, Any]]:
        """
        Get detailed data for specified companies
        
        Args:
            tickers: List of company tickers to get data for
            
        Returns:
            Dictionary mapping tickers to company data
        """
        result = {}
        
        for ticker in tickers:
            # Get company profile
            profile = self.company_monitor.get_company_profile(ticker)
            
            # Get financial metrics
            financials = self.company_monitor.get_financial_metrics(ticker)
            
            # Get recent news
            news = self.company_monitor.get_company_news(ticker, days=3)
            
            # Compile the data
            result[ticker] = {
                "profile": profile,
                "financials": financials,
                "recent_news": news,
                "source": "company_monitor"
            }
        
        return result
    
    def analyze_top_performers(self, sector: Optional[str] = None) -> Dict[str, Any]:
        """
        Analyze top performing companies/sectors in the market
        
        Args:
            sector: Optional sector to focus on
            
        Returns:
            Dictionary with top performers analysis
        """
        # Get market summary
        market_summary = self.market_insights.get_market_summary()
        
        # Get trending tickers
        trending_tickers = market_summary.get('trending_tickers', [])
        
        # Get sector performance
        all_sectors = self.market_insights.get_sector_performance()
        
        # Filter by sector if specified
        if sector:
            filtered_sectors = [s for s in all_sectors if s['sector'].lower() == sector.lower()]
            sectors = filtered_sectors if filtered_sectors else all_sectors
        else:
            sectors = all_sectors
        
        # Get top sectors
        top_sectors = sorted(sectors, key=lambda x: x['daily_change_percent'], reverse=True)[:3]
        
        # Get data for trending tickers
        ticker_symbols = [ticker['symbol'] for ticker in trending_tickers]
        companies_data = self.get_companies_data(ticker_symbols[:5])  # Get top 5 trending companies
        
        return {
            "top_sectors": top_sectors,
            "trending_companies": companies_data,
            "market_mood": market_summary.get('market_mood', {}),
            "timestamp": datetime.now().isoformat(),
            "source": "market_processor"
        }
    
    def correlate_news_with_market(self, news_items: List[Dict[str, Any]], 
                                  market_overview: Dict[str, Any]) -> Dict[str, Any]:
        """
        Correlate news with market data to identify relationships
        
        Args:
            news_items: List of news items
            market_overview: Market overview data
            
        Returns:
            Dictionary with correlation analysis
        """
        # Analyze impact of news on market
        news_with_impact = self.analyze_news_market_impact(news_items)
        
        # Extract company mentions
        company_mentions = self.extract_company_mentions(news_items)
        
        # Get sector mentions
        sector_mentions = self._extract_sector_mentions(news_items)
        
        # Correlate sectors with performance
        sector_performance = market_overview.get('sector_performance', [])
        sector_correlation = self._correlate_sectors_performance(sector_mentions, sector_performance)
        
        # Get data for mentioned companies (limit to top 5)
        top_mentioned_companies = sorted(company_mentions.items(), key=lambda x: len(x[1]), reverse=True)[:5]
        top_mentioned_tickers = [ticker for ticker, _ in top_mentioned_companies]
        companies_data = self.get_companies_data(top_mentioned_tickers)
        
        return {
            "news_with_impact": news_with_impact,
            "company_mentions": {ticker: len(mentions) for ticker, mentions in company_mentions.items()},
            "sector_mentions": sector_mentions,
            "sector_correlation": sector_correlation,
            "company_data": companies_data,
            "timestamp": datetime.now().isoformat(),
            "source": "market_processor"
        }
    
    def _extract_sector_mentions(self, news_items: List[Dict[str, Any]]) -> Dict[str, int]:
        """Extract sector mentions from news items"""
        # Common market sectors
        sectors = [
            "Technology", "Healthcare", "Financials", "Consumer Discretionary",
            "Industrials", "Communication Services", "Consumer Staples",
            "Energy", "Utilities", "Materials", "Real Estate"
        ]
        
        # Initialize counts
        sector_mentions = {sector: 0 for sector in sectors}
        
        # Count mentions in each news item
        for item in news_items:
            title = item.get('title', '')
            content = item.get('content', '')
            text = title + " " + content
            
            for sector in sectors:
                if sector in text:
                    sector_mentions[sector] += 1
        
        # Return only sectors with mentions
        return {sector: count for sector, count in sector_mentions.items() if count > 0}
    
    def _correlate_sectors_performance(self, sector_mentions: Dict[str, int], 
                                      sector_performance: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Correlate sector mentions with sector performance"""
        # Create lookup for sector performance
        performance_lookup = {s['sector']: s for s in sector_performance}
        
        # Correlate mentions with performance
        correlation = []
        for sector, mentions in sector_mentions.items():
            if sector in performance_lookup:
                correlation.append({
                    "sector": sector,
                    "mentions": mentions,
                    "daily_change_percent": performance_lookup[sector]['daily_change_percent'],
                    "correlation_type": "positive" if mentions > 3 and performance_lookup[sector]['daily_change_percent'] > 0 else 
                                        "negative" if mentions > 3 and performance_lookup[sector]['daily_change_percent'] < 0 else
                                        "neutral"
                })
        
        return correlation
