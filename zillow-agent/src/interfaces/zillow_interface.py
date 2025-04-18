"""
Zillow Interface - Connects to Zillow API to retrieve real estate data
"""
import requests
import logging
from typing import List, Dict, Any, Optional
import os
from dotenv import load_dotenv
import json
from datetime import datetime

load_dotenv()

logger = logging.getLogger(__name__)

class ZillowInterface:
    """Interface for retrieving data from Zillow"""
    
    # For demo purposes, we'll mock the API endpoints
    BASE_URL = "https://api.zillow.com/v1"
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the Zillow interface
        
        Args:
            api_key: Optional API key (defaults to env variable)
        """
        self.api_key = api_key or os.getenv('ZILLOW_API_KEY', 'demo_api_key')
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
    
    def search_properties(self, location: str, filters: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """
        Search for properties in a specific location
        
        Args:
            location: Location to search in (city, zip code, etc.)
            filters: Optional filters like price range, bedrooms, etc.
            
        Returns:
            List of property details
        """
        try:
            # In a real implementation, this would make an API call to Zillow
            # For demo, we'll just return mock data
            return self._get_mock_properties(location, filters)
        except Exception as e:
            logger.error(f"Error searching properties: {e}")
            return []
    
    def get_property_details(self, property_id: str) -> Dict[str, Any]:
        """
        Get detailed information for a specific property
        
        Args:
            property_id: Zillow property ID
            
        Returns:
            Dictionary with property details
        """
        try:
            # Mock data for demo
            return self._get_mock_property_details(property_id)
        except Exception as e:
            logger.error(f"Error retrieving property details: {e}")
            return {}
    
    def get_market_trends(self, location: str, months: int = 12) -> Dict[str, Any]:
        """
        Get market trends for a specific location
        
        Args:
            location: Location to get trends for
            months: Number of months of trend data
            
        Returns:
            Dictionary with market trend data
        """
        try:
            # Mock data for demo
            return self._get_mock_market_trends(location, months)
        except Exception as e:
            logger.error(f"Error retrieving market trends: {e}")
            return {}
    
    def _get_mock_properties(self, location: str, filters: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """Generate mock property data for demo purposes"""
        # Generate a seed based on location for consistent mocks
        location_seed = sum(ord(c) for c in location)
        num_properties = 10 + (location_seed % 10)  # 10-20 properties
        
        properties = []
        for i in range(num_properties):
            # Generate somewhat realistic property data
            bedrooms = 2 + (location_seed + i) % 4  # 2-5 bedrooms
            bathrooms = bedrooms - 0.5 if i % 2 == 0 else bedrooms
            sqft = 800 + (location_seed + i*100) % 3000  # 800-3800 sqft
            
            # Price based on location, size, and some randomness
            base_price = 200000 + (location_seed % 1000000)  # Base price 200k-1.2M
            size_factor = sqft / 1000
            price = int(base_price * size_factor * (0.9 + (i % 20) / 100))
            
            # Apply filters if provided
            if filters:
                # Skip if property doesn't match price range
                if 'min_price' in filters and price < filters['min_price']:
                    continue
                if 'max_price' in filters and price > filters['max_price']:
                    continue
                # Skip if property doesn't match bedroom count
                if 'min_bedrooms' in filters and bedrooms < filters['min_bedrooms']:
                    continue
                if 'max_bedrooms' in filters and bedrooms > filters['max_bedrooms']:
                    continue
            
            property_data = {
                "id": f"property-{location.replace(' ', '-').lower()}-{i}",
                "address": f"{100 + i} Main St, {location}",
                "price": price,
                "bedrooms": bedrooms,
                "bathrooms": bathrooms,
                "sqft": sqft,
                "year_built": 1970 + (location_seed + i) % 50,  # 1970-2020
                "property_type": "Single Family" if i % 3 != 0 else "Condo" if i % 3 == 1 else "Townhouse",
                "listing_status": "For Sale" if i % 4 != 0 else "Recently Sold" if i % 4 == 1 else "For Rent",
                "days_on_market": (location_seed + i) % 120,  # 0-120 days
                "listing_date": (datetime.now().replace(day=1) - 
                             datetime.timedelta(days=(location_seed + i) % 120)).isoformat(),
                "photo_url": f"https://example.com/photos/property-{i}.jpg",
                "url": f"https://zillow.com/homes/{location.replace(' ', '-').lower()}/{i}",
                "source": "zillow"
            }
            
            properties.append(property_data)
        
        return properties
    
    def _get_mock_property_details(self, property_id: str) -> Dict[str, Any]:
        """Generate mock detailed property data for demo purposes"""
        # Extract location and index from ID for consistent mocks
        parts = property_id.split('-')
        location = '-'.join(parts[1:-1]).replace('-', ' ')
        index = int(parts[-1]) if parts[-1].isdigit() else 0
        
        # Create a base property with the same logic as search
        base_property = self._get_mock_properties(location, None)[index % 10]
        
        # Add additional details
        details = base_property.copy()
        details.update({
            "description": f"Beautiful {details['bedrooms']} bedroom home in {location}. " +
                          f"This {details['property_type'].lower()} offers modern amenities and great location.",
            "features": [
                "Central Air", 
                "Hardwood Floors", 
                "Garage", 
                "Fireplace" if index % 2 == 0 else "Pool",
                "Updated Kitchen",
                "Fenced Yard" if details['property_type'] == "Single Family" else "Balcony"
            ],
            "schools": [
                {
                    "name": f"{location} Elementary School",
                    "rating": min(10, 5 + (index % 6)),  # 5-10 rating
                    "distance": round(0.5 + (index % 15) / 10, 1)  # 0.5-2.0 miles
                },
                {
                    "name": f"{location} Middle School",
                    "rating": min(10, 5 + ((index + 1) % 6)),  # 5-10 rating
                    "distance": round(0.7 + ((index + 1) % 15) / 10, 1)  # 0.7-2.2 miles
                },
                {
                    "name": f"{location} High School",
                    "rating": min(10, 5 + ((index + 2) % 6)),  # 5-10 rating
                    "distance": round(1.0 + ((index + 2) % 15) / 10, 1)  # 1.0-2.5 miles
                }
            ],
            "tax_history": [
                {
                    "year": 2024,
                    "amount": round(details['price'] * 0.012)  # Approximately 1.2% of property value
                },
                {
                    "year": 2023,
                    "amount": round(details['price'] * 0.012 * 0.95)  # 5% less than current
                },
                {
                    "year": 2022,
                    "amount": round(details['price'] * 0.012 * 0.90)  # 10% less than current
                }
            ],
            "price_history": [
                {
                    "date": "2024-01-15",
                    "price": details['price'],
                    "event": "Listed"
                },
                {
                    "date": "2023-05-20",
                    "price": round(details['price'] * 0.88),
                    "event": "Sold"
                },
                {
                    "date": "2023-03-10",
                    "price": round(details['price'] * 0.90),
                    "event": "Listed"
                }
            ] if index % 3 == 0 else [],
            "neighborhood": {
                "name": f"{location} {['North', 'South', 'East', 'West', 'Central'][index % 5]}",
                "median_home_value": round(details['price'] * (0.9 + (index % 20) / 100)),
                "walk_score": 50 + (index % 50),  # 50-99
                "transit_score": 40 + (index % 60),  # 40-99
                "crime_rate": "Low" if index % 3 == 0 else "Medium" if index % 3 == 1 else "High"
            },
            "nearby_amenities": [
                {"type": "Grocery", "distance": 0.3 + (index % 10) / 10},
                {"type": "Restaurant", "distance": 0.2 + (index % 15) / 10},
                {"type": "Park", "distance": 0.5 + (index % 20) / 10},
                {"type": "School", "distance": 0.4 + (index % 12) / 10}
            ]
        })
        
        return details
    
    def _get_mock_market_trends(self, location: str, months: int = 12) -> Dict[str, Any]:
        """Generate mock market trend data for demo purposes"""
        # Generate a seed based on location for consistent mocks
        location_seed = sum(ord(c) for c in location)
        
        # Generate trend data
        median_price_start = 300000 + (location_seed % 500000)  # Starting point between 300k and 800k
        
        prices = []
        inventory = []
        days_on_market = []
        
        for i in range(months):
            # Seasonal factor (higher in summer, lower in winter)
            month = (datetime.now().month - i) % 12 + 1
            seasonal_factor = 1.0 + (abs(month - 6.5) / 30)  # 0.97-1.03 seasonal variation
            
            # Trend factor (slight upward trend)
            trend_factor = 1.0 + (0.002 * i)  # 0.2% monthly growth
            
            # Randomness factor
            random_factor = 1.0 + ((location_seed + i) % 100 - 50) / 1000  # ±5% random variation
            
            # Calculate price for this month
            price = median_price_start * seasonal_factor * trend_factor * random_factor
            
            # Inventory tends to be higher in summer
            inventory_base = 100 + (location_seed % 200)  # 100-300 base inventory
            inventory_value = inventory_base * (1.0 + (month - 1) / 24)  # Higher in summer
            
            # Days on market tends to be lower in summer
            dom_base = 30 + (location_seed % 30)  # 30-60 days base
            dom_value = dom_base * (1.0 - (month - 1) / 36)  # Lower in summer
            
            # Add data points
            prices.append({
                "month": (datetime.now().replace(day=1) - 
                        datetime.timedelta(days=30*i)).strftime("%Y-%m"),
                "value": round(price)
            })
            
            inventory.append({
                "month": (datetime.now().replace(day=1) - 
                        datetime.timedelta(days=30*i)).strftime("%Y-%m"),
                "value": round(inventory_value)
            })
            
            days_on_market.append({
                "month": (datetime.now().replace(day=1) - 
                        datetime.timedelta(days=30*i)).strftime("%Y-%m"),
                "value": round(dom_value)
            })
        
        # Calculate year-over-year changes
        yoy_price_change = (prices[0]["value"] - prices[min(11, len(prices)-1)]["value"]) / prices[min(11, len(prices)-1)]["value"]
        yoy_inventory_change = (inventory[0]["value"] - inventory[min(11, len(inventory)-1)]["value"]) / inventory[min(11, len(inventory)-1)]["value"]
        
        # Reverse to get chronological order
        prices.reverse()
        inventory.reverse()
        days_on_market.reverse()
        
        return {
            "location": location,
            "median_home_price": {
                "current": prices[-1]["value"],
                "trends": prices,
                "yoy_change": round(yoy_price_change * 100, 1)
            },
            "inventory": {
                "current": inventory[-1]["value"],
                "trends": inventory,
                "yoy_change": round(yoy_inventory_change * 100, 1)
            },
            "days_on_market": {
                "current": days_on_market[-1]["value"],
                "trends": days_on_market
            },
            "market_hotness": {
                "score": min(10, (inventory[-1]["value"] / days_on_market[-1]["value"]) / 10),
                "description": self._get_market_description(location_seed)
            },
            "forecast": {
                "next_quarter": self._get_forecast_description(location_seed, 1),
                "next_year": self._get_forecast_description(location_seed, 4)
            },
            "source": "zillow",
            "last_updated": datetime.now().isoformat()
        }
    
    def _get_market_description(self, seed: int) -> str:
        """Generate a market description based on seed"""
        descriptions = [
            "Very Hot - Seller's Market",
            "Hot - Favoring Sellers",
            "Warm - Slightly Favoring Sellers",
            "Neutral - Balanced Market",
            "Cool - Slightly Favoring Buyers",
            "Cold - Buyer's Market"
        ]
        
        index = seed % len(descriptions)
        return descriptions[index]
    
    def _get_forecast_description(self, seed: int, quarters: int) -> Dict[str, Any]:
        """Generate a market forecast based on seed and timeframe"""
        # Direction (up, down, stable)
        directions = ["increasing", "stable", "decreasing"]
        direction_index = (seed + quarters) % len(directions)
        direction = directions[direction_index]
        
        # Magnitude (small, moderate, significant)
        magnitudes = ["slightly", "moderately", "significantly"]
        magnitude_index = (seed + quarters * 2) % len(magnitudes)
        magnitude = magnitudes[magnitude_index] if direction != "stable" else ""
        
        # Combine for description
        if direction == "stable":
            description = "Prices expected to remain stable"
        else:
            description = f"Prices expected to {direction} {magnitude}"
        
        # Numeric forecast
        if direction == "increasing":
            rate = 1 + (0.01 * (1 + magnitude_index) * quarters)
        elif direction == "decreasing":
            rate = 1 - (0.01 * (1 + magnitude_index) * quarters)
        else:
            rate = 1 + (0.005 * quarters)  # Small baseline growth even for "stable"
        
        return {
            "description": description,
            "price_change_percent": round((rate - 1) * 100, 1)
        }
