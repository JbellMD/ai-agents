"""
Company Monitor Interface - Connects to company data sources to monitor specific companies
"""
import requests
import logging
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

class CompanyMonitorInterface:
    """Interface for monitoring company data and news"""
    
    # For demo purposes, we'll mock the API endpoints
    BASE_URL = "https://api.companymonitor.io/v1"
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the Company Monitor interface
        
        Args:
            api_key: Optional API key (defaults to env variable)
        """
        self.api_key = api_key or os.getenv('COMPANY_MONITOR_API_KEY', 'demo_api_key')
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
    
    def get_company_profile(self, ticker: str) -> Dict[str, Any]:
        """
        Get detailed profile information for a company
        
        Args:
            ticker: Company stock ticker symbol
            
        Returns:
            Dictionary with company profile data
        """
        try:
            # Simulated API call
            # response = requests.get(
            #     f"{self.BASE_URL}/company/{ticker}/profile",
            #     headers=self.headers
            # )
            # response.raise_for_status()
            # return response.json()
            
            # Mock data for demo
            return self._get_mock_company_profile(ticker)
        except Exception as e:
            logger.error(f"Error retrieving company profile for {ticker}: {e}")
            return {}
    
    def get_company_news(self, ticker: str, days: int = 7) -> List[Dict[str, Any]]:
        """
        Get recent news for a specific company
        
        Args:
            ticker: Company stock ticker symbol
            days: Number of days of news to retrieve
            
        Returns:
            List of news articles about the company
        """
        try:
            # Simulated API call
            # response = requests.get(
            #     f"{self.BASE_URL}/company/{ticker}/news",
            #     params={"days": days},
            #     headers=self.headers
            # )
            # response.raise_for_status()
            # return response.json()
            
            # Mock data for demo
            return self._get_mock_company_news(ticker, days)
        except Exception as e:
            logger.error(f"Error retrieving company news for {ticker}: {e}")
            return []
    
    def get_financial_metrics(self, ticker: str) -> Dict[str, Any]:
        """
        Get key financial metrics for a company
        
        Args:
            ticker: Company stock ticker symbol
            
        Returns:
            Dictionary with financial metrics
        """
        try:
            # Simulated API call
            # response = requests.get(
            #     f"{self.BASE_URL}/company/{ticker}/financials",
            #     headers=self.headers
            # )
            # response.raise_for_status()
            # return response.json()
            
            # Mock data for demo
            return self._get_mock_financial_metrics(ticker)
        except Exception as e:
            logger.error(f"Error retrieving financial metrics for {ticker}: {e}")
            return {}
    
    def get_insider_trading(self, ticker: str, months: int = 3) -> List[Dict[str, Any]]:
        """
        Get insider trading activity for a company
        
        Args:
            ticker: Company stock ticker symbol
            months: Number of months of insider trading data to retrieve
            
        Returns:
            List of insider trading activities
        """
        try:
            # Simulated API call
            # response = requests.get(
            #     f"{self.BASE_URL}/company/{ticker}/insider-trading",
            #     params={"months": months},
            #     headers=self.headers
            # )
            # response.raise_for_status()
            # return response.json()
            
            # Mock data for demo
            return self._get_mock_insider_trading(ticker, months)
        except Exception as e:
            logger.error(f"Error retrieving insider trading for {ticker}: {e}")
            return []
    
    def get_competitors(self, ticker: str) -> Dict[str, Any]:
        """
        Get competitor information for a company
        
        Args:
            ticker: Company stock ticker symbol
            
        Returns:
            Dictionary with competitor data
        """
        try:
            # Simulated API call
            # response = requests.get(
            #     f"{self.BASE_URL}/company/{ticker}/competitors",
            #     headers=self.headers
            # )
            # response.raise_for_status()
            # return response.json()
            
            # Mock data for demo
            return self._get_mock_competitors(ticker)
        except Exception as e:
            logger.error(f"Error retrieving competitors for {ticker}: {e}")
            return {}
    
    def _get_mock_company_profile(self, ticker: str) -> Dict[str, Any]:
        """Generate mock company profile data for demo purposes"""
        # Company profiles based on common tech tickers
        company_profiles = {
            "AAPL": {
                "name": "Apple Inc.",
                "sector": "Technology",
                "industry": "Consumer Electronics",
                "description": "Apple designs, manufactures, and markets smartphones, personal computers, tablets, wearables, and accessories, and sells a variety of related services.",
                "ceo": "Tim Cook",
                "employees": 161000,
                "founded": 1976,
                "headquarters": "Cupertino, California",
                "website": "https://www.apple.com"
            },
            "MSFT": {
                "name": "Microsoft Corporation",
                "sector": "Technology",
                "industry": "Software—Infrastructure",
                "description": "Microsoft develops, licenses, and supports software, services, devices, and solutions worldwide.",
                "ceo": "Satya Nadella",
                "employees": 221000,
                "founded": 1975,
                "headquarters": "Redmond, Washington",
                "website": "https://www.microsoft.com"
            },
            "GOOGL": {
                "name": "Alphabet Inc.",
                "sector": "Technology",
                "industry": "Internet Content & Information",
                "description": "Alphabet provides web-based search, advertisements, maps, software applications, mobile operating systems, consumer content, enterprise solutions, commerce, and hardware products.",
                "ceo": "Sundar Pichai",
                "employees": 190234,
                "founded": 1998,
                "headquarters": "Mountain View, California",
                "website": "https://www.abc.xyz"
            },
            "AMZN": {
                "name": "Amazon.com, Inc.",
                "sector": "Consumer Cyclical",
                "industry": "Internet Retail",
                "description": "Amazon engages in the retail sale of consumer products and subscriptions in North America and internationally.",
                "ceo": "Andy Jassy",
                "employees": 1540000,
                "founded": 1994,
                "headquarters": "Seattle, Washington",
                "website": "https://www.amazon.com"
            },
            "META": {
                "name": "Meta Platforms, Inc.",
                "sector": "Technology",
                "industry": "Internet Content & Information",
                "description": "Meta builds technologies that help people connect, find communities, and grow businesses.",
                "ceo": "Mark Zuckerberg",
                "employees": 77805,
                "founded": 2004,
                "headquarters": "Menlo Park, California",
                "website": "https://about.meta.com"
            }
        }
        
        # Default profile for tickers not in our mock database
        default_profile = {
            "name": f"{ticker} Corporation",
            "sector": "Unknown",
            "industry": "Unknown",
            "description": f"A company trading under the ticker {ticker}.",
            "ceo": "Unknown",
            "employees": 0,
            "founded": 0,
            "headquarters": "Unknown",
            "website": f"https://www.{ticker.lower()}.com"
        }
        
        # Get the profile or default
        profile = company_profiles.get(ticker.upper(), default_profile).copy()
        
        # Add additional fields
        profile.update({
            "ticker": ticker.upper(),
            "exchange": "NASDAQ",
            "market_cap": self._get_mock_market_cap(ticker),
            "pe_ratio": round(20 + (sum(ord(c) for c in ticker) % 30), 2),
            "dividend_yield": round((sum(ord(c) for c in ticker) % 35) / 10, 2),
            "source": "company_monitor",
            "last_updated": datetime.now().isoformat()
        })
        
        return profile
    
    def _get_mock_market_cap(self, ticker: str) -> Dict[str, Any]:
        """Generate mock market cap data for demo purposes"""
        # Generate a consistent market cap based on ticker
        ticker_seed = sum(ord(c) for c in ticker)
        base_value = 10 + (ticker_seed % 990)  # 10-1000 billion
        
        value_billions = base_value
        if ticker.upper() in ["AAPL", "MSFT", "GOOGL", "AMZN", "META"]:
            # For big tech, use higher values
            value_billions = 1000 + (ticker_seed % 2000)
        
        return {
            "value_billions": value_billions,
            "currency": "USD",
            "change_percent_1d": round(((ticker_seed % 11) - 5) / 10, 2),
            "change_percent_1m": round(((ticker_seed % 41) - 20) / 10, 2),
            "change_percent_1y": round(((ticker_seed % 61) - 30) / 10, 2)
        }
    
    def _get_mock_company_news(self, ticker: str, days: int) -> List[Dict[str, Any]]:
        """Generate mock company news data for demo purposes"""
        company_name = self._get_mock_company_profile(ticker)["name"]
        ticker_seed = sum(ord(c) for c in ticker)
        
        news_templates = [
            "{company} Reports Strong Q{quarter} Earnings, Exceeding Analyst Expectations",
            "{company} Announces New Product Line",
            "{company} Expands Operations to New Markets",
            "{company} CEO Discusses Future Growth Strategies",
            "{company} Partners with {partner} on Joint Venture",
            "Analysts Upgrade {company} Stock Rating",
            "{company} to Invest $1 Billion in R&D",
            "{company} Faces Regulatory Scrutiny Over Business Practices",
            "{company} Completes Acquisition of {startup}",
            "{company} Stock Surges Following Positive Earnings Report"
        ]
        
        partners = ["Microsoft", "Google", "Amazon", "IBM", "Oracle", "Salesforce"]
        startups = ["TechFusion", "DataNova", "AIWorks", "CloudPeak", "QuantumSoft", "NexGen"]
        
        news_items = []
        for i in range(min(days, len(news_templates))):
            template_index = (ticker_seed + i) % len(news_templates)
            template = news_templates[template_index]
            
            # Fill in template variables
            partner_index = (ticker_seed + i) % len(partners)
            startup_index = (ticker_seed + i*2) % len(startups)
            quarter = ((ticker_seed + i) % 4) + 1
            
            title = template.format(
                company=company_name,
                partner=partners[partner_index],
                startup=startups[startup_index],
                quarter=quarter
            )
            
            # Generate a date within the specified range
            date = (datetime.now() - timedelta(days=i)).isoformat()
            
            news_items.append({
                "id": f"news-{ticker}-{i}",
                "title": title,
                "url": f"https://companynews.com/{ticker.lower()}/{i}",
                "source": "Financial News Network",
                "published_date": date,
                "summary": f"This article discusses {title.lower()} and its implications for investors.",
                "sentiment": {
                    "score": round(((ticker_seed + i) % 20 - 10) / 10, 1),  # -1.0 to 1.0
                    "label": "positive" if (ticker_seed + i) % 3 != 0 else "negative"
                },
                "related_tickers": self._get_mock_related_tickers(ticker, 3),
                "source": "company_monitor"
            })
        
        return news_items
    
    def _get_mock_financial_metrics(self, ticker: str) -> Dict[str, Any]:
        """Generate mock financial metrics data for demo purposes"""
        ticker_seed = sum(ord(c) for c in ticker)
        
        # Generate semi-realistic financial data based on ticker seed
        revenue_base = 10 + (ticker_seed % 90)  # 10-100 billion
        profit_margin = 10 + (ticker_seed % 30)  # 10-40%
        
        # Higher revenue for big tech
        if ticker.upper() in ["AAPL", "MSFT", "GOOGL", "AMZN", "META"]:
            revenue_base = 100 + (ticker_seed % 300)  # 100-400 billion
        
        return {
            "financial_ratios": {
                "pe_ratio": round(15 + (ticker_seed % 35), 2),
                "price_to_sales": round(2 + (ticker_seed % 8), 2),
                "price_to_book": round(3 + (ticker_seed % 7), 2),
                "debt_to_equity": round(0.5 + (ticker_seed % 15) / 10, 2),
                "current_ratio": round(1.5 + (ticker_seed % 15) / 10, 2),
                "quick_ratio": round(1.0 + (ticker_seed % 10) / 10, 2),
                "roe": round(10 + (ticker_seed % 30), 2),  # 10-40%
                "roa": round(5 + (ticker_seed % 15), 2)  # 5-20%
            },
            "revenue": {
                "annual_revenue_billions": revenue_base,
                "quarterly_revenue_millions": revenue_base * 250 + (ticker_seed % 1000),
                "revenue_growth_yoy": round(5 + (ticker_seed % 25), 2),  # 5-30%
                "revenue_growth_qoq": round(1 + (ticker_seed % 9), 2)  # 1-10%
            },
            "profitability": {
                "profit_margin": profit_margin,
                "operating_margin": round(profit_margin * 0.8, 2),
                "gross_margin": round(profit_margin * 1.5, 2),
                "ebitda_margin": round(profit_margin * 1.2, 2),
                "net_income_billions": round(revenue_base * profit_margin / 100, 2)
            },
            "cash_flow": {
                "operating_cash_flow_billions": round(revenue_base * 0.2, 2),
                "free_cash_flow_billions": round(revenue_base * 0.15, 2),
                "capital_expenditure_billions": round(revenue_base * 0.05, 2),
                "dividend_payout_ratio": round((ticker_seed % 80), 2)  # 0-80%
            },
            "valuation": {
                "enterprise_value_billions": round(revenue_base * 4 + (ticker_seed % 100), 2),
                "ev_to_revenue": round(3 + (ticker_seed % 7), 2),
                "ev_to_ebitda": round(10 + (ticker_seed % 20), 2)
            },
            "source": "company_monitor",
            "last_updated": datetime.now().isoformat()
        }
    
    def _get_mock_insider_trading(self, ticker: str, months: int) -> List[Dict[str, Any]]:
        """Generate mock insider trading data for demo purposes"""
        ticker_seed = sum(ord(c) for c in ticker)
        company = self._get_mock_company_profile(ticker)
        
        # Generate insider names based on company
        ceo_name = company.get("ceo", "CEO")
        insiders = [
            ceo_name,
            f"Jane Smith, CFO",
            f"Michael Johnson, CTO",
            f"Sarah Williams, COO",
            f"Robert Brown, Director",
            f"Jennifer Davis, SVP of Sales",
            f"David Miller, VP of Engineering"
        ]
        
        # Transaction types and their probabilities
        transaction_types = ["Buy", "Sell", "Sell"]  # Sell is more common
        
        activities = []
        for i in range(min(months * 3, 12)):  # 3 activities per month, max 12
            insider_index = (ticker_seed + i) % len(insiders)
            insider = insiders[insider_index]
            
            # Transaction type
            tx_type_index = (ticker_seed + i) % len(transaction_types)
            tx_type = transaction_types[tx_type_index]
            
            # Generate a date within the specified range
            date = (datetime.now() - timedelta(days=i*10)).isoformat()
            
            # Transaction details
            shares = (ticker_seed + i*100) % 10000 + 1000  # 1000-11000 shares
            price = round(50 + (ticker_seed % 950), 2)  # $50-$1000 per share
            value = round(shares * price, 2)
            
            activities.append({
                "id": f"insider-{ticker}-{i}",
                "date": date,
                "insider_name": insider,
                "title": insider.split(", ")[1] if ", " in insider else "Unknown",
                "transaction_type": tx_type,
                "shares": shares,
                "price_per_share": price,
                "total_value": value,
                "shares_owned_after": (ticker_seed + i*1000) % 100000 + 10000,  # 10k-110k shares
                "form_type": "Form 4",
                "source": "company_monitor"
            })
        
        return activities
    
    def _get_mock_competitors(self, ticker: str) -> Dict[str, Any]:
        """Generate mock competitor data for demo purposes"""
        # Define competitor relationships for common tickers
        competitor_map = {
            "AAPL": ["MSFT", "GOOGL", "SSNLF", "HPQ"],
            "MSFT": ["AAPL", "GOOGL", "ORCL", "IBM"],
            "GOOGL": ["MSFT", "META", "AAPL", "AMZN"],
            "AMZN": ["WMT", "EBAY", "TGT", "BABA"],
            "META": ["SNAP", "GOOGL", "TWTR", "PINS"]
        }
        
        # Get competitors for the ticker
        ticker_upper = ticker.upper()
        competitors = competitor_map.get(ticker_upper, [])
        
        # If no predefined competitors, generate some
        if not competitors:
            ticker_seed = sum(ord(c) for c in ticker)
            all_tickers = list(competitor_map.keys())
            
            # Select random tickers as competitors
            for i in range(3):
                idx = (ticker_seed + i) % len(all_tickers)
                competitor = all_tickers[idx]
                if competitor != ticker_upper and competitor not in competitors:
                    competitors.append(competitor)
        
        # Generate competitor details
        competitor_details = []
        for comp_ticker in competitors:
            profile = self._get_mock_company_profile(comp_ticker)
            
            competitor_details.append({
                "ticker": comp_ticker,
                "name": profile["name"],
                "market_cap_billions": profile["market_cap"]["value_billions"],
                "sector": profile["sector"],
                "industry": profile["industry"]
            })
        
        return {
            "company": ticker_upper,
            "competitors": competitor_details,
            "market_share": self._get_mock_market_share(ticker, competitors),
            "comparative_metrics": self._get_mock_comparative_metrics(ticker, competitors),
            "source": "company_monitor",
            "last_updated": datetime.now().isoformat()
        }
    
    def _get_mock_market_share(self, ticker: str, competitors: List[str]) -> Dict[str, float]:
        """Generate mock market share data for demo purposes"""
        ticker_seed = sum(ord(c) for c in ticker)
        
        # Assign market shares
        market_shares = {ticker.upper(): 20 + (ticker_seed % 30)}  # 20-50%
        
        remaining_share = 100 - market_shares[ticker.upper()]
        per_competitor = remaining_share / (len(competitors) + 1)  # +1 for "Others"
        
        for i, comp in enumerate(competitors):
            # Vary the share a bit for each competitor
            variation = ((ticker_seed + i) % 10) - 5  # -5 to +5
            comp_share = per_competitor + variation
            market_shares[comp] = round(max(1, comp_share), 1)  # Ensure at least 1%
        
        # Add "Others" category with remaining share
        assigned_share = sum(market_shares.values())
        market_shares["Others"] = round(max(1, 100 - assigned_share), 1)
        
        return market_shares
    
    def _get_mock_comparative_metrics(self, ticker: str, competitors: List[str]) -> Dict[str, Dict[str, float]]:
        """Generate mock comparative metrics data for demo purposes"""
        ticker_seed = sum(ord(c) for c in ticker)
        
        metrics = {
            "revenue_growth": {},
            "profit_margin": {},
            "pe_ratio": {},
            "price_to_sales": {}
        }
        
        # Generate metrics for main ticker
        metrics["revenue_growth"][ticker.upper()] = round(5 + (ticker_seed % 25), 1)  # 5-30%
        metrics["profit_margin"][ticker.upper()] = round(10 + (ticker_seed % 30), 1)  # 10-40%
        metrics["pe_ratio"][ticker.upper()] = round(15 + (ticker_seed % 35), 1)  # 15-50
        metrics["price_to_sales"][ticker.upper()] = round(2 + (ticker_seed % 8), 1)  # 2-10
        
        # Generate metrics for competitors
        for i, comp in enumerate(competitors):
            comp_seed = ticker_seed + sum(ord(c) for c in comp)
            
            metrics["revenue_growth"][comp] = round(5 + (comp_seed % 25), 1)  # 5-30%
            metrics["profit_margin"][comp] = round(10 + (comp_seed % 30), 1)  # 10-40%
            metrics["pe_ratio"][comp] = round(15 + (comp_seed % 35), 1)  # 15-50
            metrics["price_to_sales"][comp] = round(2 + (comp_seed % 8), 1)  # 2-10
        
        return metrics
    
    def _get_mock_related_tickers(self, ticker: str, count: int) -> List[str]:
        """Generate mock related tickers for demo purposes"""
        related = self._get_mock_competitors(ticker)["competitors"]
        return [comp["ticker"] for comp in related[:count]]
