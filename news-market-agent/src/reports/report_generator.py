"""
Report Generator - Generates structured reports from processed data
"""
import logging
from typing import List, Dict, Any
import json
from datetime import datetime
import os
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from collections import Counter

logger = logging.getLogger(__name__)

class ReportGenerator:
    """Generates reports from processed news and market data"""
    
    def __init__(self, output_dir: str = 'reports'):
        """
        Initialize the report generator
        
        Args:
            output_dir: Directory to save generated reports
        """
        self.output_dir = output_dir
        
        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)
    
    def generate_daily_digest(self, news_data: List[Dict[str, Any]], 
                             market_data: Dict[str, Any],
                             correlation_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate a daily digest report
        
        Args:
            news_data: Processed news data
            market_data: Processed market data
            correlation_data: Data correlating news and market
            
        Returns:
            Report data
        """
        # Generate timestamp for the report
        timestamp = datetime.now().isoformat()
        report_id = f"daily_digest_{datetime.now().strftime('%Y%m%d')}"
        
        # Extract key data points
        market_summary = market_data.get('summary', {}).get('indices', {})
        sector_performance = market_data.get('sector_performance', [])
        news_with_impact = correlation_data.get('news_with_impact', [])
        company_mentions = correlation_data.get('company_mentions', {})
        
        # Generate insights
        market_insights = self._generate_market_insights(market_data)
        news_insights = self._generate_news_insights(news_data)
        correlation_insights = self._generate_correlation_insights(correlation_data)
        
        # Compile the report
        report = {
            "report_id": report_id,
            "report_type": "daily_digest",
            "timestamp": timestamp,
            "market_summary": {
                "indices": market_summary,
                "top_sectors": sector_performance[:3] if sector_performance else []
            },
            "news_summary": {
                "top_stories": news_data[:5] if news_data else [],
                "trending_topics": self._extract_trending_topics(news_data),
                "sentiment_overview": self._analyze_overall_sentiment(news_data)
            },
            "key_companies": {
                "most_mentioned": self._get_top_items(company_mentions, 5),
                "top_performers": self._extract_top_performers(market_data)
            },
            "insights": {
                "market_insights": market_insights,
                "news_insights": news_insights,
                "correlation_insights": correlation_insights
            },
            "source": "report_generator"
        }
        
        # Generate visualizations
        self._generate_visualizations(report)
        
        # Save the report
        self._save_report(report, f"{report_id}.json")
        
        return report
    
    def generate_company_report(self, ticker: str, company_data: Dict[str, Any],
                               related_news: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Generate a report for a specific company
        
        Args:
            ticker: Company ticker symbol
            company_data: Processed company data
            related_news: News related to the company
            
        Returns:
            Report data
        """
        # Generate timestamp for the report
        timestamp = datetime.now().isoformat()
        report_id = f"company_report_{ticker}_{datetime.now().strftime('%Y%m%d')}"
        
        # Extract company profile
        profile = company_data.get('profile', {})
        financials = company_data.get('financials', {})
        
        # Generate insights
        company_insights = self._generate_company_insights(ticker, company_data, related_news)
        
        # Compile the report
        report = {
            "report_id": report_id,
            "report_type": "company_report",
            "ticker": ticker,
            "company_name": profile.get('name', ticker),
            "timestamp": timestamp,
            "profile_summary": {
                "sector": profile.get('sector', 'Unknown'),
                "industry": profile.get('industry', 'Unknown'),
                "description": profile.get('description', ''),
                "market_cap": profile.get('market_cap', {})
            },
            "financial_summary": {
                "revenue": financials.get('revenue', {}),
                "profitability": financials.get('profitability', {}),
                "ratios": financials.get('financial_ratios', {})
            },
            "news_summary": {
                "recent_news": related_news[:3] if related_news else [],
                "news_sentiment": self._analyze_overall_sentiment(related_news)
            },
            "insights": company_insights,
            "source": "report_generator"
        }
        
        # Save the report
        self._save_report(report, f"{report_id}.json")
        
        return report
    
    def generate_sector_report(self, sector: str, sector_data: List[Dict[str, Any]], 
                              related_news: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Generate a report for a specific market sector
        
        Args:
            sector: Sector name
            sector_data: Processed sector data
            related_news: News related to the sector
            
        Returns:
            Report data
        """
        # Generate timestamp for the report
        timestamp = datetime.now().isoformat()
        report_id = f"sector_report_{sector.lower().replace(' ', '_')}_{datetime.now().strftime('%Y%m%d')}"
        
        # Generate insights
        sector_insights = self._generate_sector_insights(sector, sector_data, related_news)
        
        # Compile the report
        report = {
            "report_id": report_id,
            "report_type": "sector_report",
            "sector": sector,
            "timestamp": timestamp,
            "performance_summary": {
                "daily_change": next((s.get('daily_change_percent', 0) for s in sector_data if s.get('sector') == sector), 0),
                "weekly_change": next((s.get('weekly_change_percent', 0) for s in sector_data if s.get('sector') == sector), 0),
                "monthly_change": next((s.get('monthly_change_percent', 0) for s in sector_data if s.get('sector') == sector), 0)
            },
            "news_summary": {
                "recent_news": related_news[:3] if related_news else [],
                "news_sentiment": self._analyze_overall_sentiment(related_news)
            },
            "insights": sector_insights,
            "source": "report_generator"
        }
        
        # Save the report
        self._save_report(report, f"{report_id}.json")
        
        return report
    
    def _generate_market_insights(self, market_data: Dict[str, Any]) -> List[str]:
        """Generate insights from market data"""
        insights = []
        
        # Extract key data points
        market_summary = market_data.get('summary', {})
        indices = market_summary.get('indices', {})
        market_mood = market_summary.get('market_mood', {})
        sector_performance = market_data.get('sector_performance', [])
        economic_indicators = market_data.get('economic_indicators', {})
        
        # Generate insights based on market indices
        if indices:
            for index_name, index_data in indices.items():
                direction = index_data.get('direction', '')
                change_percent = index_data.get('change_percent', 0)
                
                if direction == 'up' and change_percent > 1:
                    insights.append(f"{index_name} showed strong performance with a {change_percent}% increase.")
                elif direction == 'down' and change_percent < -1:
                    insights.append(f"{index_name} declined significantly with a {abs(change_percent)}% decrease.")
        
        # Generate insights based on market mood
        if market_mood:
            sentiment = market_mood.get('sentiment', '')
            fear_greed = market_mood.get('fear_greed_index', 0)
            volatility = market_mood.get('volatility_index', 0)
            
            if sentiment:
                insights.append(f"Market sentiment is currently {sentiment}.")
            
            if fear_greed > 75:
                insights.append("The fear & greed index indicates extreme greed in the market.")
            elif fear_greed < 25:
                insights.append("The fear & greed index indicates extreme fear in the market.")
            
            if volatility > 30:
                insights.append("Market volatility is elevated, suggesting uncertainty.")
            elif volatility < 15:
                insights.append("Market volatility is low, suggesting stability.")
        
        # Generate insights based on sector performance
        if sector_performance:
            top_sector = sector_performance[0] if sector_performance else {}
            bottom_sector = sector_performance[-1] if sector_performance else {}
            
            if top_sector:
                insights.append(f"The {top_sector.get('sector', '')} sector is leading with a {top_sector.get('daily_change_percent', 0)}% daily change.")
            
            if bottom_sector:
                insights.append(f"The {bottom_sector.get('sector', '')} sector is underperforming with a {bottom_sector.get('daily_change_percent', 0)}% daily change.")
        
        # Generate insights based on economic indicators
        if economic_indicators:
            inflation = economic_indicators.get('inflation_rate', {})
            unemployment = economic_indicators.get('unemployment_rate', {})
            gdp_growth = economic_indicators.get('gdp_growth', {})
            
            if inflation and 'trend' in inflation:
                insights.append(f"Inflation rate is {inflation.get('trend', '')} at {inflation.get('value', 0)}%.")
            
            if unemployment and 'trend' in unemployment:
                insights.append(f"Unemployment rate is {unemployment.get('trend', '')} at {unemployment.get('value', 0)}%.")
            
            if gdp_growth and 'trend' in gdp_growth:
                insights.append(f"GDP growth is {gdp_growth.get('trend', '')} at {gdp_growth.get('value', 0)}%.")
        
        return insights
    
    def _generate_news_insights(self, news_data: List[Dict[str, Any]]) -> List[str]:
        """Generate insights from news data"""
        insights = []
        
        # Count sentiment distribution
        sentiment_counts = {"positive": 0, "negative": 0, "neutral": 0}
        for item in news_data:
            sentiment = item.get('sentiment', {}).get('label', 'neutral')
            sentiment_counts[sentiment] += 1
        
        # Generate insight based on overall sentiment
        total_items = len(news_data)
        if total_items > 0:
            positive_ratio = sentiment_counts["positive"] / total_items
            negative_ratio = sentiment_counts["negative"] / total_items
            
            if positive_ratio > 0.6:
                insights.append(f"News sentiment is predominantly positive ({int(positive_ratio*100)}% of articles).")
            elif negative_ratio > 0.6:
                insights.append(f"News sentiment is predominantly negative ({int(negative_ratio*100)}% of articles).")
            else:
                insights.append("News sentiment is mixed with no clear direction.")
        
        # Extract trending topics
        trending_topics = self._extract_trending_topics(news_data)
        if trending_topics:
            top_topics = [topic for topic, _ in trending_topics[:3]]
            insights.append(f"Trending topics in the news: {', '.join(top_topics)}.")
        
        # Look for recurring companies
        company_mentions = {}
        for item in news_data:
            entities = item.get('entities', [])
            for entity in entities:
                if entity.get('type') == 'organization':
                    name = entity.get('name', '')
                    company_mentions[name] = company_mentions.get(name, 0) + 1
        
        if company_mentions:
            top_companies = sorted(company_mentions.items(), key=lambda x: x[1], reverse=True)[:3]
            insights.append(f"Most mentioned companies: {', '.join(name for name, _ in top_companies)}.")
        
        return insights
    
    def _generate_correlation_insights(self, correlation_data: Dict[str, Any]) -> List[str]:
        """Generate insights from correlation data"""
        insights = []
        
        # Extract key data
        news_with_impact = correlation_data.get('news_with_impact', [])
        company_mentions = correlation_data.get('company_mentions', {})
        sector_correlation = correlation_data.get('sector_correlation', [])
        
        # Find high-impact news
        high_impact_news = [item for item in news_with_impact 
                           if item.get('market_impact', {}).get('impact_level') == 'high']
        
        if high_impact_news:
            insights.append(f"Identified {len(high_impact_news)} high-impact news items that could significantly affect the market.")
            
            # Get the top high-impact news item
            top_news = high_impact_news[0] if high_impact_news else None
            if top_news:
                title = top_news.get('title', '')
                direction = top_news.get('market_impact', {}).get('direction', '')
                affected_sectors = top_news.get('market_impact', {}).get('affected_sectors', [])
                
                if title and direction and affected_sectors:
                    sectors_str = ', '.join(affected_sectors[:2])
                    if len(affected_sectors) > 2:
                        sectors_str += f" and {len(affected_sectors) - 2} other sectors"
                    
                    insights.append(f"Top story '{title}' could have a {direction} impact on {sectors_str}.")
        
        # Analyze company mentions correlation
        if company_mentions:
            top_mentioned = self._get_top_items(company_mentions, 1)
            if top_mentioned:
                company, mentions = top_mentioned[0]
                insights.append(f"{company} is receiving significant attention with {mentions} mentions in recent news.")
        
        # Analyze sector correlation
        positive_correlations = [item for item in sector_correlation if item.get('correlation_type') == 'positive']
        negative_correlations = [item for item in sector_correlation if item.get('correlation_type') == 'negative']
        
        if positive_correlations:
            sectors = [item.get('sector') for item in positive_correlations[:2]]
            sectors_str = ', '.join(sectors)
            insights.append(f"Positive correlation between news mentions and performance in the {sectors_str} sector(s).")
        
        if negative_correlations:
            sectors = [item.get('sector') for item in negative_correlations[:2]]
            sectors_str = ', '.join(sectors)
            insights.append(f"Negative correlation between news mentions and performance in the {sectors_str} sector(s).")
        
        return insights
    
    def _generate_company_insights(self, ticker: str, company_data: Dict[str, Any], 
                                  related_news: List[Dict[str, Any]]) -> List[str]:
        """Generate insights for a specific company"""
        insights = []
        
        # Extract key data
        profile = company_data.get('profile', {})
        financials = company_data.get('financials', {})
        recent_news = company_data.get('recent_news', [])
        
        # Basic company info insight
        company_name = profile.get('name', ticker)
        sector = profile.get('sector', 'Unknown')
        industry = profile.get('industry', 'Unknown')
        
        insights.append(f"{company_name} ({ticker}) operates in the {industry} industry within the {sector} sector.")
        
        # Financial insights
        if financials:
            revenue = financials.get('revenue', {})
            profitability = financials.get('profitability', {})
            ratios = financials.get('financial_ratios', {})
            
            if revenue and 'annual_revenue_billions' in revenue:
                annual_revenue = revenue.get('annual_revenue_billions', 0)
                revenue_growth = revenue.get('revenue_growth_yoy', 0)
                
                insights.append(f"Annual revenue of ${annual_revenue} billion with {revenue_growth}% year-over-year growth.")
            
            if profitability and 'profit_margin' in profitability:
                profit_margin = profitability.get('profit_margin', 0)
                
                if profit_margin > 20:
                    insights.append(f"Strong profit margin of {profit_margin}%, well above industry averages.")
                elif profit_margin < 5:
                    insights.append(f"Slim profit margin of {profit_margin}%, below typical industry levels.")
                else:
                    insights.append(f"Moderate profit margin of {profit_margin}%.")
            
            if ratios and 'pe_ratio' in ratios:
                pe_ratio = ratios.get('pe_ratio', 0)
                
                if pe_ratio > 30:
                    insights.append(f"High P/E ratio of {pe_ratio}, suggesting high growth expectations.")
                elif pe_ratio < 10:
                    insights.append(f"Low P/E ratio of {pe_ratio}, potentially indicating undervaluation.")
        
        # News sentiment insights
        if related_news:
            sentiment = self._analyze_overall_sentiment(related_news)
            
            if sentiment.get('label') == 'positive':
                insights.append(f"Recent news sentiment is positive with a score of {sentiment.get('score', 0)}.")
            elif sentiment.get('label') == 'negative':
                insights.append(f"Recent news sentiment is negative with a score of {sentiment.get('score', 0)}.")
            
            # Extract key news themes
            news_titles = [item.get('title', '') for item in related_news]
            if news_titles:
                insights.append(f"Recent news focuses on: {news_titles[0]}")
        
        return insights
    
    def _generate_sector_insights(self, sector: str, sector_data: List[Dict[str, Any]], 
                                related_news: List[Dict[str, Any]]) -> List[str]:
        """Generate insights for a specific sector"""
        insights = []
        
        # Find the sector in the data
        sector_info = next((s for s in sector_data if s.get('sector') == sector), {})
        
        if sector_info:
            daily_change = sector_info.get('daily_change_percent', 0)
            weekly_change = sector_info.get('weekly_change_percent', 0)
            monthly_change = sector_info.get('monthly_change_percent', 0)
            
            # Performance insights
            if daily_change > 0:
                insights.append(f"The {sector} sector is up {daily_change}% today.")
            else:
                insights.append(f"The {sector} sector is down {abs(daily_change)}% today.")
            
            # Trend insights
            if monthly_change > weekly_change > daily_change > 0:
                insights.append(f"The {sector} sector is showing a decelerating positive trend.")
            elif monthly_change < weekly_change < daily_change and daily_change > 0:
                insights.append(f"The {sector} sector is showing an accelerating positive trend.")
            elif monthly_change > weekly_change > daily_change and daily_change < 0:
                insights.append(f"The {sector} sector is showing an accelerating negative trend.")
            elif monthly_change < weekly_change < daily_change < 0:
                insights.append(f"The {sector} sector is showing a decelerating negative trend.")
            elif monthly_change < 0 < daily_change:
                insights.append(f"The {sector} sector may be recovering from a bearish trend.")
            elif monthly_change > 0 > daily_change:
                insights.append(f"The {sector} sector may be entering a bearish trend.")
        
        # News sentiment insights
        if related_news:
            sentiment = self._analyze_overall_sentiment(related_news)
            
            if sentiment.get('label') == 'positive' and len(related_news) > 3:
                insights.append(f"High volume of positive news coverage for the {sector} sector.")
            elif sentiment.get('label') == 'negative' and len(related_news) > 3:
                insights.append(f"High volume of negative news coverage for the {sector} sector.")
            elif len(related_news) > 5:
                insights.append(f"The {sector} sector is receiving significant media attention.")
        else:
            insights.append(f"Limited recent news coverage for the {sector} sector.")
        
        return insights
    
    def _extract_trending_topics(self, news_data: List[Dict[str, Any]]) -> List[tuple]:
        """Extract trending topics from news data"""
        # Extract keywords and entities
        keywords = []
        
        for item in news_data:
            # Extract from title and content
            title = item.get('title', '')
            content = item.get('content', '')
            
            # Simple keyword extraction by splitting and filtering
            title_words = title.lower().split()
            title_words = [word for word in title_words if len(word) > 3]
            
            keywords.extend(title_words)
            
            # Extract entities if available
            entities = item.get('entities', [])
            for entity in entities:
                if entity.get('type') in ['product', 'technology', 'topic']:
                    keywords.append(entity.get('name', '').lower())
        
        # Count occurrences
        keyword_counts = Counter(keywords)
        
        # Filter out common stop words
        stop_words = ['this', 'that', 'with', 'from', 'have', 'has', 'had', 'are', 'were', 'what', 'when', 'while']
        for word in stop_words:
            if word in keyword_counts:
                del keyword_counts[word]
        
        # Return top keywords
        return keyword_counts.most_common(10)
    
    def _analyze_overall_sentiment(self, news_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze overall sentiment of news data"""
        if not news_data:
            return {"label": "neutral", "score": 0, "counts": {"positive": 0, "negative": 0, "neutral": 0}}
        
        # Count sentiment labels
        sentiment_counts = {"positive": 0, "negative": 0, "neutral": 0}
        compound_scores = []
        
        for item in news_data:
            sentiment = item.get('sentiment', {})
            label = sentiment.get('label', 'neutral')
            sentiment_counts[label] += 1
            
            # Collect compound scores if available
            if 'compound' in sentiment:
                compound_scores.append(sentiment['compound'])
            elif 'score' in sentiment:
                compound_scores.append(sentiment['score'])
        
        # Calculate average compound score
        avg_score = sum(compound_scores) / len(compound_scores) if compound_scores else 0
        
        # Determine overall sentiment
        total = sum(sentiment_counts.values())
        if total == 0:
            overall_label = "neutral"
        else:
            pos_ratio = sentiment_counts["positive"] / total
            neg_ratio = sentiment_counts["negative"] / total
            
            if pos_ratio > 0.6:
                overall_label = "positive"
            elif neg_ratio > 0.6:
                overall_label = "negative"
            else:
                overall_label = "neutral"
        
        return {
            "label": overall_label,
            "score": round(avg_score, 2),
            "counts": sentiment_counts
        }
    
    def _extract_top_performers(self, market_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Extract top performing companies from market data"""
        # Get trending tickers
        trending_tickers = market_data.get('summary', {}).get('trending_tickers', [])
        
        # Filter for positive performers
        positive_performers = [ticker for ticker in trending_tickers if ticker.get('change_percent', 0) > 0]
        
        # Sort by performance
        return sorted(positive_performers, key=lambda x: x.get('change_percent', 0), reverse=True)[:5]
    
    def _get_top_items(self, items_dict: Dict[str, Any], count: int) -> List[tuple]:
        """Get top items from a dictionary by value"""
        return sorted(items_dict.items(), key=lambda x: x[1], reverse=True)[:count]
    
    def _generate_visualizations(self, report: Dict[str, Any]) -> None:
        """Generate visualizations for the report"""
        # This would generate charts and graphs for the report
        # For demonstration purposes, we're just logging this
        logger.info(f"Generating visualizations for report {report.get('report_id')}")
        
        # In a real implementation, this would create visualizations using matplotlib or similar
        # For example:
        # plt.figure(figsize=(10, 6))
        # # Plot data
        # plt.savefig(f"{self.output_dir}/{report.get('report_id')}_chart.png")
    
    def _save_report(self, report: Dict[str, Any], filename: str) -> None:
        """Save the report to disk"""
        try:
            filepath = os.path.join(self.output_dir, filename)
            with open(filepath, 'w') as f:
                json.dump(report, f, indent=2)
            logger.info(f"Report saved to {filepath}")
        except Exception as e:
            logger.error(f"Error saving report: {e}")
