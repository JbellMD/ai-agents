"""
News & Market Analysis Agent - Main Module

This agent integrates data from multiple sources (HackerNews, Reddit, Firecrawl, 
Market Insights, Company Monitor) to provide comprehensive analysis of
news and market trends with actionable insights.
"""
import logging
import argparse
import os
import json
import schedule
import time
from datetime import datetime
from typing import List, Dict, Any, Optional
from dotenv import load_dotenv

# Local imports
from interfaces.hackernews_interface import HackerNewsInterface
from interfaces.reddit_interface import RedditInterface
from interfaces.firecrawl_interface import FirecrawlInterface
from interfaces.market_insights_interface import MarketInsightsInterface
from interfaces.company_monitor_interface import CompanyMonitorInterface
from processors.news_processor import NewsProcessor
from processors.market_processor import MarketProcessor
from reports.report_generator import ReportGenerator

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("agent.log"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

class NewsMarketAgent:
    """
    News & Market Analysis Agent
    
    This agent integrates news and market data to generate actionable insights.
    """
    
    def __init__(self, output_dir: str = 'reports'):
        """
        Initialize the agent and its components
        
        Args:
            output_dir: Directory to save generated reports
        """
        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)
        
        # Initialize processors
        self.news_processor = NewsProcessor()
        self.market_processor = MarketProcessor()
        
        # Initialize report generator
        self.report_generator = ReportGenerator(output_dir=output_dir)
        
        logger.info("News & Market Analysis Agent initialized")
    
    def generate_daily_digest(self, topics: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        Generate a daily digest of news and market insights
        
        Args:
            topics: Optional list of topics to filter news by
            
        Returns:
            Generated report data
        """
        logger.info("Generating daily digest")
        
        # Step 1: Gather and process news data
        logger.info("Gathering news data")
        news_data = self.news_processor.get_aggregated_news(topics=topics)
        
        # Step 2: Enrich news with additional content
        logger.info("Enriching news data")
        enriched_news = self.news_processor.enrich_news_with_firecrawl(news_data)
        
        # Step 3: Gather market data
        logger.info("Gathering market data")
        market_data = self.market_processor.get_market_overview()
        
        # Step 4: Correlate news with market data
        logger.info("Correlating news with market data")
        correlation_data = self.market_processor.correlate_news_with_market(enriched_news, market_data)
        
        # Step 5: Generate daily digest report
        logger.info("Generating report")
        report = self.report_generator.generate_daily_digest(
            news_data=enriched_news,
            market_data=market_data,
            correlation_data=correlation_data
        )
        
        logger.info(f"Daily digest completed: {report.get('report_id')}")
        return report
    
    def generate_company_analysis(self, ticker: str) -> Dict[str, Any]:
        """
        Generate an analysis report for a specific company
        
        Args:
            ticker: Company stock ticker symbol
            
        Returns:
            Generated report data
        """
        logger.info(f"Generating company analysis for {ticker}")
        
        # Step 1: Gather company data
        company_data = self.market_processor.get_companies_data([ticker]).get(ticker, {})
        
        # Step 2: Gather and enrich news data
        all_news = self.news_processor.get_aggregated_news()
        enriched_news = self.news_processor.enrich_news_with_firecrawl(all_news)
        
        # Step 3: Extract company mentions from news
        company_mentions = self.market_processor.extract_company_mentions(enriched_news)
        related_news = company_mentions.get(ticker, [])
        
        # Step 4: Generate company report
        report = self.report_generator.generate_company_report(
            ticker=ticker,
            company_data=company_data,
            related_news=related_news
        )
        
        logger.info(f"Company analysis completed: {report.get('report_id')}")
        return report
    
    def generate_sector_analysis(self, sector: str) -> Dict[str, Any]:
        """
        Generate an analysis report for a specific market sector
        
        Args:
            sector: Market sector name
            
        Returns:
            Generated report data
        """
        logger.info(f"Generating sector analysis for {sector}")
        
        # Step 1: Gather market data
        market_data = self.market_processor.get_market_overview()
        sector_data = market_data.get('sector_performance', [])
        
        # Step 2: Gather and enrich news data
        all_news = self.news_processor.get_aggregated_news()
        enriched_news = self.news_processor.enrich_news_with_firecrawl(all_news)
        
        # Step 3: Extract news related to the sector
        # This is a simple approach - in a real implementation, we'd use NLP for better extraction
        related_news = []
        for item in enriched_news:
            title = item.get('title', '').lower()
            content = item.get('content', '').lower()
            text = title + " " + content
            
            if sector.lower() in text:
                related_news.append(item)
        
        # Step 4: Generate sector report
        report = self.report_generator.generate_sector_report(
            sector=sector,
            sector_data=sector_data,
            related_news=related_news
        )
        
        logger.info(f"Sector analysis completed: {report.get('report_id')}")
        return report
    
    def schedule_daily_digest(self, hour: int = 8, minute: int = 0) -> None:
        """
        Schedule daily digest to run at a specific time
        
        Args:
            hour: Hour to run (24-hour format)
            minute: Minute to run
        """
        schedule.every().day.at(f"{hour:02d}:{minute:02d}").do(self.generate_daily_digest)
        logger.info(f"Scheduled daily digest to run at {hour:02d}:{minute:02d}")
        
        # Keep the script running to execute scheduled tasks
        while True:
            schedule.run_pending()
            time.sleep(60)

def parse_args():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(description="News & Market Analysis Agent")
    
    # Create subparsers for different commands
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")
    
    # Daily digest command
    daily_parser = subparsers.add_parser("daily", help="Generate a daily digest")
    daily_parser.add_argument("--topics", nargs="+", help="Topics to filter news by")
    daily_parser.add_argument("--output", default="reports", help="Output directory for reports")
    
    # Company analysis command
    company_parser = subparsers.add_parser("company", help="Generate a company analysis")
    company_parser.add_argument("ticker", help="Company stock ticker symbol")
    company_parser.add_argument("--output", default="reports", help="Output directory for reports")
    
    # Sector analysis command
    sector_parser = subparsers.add_parser("sector", help="Generate a sector analysis")
    sector_parser.add_argument("sector", help="Market sector name")
    sector_parser.add_argument("--output", default="reports", help="Output directory for reports")
    
    # Schedule command
    schedule_parser = subparsers.add_parser("schedule", help="Schedule daily digest")
    schedule_parser.add_argument("--hour", type=int, default=8, help="Hour to run (24-hour format)")
    schedule_parser.add_argument("--minute", type=int, default=0, help="Minute to run")
    schedule_parser.add_argument("--output", default="reports", help="Output directory for reports")
    
    return parser.parse_args()

def main():
    """Main entry point"""
    args = parse_args()
    
    # Create the agent
    agent = NewsMarketAgent(output_dir=args.output if hasattr(args, 'output') else 'reports')
    
    # Execute the requested command
    if args.command == "daily":
        report = agent.generate_daily_digest(topics=args.topics)
        print(f"Daily digest generated: {report.get('report_id')}")
    elif args.command == "company":
        report = agent.generate_company_analysis(args.ticker)
        print(f"Company analysis generated: {report.get('report_id')}")
    elif args.command == "sector":
        report = agent.generate_sector_analysis(args.sector)
        print(f"Sector analysis generated: {report.get('report_id')}")
    elif args.command == "schedule":
        print(f"Scheduling daily digest at {args.hour:02d}:{args.minute:02d}")
        agent.schedule_daily_digest(hour=args.hour, minute=args.minute)
    else:
        # Default action if no command is provided
        print("Generating a sample daily digest...")
        report = agent.generate_daily_digest()
        print(f"Daily digest generated: {report.get('report_id')}")

if __name__ == "__main__":
    main()
