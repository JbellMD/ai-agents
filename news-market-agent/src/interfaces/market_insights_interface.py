"""
Market Insights Interface - Connects to Market Insights data source for market trend analysis
"""
import requests
import logging
import json
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

class MarketInsightsInterface:
    """Interface for retrieving market data and insights"""
    
    # For demo purposes, we'll mock the API endpoints
    BASE_URL = "https://api.marketinsights.io/v1"
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the Market Insights interface
        
        Args:
            api_key: Optional API key (defaults to env variable)
        """
        self.api_key = api_key or os.getenv('MARKET_INSIGHTS_API_KEY', 'demo_api_key')
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
    
    def get_market_summary(self) -> Dict[str, Any]:
        """
        Get summary of current market conditions
        
        Returns:
            Dictionary with market summary data
        """
        try:
            # Simulated API call
            # response = requests.get(
            #     f"{self.BASE_URL}/market/summary",
            #     headers=self.headers
            # )
            # response.raise_for_status()
            # return response.json()
            
            # Mock data for demo
            return self._get_mock_market_summary()
        except Exception as e:
            logger.error(f"Error retrieving market summary: {e}")
            return {}
    
    def get_stock_data(self, symbols: List[str], days: int = 7) -> Dict[str, List[Dict[str, Any]]]:
        """
        Get historical stock data for specified symbols
        
        Args:
            symbols: List of stock symbols to retrieve data for
            days: Number of days of historical data to retrieve
            
        Returns:
            Dictionary mapping symbols to their historical data
        """
        try:
            # Simulated API call
            # response = requests.get(
            #     f"{self.BASE_URL}/stocks/historical",
            #     params={"symbols": ",".join(symbols), "days": days},
            #     headers=self.headers
            # )
            # response.raise_for_status()
            # return response.json()
            
            # Mock data for demo
            return self._get_mock_stock_data(symbols, days)
        except Exception as e:
            logger.error(f"Error retrieving stock data for {symbols}: {e}")
            return {symbol: [] for symbol in symbols}
    
    def get_sector_performance(self) -> List[Dict[str, Any]]:
        """
        Get performance data for market sectors
        
        Returns:
            List of sector performance data
        """
        try:
            # Simulated API call
            # response = requests.get(
            #     f"{self.BASE_URL}/market/sectors",
            #     headers=self.headers
            # )
            # response.raise_for_status()
            # return response.json()
            
            # Mock data for demo
            return self._get_mock_sector_performance()
        except Exception as e:
            logger.error(f"Error retrieving sector performance: {e}")
            return []
    
    def get_economic_indicators(self) -> Dict[str, Any]:
        """
        Get current economic indicators
        
        Returns:
            Dictionary with economic indicator data
        """
        try:
            # Simulated API call
            # response = requests.get(
            #     f"{self.BASE_URL}/economy/indicators",
            #     headers=self.headers
            # )
            # response.raise_for_status()
            # return response.json()
            
            # Mock data for demo
            return self._get_mock_economic_indicators()
        except Exception as e:
            logger.error(f"Error retrieving economic indicators: {e}")
            return {}
    
    def analyze_news_impact(self, news_items: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Analyze the potential market impact of news items
        
        Args:
            news_items: List of news items to analyze
            
        Returns:
            List of news items with added market impact analysis
        """
        try:
            # In a real implementation, this would send the news items to the API
            # and get back impact analysis
            # response = requests.post(
            #     f"{self.BASE_URL}/analysis/news-impact",
            #     json={"news_items": news_items},
            #     headers=self.headers
            # )
            # response.raise_for_status()
            # return response.json()
            
            # Mock data for demo
            return self._get_mock_news_impact(news_items)
        except Exception as e:
            logger.error(f"Error analyzing news impact: {e}")
            return news_items  # Return original items without analysis
    
    def _get_mock_market_summary(self) -> Dict[str, Any]:
        """Generate mock market summary data for demo purposes"""
        return {
            "timestamp": datetime.now().isoformat(),
            "indices": {
                "S&P 500": {
                    "value": 5432.10,
                    "change": 12.43,
                    "change_percent": 0.23,
                    "direction": "up"
                },
                "Dow Jones": {
                    "value": 38765.21,
                    "change": -45.67,
                    "change_percent": -0.12,
                    "direction": "down"
                },
                "NASDAQ": {
                    "value": 18234.56,
                    "change": 78.90,
                    "change_percent": 0.43,
                    "direction": "up"
                }
            },
            "market_mood": {
                "sentiment": "bullish",
                "fear_greed_index": 65,  # 0-100, higher means more greedy/optimistic
                "volatility_index": 16.8
            },
            "trending_tickers": [
                {"symbol": "AAPL", "change_percent": 1.2},
                {"symbol": "MSFT", "change_percent": 0.8},
                {"symbol": "GOOGL", "change_percent": -0.5},
                {"symbol": "AMZN", "change_percent": 2.1},
                {"symbol": "TSLA", "change_percent": 3.7}
            ],
            "trading_volume": {
                "value": 8.2,  # in billions
                "change_percent": 0.15
            },
            "source": "market_insights"
        }
    
    def _get_mock_stock_data(self, symbols: List[str], days: int) -> Dict[str, List[Dict[str, Any]]]:
        """Generate mock stock data for demo purposes"""
        result = {}
        base_date = datetime.now().date()
        
        for symbol in symbols:
            # Generate somewhat realistic price data based on the symbol
            # This ensures the mock data is consistent for the same symbol
            symbol_seed = sum(ord(c) for c in symbol)
            base_price = 100 + (symbol_seed % 900)  # Base price between 100 and 1000
            volatility = (symbol_seed % 10) / 100  # Volatility between 0.01 and 0.09
            
            daily_data = []
            current_price = base_price
            
            for i in range(days):
                date = base_date - timedelta(days=(days-i-1))
                # Generate price movement based on volatility and some pseudo-randomness
                change_percent = (((symbol_seed + i) % 10) - 5) * volatility
                current_price = current_price * (1 + change_percent)
                
                daily_data.append({
                    "date": date.isoformat(),
                    "open": round(current_price * 0.995, 2),
                    "close": round(current_price, 2),
                    "high": round(current_price * 1.01, 2),
                    "low": round(current_price * 0.99, 2),
                    "volume": int(1000000 + (symbol_seed + i) % 9000000)
                })
            
            result[symbol] = daily_data
        
        return result
    
    def _get_mock_sector_performance(self) -> List[Dict[str, Any]]:
        """Generate mock sector performance data for demo purposes"""
        sectors = [
            "Technology",
            "Healthcare",
            "Financials",
            "Consumer Discretionary",
            "Industrials",
            "Communication Services",
            "Consumer Staples",
            "Energy",
            "Utilities",
            "Materials",
            "Real Estate"
        ]
        
        # Static seed to ensure consistent but varied returns
        seed = 42
        
        result = []
        for i, sector in enumerate(sectors):
            # Generate somewhat realistic returns
            daily_change = ((seed + i) % 21 - 10) / 10  # Between -1.0% and +1.0%
            weekly_change = daily_change * 3 + ((seed + i*2) % 10 - 5) / 10  # More varied
            monthly_change = weekly_change * 2 + ((seed + i*3) % 30 - 15) / 10  # Even more varied
            
            result.append({
                "sector": sector,
                "daily_change_percent": round(daily_change, 2),
                "weekly_change_percent": round(weekly_change, 2),
                "monthly_change_percent": round(monthly_change, 2),
                "market_cap_billions": round(500 + (seed + i*4) % 2000, 1),
                "pe_ratio": round(15 + (seed + i*5) % 20, 1)
            })
        
        # Sort by daily performance
        return sorted(result, key=lambda x: x["daily_change_percent"], reverse=True)
    
    def _get_mock_economic_indicators(self) -> Dict[str, Any]:
        """Generate mock economic indicator data for demo purposes"""
        return {
            "inflation_rate": {
                "value": 3.2,
                "previous": 3.4,
                "trend": "decreasing"
            },
            "unemployment_rate": {
                "value": 4.1,
                "previous": 4.2,
                "trend": "decreasing"
            },
            "gdp_growth": {
                "value": 2.3,
                "previous": 2.1,
                "trend": "increasing"
            },
            "interest_rates": {
                "fed_funds_rate": {
                    "value": 4.75,
                    "previous": 5.0,
                    "trend": "decreasing"
                },
                "ten_year_treasury": {
                    "value": 3.85,
                    "previous": 3.92,
                    "trend": "decreasing"
                }
            },
            "housing_market": {
                "new_home_sales": {
                    "value": 723000,  # Annualized
                    "change_percent": 2.8
                },
                "median_home_price": {
                    "value": 432100,
                    "change_percent": 4.2
                }
            },
            "retail_sales": {
                "value": 706.2,  # Billions
                "change_percent": 0.6
            },
            "source": "market_insights",
            "last_updated": datetime.now().isoformat()
        }
    
    def _get_mock_news_impact(self, news_items: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Generate mock news impact analysis for demo purposes"""
        result = []
        
        impact_types = ["high", "medium", "low", "negligible"]
        market_sectors = [
            "Technology", "Healthcare", "Financials", "Consumer", 
            "Energy", "Industrials", "Communication", "Materials"
        ]
        directions = ["positive", "negative", "mixed", "neutral"]
        
        for i, item in enumerate(news_items):
            # Generate somewhat consistent impact analysis based on the news title
            title = item.get('title', '')
            title_seed = sum(ord(c) for c in title) if title else i
            
            # Determine impact level
            impact_index = title_seed % len(impact_types)
            impact_level = impact_types[impact_index]
            
            # Determine affected sectors
            num_sectors = 1 + (title_seed % 3)  # 1-3 sectors
            sector_indices = [(title_seed + j) % len(market_sectors) for j in range(num_sectors)]
            affected_sectors = [market_sectors[idx] for idx in sector_indices]
            
            # Determine impact direction
            direction_index = (title_seed // 2) % len(directions)
            direction = directions[direction_index]
            
            # Add impact analysis to the news item
            item_with_analysis = item.copy()
            item_with_analysis.update({
                "market_impact": {
                    "impact_level": impact_level,
                    "direction": direction,
                    "affected_sectors": affected_sectors,
                    "confidence_score": round(0.5 + (title_seed % 50) / 100, 2),  # 0.5-0.99
                    "timeframe": "short-term" if title_seed % 3 == 0 else "long-term"
                }
            })
            
            result.append(item_with_analysis)
        
        return result
