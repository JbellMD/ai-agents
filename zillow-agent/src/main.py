"""
Zillow Real Estate Agent - Main Module

This agent integrates real estate data from Zillow with weather information
to provide comprehensive property analysis, recommendations, and insights.
"""
import logging
import argparse
import os
import json
from datetime import datetime
from typing import Dict, Any, Optional, List
from dotenv import load_dotenv

# Local imports
from interfaces.zillow_interface import ZillowInterface
from interfaces.weather_interface import WeatherInterface
from processors.property_processor import PropertyProcessor

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

class ZillowAgent:
    """
    Zillow Real Estate Agent
    
    This agent integrates real estate data with weather information to provide
    comprehensive property analysis and recommendations.
    """
    
    def __init__(self, output_dir: str = 'reports'):
        """
        Initialize the agent and its components
        
        Args:
            output_dir: Directory to save generated reports
        """
        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)
        self.output_dir = output_dir
        
        # Initialize components
        self.zillow = ZillowInterface()
        self.weather = WeatherInterface()
        self.processor = PropertyProcessor()
        
        logger.info("Zillow Real Estate Agent initialized")
    
    def search_properties(self, location: str, filters: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Search for properties with comprehensive context
        
        Args:
            location: Location to search in
            filters: Optional property filters
            
        Returns:
            Search results with property and market data
        """
        logger.info(f"Searching properties in {location}")
        
        # Get properties with context
        results = self.processor.search_properties_with_context(location, filters)
        
        # Save results
        self._save_results(results, f"property_search_{location.replace(' ', '_').lower()}.json")
        
        return results
    
    def get_property_recommendations(self, location: str, preferences: Dict[str, Any]) -> Dict[str, Any]:
        """
        Get personalized property recommendations
        
        Args:
            location: Location to search in
            preferences: User preferences for property features
            
        Returns:
            Recommendations with property matches
        """
        logger.info(f"Getting property recommendations for {location}")
        
        # Get recommendations
        recommendations = self.processor.get_property_recommendation(location, preferences)
        
        # Save results
        self._save_results(recommendations, f"recommendations_{location.replace(' ', '_').lower()}.json")
        
        return recommendations
    
    def analyze_investment_properties(self, location: str, 
                                     filters: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Analyze properties for investment potential
        
        Args:
            location: Location to search in
            filters: Optional property filters
            
        Returns:
            Properties with investment analysis
        """
        logger.info(f"Analyzing investment properties in {location}")
        
        # Search for properties
        properties = self.zillow.search_properties(location, filters)
        
        # Analyze investment potential
        analyzed_properties = self.processor.analyze_investment_potential(properties, location)
        
        # Get market trends
        market_trends = self.zillow.get_market_trends(location)
        
        results = {
            "properties": analyzed_properties,
            "market_trends": market_trends,
            "location": location,
            "timestamp": datetime.now().isoformat(),
            "source": "zillow_agent"
        }
        
        # Save results
        self._save_results(results, f"investment_analysis_{location.replace(' ', '_').lower()}.json")
        
        return results
    
    def get_property_details(self, property_id: str) -> Dict[str, Any]:
        """
        Get detailed information about a specific property
        
        Args:
            property_id: Zillow property ID
            
        Returns:
            Detailed property information
        """
        logger.info(f"Getting details for property {property_id}")
        
        # Get property details
        details = self.zillow.get_property_details(property_id)
        
        # Extract location from property
        location = details.get('address', '').split(',')[-1].strip()
        
        # Get weather for the location
        if location:
            current_weather = self.weather.get_current_weather(location)
            weather_forecast = self.weather.get_forecast(location, days=5)
            
            # Add weather to details
            details['weather'] = {
                'current': current_weather,
                'forecast': weather_forecast
            }
        
        # Save results
        self._save_results(details, f"property_details_{property_id}.json")
        
        return details
    
    def compare_properties(self, property_ids: List[str]) -> Dict[str, Any]:
        """
        Compare multiple properties side by side
        
        Args:
            property_ids: List of Zillow property IDs to compare
            
        Returns:
            Comparative analysis of properties
        """
        logger.info(f"Comparing properties: {property_ids}")
        
        # Get details for each property
        properties = []
        for prop_id in property_ids:
            details = self.zillow.get_property_details(prop_id)
            properties.append(details)
        
        # Extract key metrics for comparison
        comparison = {
            "properties": properties,
            "comparison_metrics": self._extract_comparison_metrics(properties),
            "timestamp": datetime.now().isoformat(),
            "source": "zillow_agent"
        }
        
        # Save results
        self._save_results(comparison, f"property_comparison_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
        
        return comparison
    
    def _extract_comparison_metrics(self, properties: List[Dict[str, Any]]) -> Dict[str, List[Any]]:
        """Extract metrics for property comparison"""
        metrics = {
            "price": [],
            "price_per_sqft": [],
            "bedrooms": [],
            "bathrooms": [],
            "sqft": [],
            "year_built": [],
            "property_type": [],
            "days_on_market": []
        }
        
        for prop in properties:
            metrics["price"].append(prop.get("price", "N/A"))
            
            # Calculate price per sqft
            if prop.get("price") and prop.get("sqft"):
                price_per_sqft = round(prop.get("price") / prop.get("sqft"), 2)
            else:
                price_per_sqft = "N/A"
            metrics["price_per_sqft"].append(price_per_sqft)
            
            metrics["bedrooms"].append(prop.get("bedrooms", "N/A"))
            metrics["bathrooms"].append(prop.get("bathrooms", "N/A"))
            metrics["sqft"].append(prop.get("sqft", "N/A"))
            metrics["year_built"].append(prop.get("year_built", "N/A"))
            metrics["property_type"].append(prop.get("property_type", "N/A"))
            metrics["days_on_market"].append(prop.get("days_on_market", "N/A"))
        
        return metrics
    
    def _save_results(self, results: Dict[str, Any], filename: str) -> None:
        """Save results to file"""
        try:
            filepath = os.path.join(self.output_dir, filename)
            with open(filepath, 'w') as f:
                json.dump(results, f, indent=2)
            logger.info(f"Results saved to {filepath}")
        except Exception as e:
            logger.error(f"Error saving results: {e}")

def parse_args():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(description="Zillow Real Estate Agent")
    
    # Create subparsers for different commands
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")
    
    # Search command
    search_parser = subparsers.add_parser("search", help="Search for properties")
    search_parser.add_argument("location", help="Location to search in")
    search_parser.add_argument("--min_price", type=int, help="Minimum price")
    search_parser.add_argument("--max_price", type=int, help="Maximum price")
    search_parser.add_argument("--bedrooms", type=int, help="Number of bedrooms")
    search_parser.add_argument("--property_type", help="Property type")
    search_parser.add_argument("--output", default="reports", help="Output directory")
    
    # Recommend command
    recommend_parser = subparsers.add_parser("recommend", help="Get property recommendations")
    recommend_parser.add_argument("location", help="Location to search in")
    recommend_parser.add_argument("--min_price", type=int, help="Minimum price")
    recommend_parser.add_argument("--max_price", type=int, help="Maximum price")
    recommend_parser.add_argument("--bedrooms", type=int, help="Number of bedrooms")
    recommend_parser.add_argument("--bathrooms", type=float, help="Number of bathrooms")
    recommend_parser.add_argument("--property_type", help="Property type")
    recommend_parser.add_argument("--output", default="reports", help="Output directory")
    
    # Investment command
    invest_parser = subparsers.add_parser("invest", help="Analyze investment properties")
    invest_parser.add_argument("location", help="Location to search in")
    invest_parser.add_argument("--min_price", type=int, help="Minimum price")
    invest_parser.add_argument("--max_price", type=int, help="Maximum price")
    invest_parser.add_argument("--property_type", help="Property type")
    invest_parser.add_argument("--output", default="reports", help="Output directory")
    
    # Details command
    details_parser = subparsers.add_parser("details", help="Get property details")
    details_parser.add_argument("property_id", help="Zillow property ID")
    details_parser.add_argument("--output", default="reports", help="Output directory")
    
    # Compare command
    compare_parser = subparsers.add_parser("compare", help="Compare properties")
    compare_parser.add_argument("property_ids", nargs="+", help="Zillow property IDs to compare")
    compare_parser.add_argument("--output", default="reports", help="Output directory")
    
    return parser.parse_args()

def main():
    """Main entry point"""
    args = parse_args()
    
    # Create agent
    agent = ZillowAgent(output_dir=args.output if hasattr(args, 'output') else 'reports')
    
    # Execute command
    if args.command == "search":
        # Build filters from arguments
        filters = {}
        if hasattr(args, 'min_price') and args.min_price:
            filters['min_price'] = args.min_price
        if hasattr(args, 'max_price') and args.max_price:
            filters['max_price'] = args.max_price
        if hasattr(args, 'bedrooms') and args.bedrooms:
            filters['min_bedrooms'] = args.bedrooms
        if hasattr(args, 'property_type') and args.property_type:
            filters['property_type'] = args.property_type
        
        results = agent.search_properties(args.location, filters)
        print(f"Found {len(results['properties'])} properties in {args.location}")
        
    elif args.command == "recommend":
        # Build preferences from arguments
        preferences = {}
        if hasattr(args, 'min_price') and args.min_price:
            preferences['min_price'] = args.min_price
        if hasattr(args, 'max_price') and args.max_price:
            preferences['max_price'] = args.max_price
        if hasattr(args, 'bedrooms') and args.bedrooms:
            preferences['bedrooms'] = args.bedrooms
        if hasattr(args, 'bathrooms') and args.bathrooms:
            preferences['bathrooms'] = args.bathrooms
        if hasattr(args, 'property_type') and args.property_type:
            preferences['property_type'] = args.property_type
        
        results = agent.get_property_recommendations(args.location, preferences)
        print(f"Generated {len(results['recommendations'])} recommendations for {args.location}")
        
    elif args.command == "invest":
        # Build filters from arguments
        filters = {}
        if hasattr(args, 'min_price') and args.min_price:
            filters['min_price'] = args.min_price
        if hasattr(args, 'max_price') and args.max_price:
            filters['max_price'] = args.max_price
        if hasattr(args, 'property_type') and args.property_type:
            filters['property_type'] = args.property_type
        
        results = agent.analyze_investment_properties(args.location, filters)
        print(f"Analyzed {len(results['properties'])} investment properties in {args.location}")
        
    elif args.command == "details":
        results = agent.get_property_details(args.property_id)
        print(f"Retrieved details for property {args.property_id}")
        
    elif args.command == "compare":
        results = agent.compare_properties(args.property_ids)
        print(f"Compared {len(results['properties'])} properties")
        
    else:
        # Default action
        print("Searching properties in a default location...")
        results = agent.search_properties("San Francisco, CA")
        print(f"Found {len(results['properties'])} properties in San Francisco, CA")

if __name__ == "__main__":
    main()
