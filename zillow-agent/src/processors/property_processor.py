"""
Property Processor - Analyzes real estate data and generates insights
"""
import logging
from typing import List, Dict, Any, Optional
from datetime import datetime

# Local imports
from ..interfaces.zillow_interface import ZillowInterface
from ..interfaces.weather_interface import WeatherInterface

logger = logging.getLogger(__name__)

class PropertyProcessor:
    """Processes and analyzes real estate property data"""
    
    def __init__(self):
        """Initialize property processor and its dependencies"""
        self.zillow = ZillowInterface()
        self.weather = WeatherInterface()
    
    def search_properties_with_context(self, location: str, filters: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Search for properties with additional contextual information
        
        Args:
            location: Location to search in
            filters: Optional property filters
            
        Returns:
            Dictionary with properties and contextual data
        """
        # Get properties
        properties = self.zillow.search_properties(location, filters)
        
        # Get market trends
        market_trends = self.zillow.get_market_trends(location)
        
        # Get weather data
        current_weather = self.weather.get_current_weather(location)
        weather_forecast = self.weather.get_forecast(location, days=5)
        
        # Calculate property metrics
        avg_price = sum(p.get('price', 0) for p in properties) / len(properties) if properties else 0
        avg_price_per_sqft = sum(p.get('price', 0) / p.get('sqft', 1) for p in properties) / len(properties) if properties else 0
        
        # Categorize properties
        categorized_properties = self._categorize_properties(properties)
        
        return {
            "properties": properties,
            "market_trends": market_trends,
            "weather": {
                "current": current_weather,
                "forecast": weather_forecast
            },
            "metrics": {
                "count": len(properties),
                "avg_price": int(avg_price),
                "avg_price_per_sqft": int(avg_price_per_sqft),
                "types": {k: len(v) for k, v in categorized_properties.items()}
            },
            "timestamp": datetime.now().isoformat(),
            "source": "property_processor"
        }
    
    def get_property_recommendation(self, location: str, preferences: Dict[str, Any]) -> Dict[str, Any]:
        """
        Get property recommendations based on user preferences
        
        Args:
            location: Location to search in
            preferences: User preferences for property features
            
        Returns:
            Dictionary with recommended properties and insights
        """
        # Convert preferences to filters for the search
        filters = self._preferences_to_filters(preferences)
        
        # Get properties matching filters
        all_properties = self.zillow.search_properties(location, filters)
        
        # Score properties based on preferences
        scored_properties = self._score_properties(all_properties, preferences)
        
        # Get top recommendations
        top_recommendations = sorted(scored_properties, key=lambda x: x['match_score'], reverse=True)[:5]
        
        # Get weather influence
        weather_insights = self._get_weather_insights(location)
        
        return {
            "recommendations": top_recommendations,
            "match_criteria": preferences,
            "location_insights": {
                "market_trends": self.zillow.get_market_trends(location),
                "weather_insights": weather_insights
            },
            "timestamp": datetime.now().isoformat(),
            "source": "property_processor"
        }
    
    def analyze_investment_potential(self, properties: List[Dict[str, Any]], 
                                    location: str) -> List[Dict[str, Any]]:
        """
        Analyze investment potential of properties
        
        Args:
            properties: List of properties to analyze
            location: Location of properties
            
        Returns:
            List of properties with added investment analysis
        """
        # Get market trends for rent/price ratio and appreciation
        market_trends = self.zillow.get_market_trends(location)
        
        # Analyze each property
        analyzed_properties = []
        
        for property in properties:
            # Calculate estimated rental income (using a simple price-to-rent ratio)
            # Normally this would use more sophisticated methods
            price = property.get('price', 0)
            sqft = property.get('sqft', 1000)
            bedrooms = property.get('bedrooms', 2)
            
            # Estimate monthly rent (very simplified model)
            estimated_rent = (price * 0.005) + (bedrooms * 100) + (sqft * 0.1)
            estimated_rent = min(5000, max(500, int(estimated_rent)))  # Reasonable bounds
            
            # Calculate investment metrics
            annual_rental_income = estimated_rent * 12
            annual_expenses = price * 0.02  # Property tax, insurance, maintenance (~2% of value)
            net_income = annual_rental_income - annual_expenses
            cap_rate = (net_income / price) * 100 if price > 0 else 0
            
            # Estimate appreciation based on market trends
            appreciation_rate = market_trends.get('median_home_price', {}).get('yoy_change', 3) / 100
            estimated_5yr_value = price * (1 + appreciation_rate) ** 5
            
            # Add analysis to property
            property_with_analysis = property.copy()
            property_with_analysis.update({
                "investment_analysis": {
                    "estimated_monthly_rent": int(estimated_rent),
                    "annual_rental_income": int(annual_rental_income),
                    "annual_expenses": int(annual_expenses),
                    "net_annual_income": int(net_income),
                    "cap_rate": round(cap_rate, 2),
                    "estimated_5yr_value": int(estimated_5yr_value),
                    "estimated_5yr_appreciation": round((estimated_5yr_value - price) / price * 100, 1),
                    "investment_rating": self._get_investment_rating(cap_rate, appreciation_rate)
                }
            })
            
            analyzed_properties.append(property_with_analysis)
        
        # Sort by investment rating
        return sorted(analyzed_properties, 
                     key=lambda x: x['investment_analysis']['cap_rate'], 
                     reverse=True)
    
    def _categorize_properties(self, properties: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
        """Categorize properties by type"""
        categories = {}
        
        for prop in properties:
            prop_type = prop.get('property_type', 'Unknown')
            
            if prop_type not in categories:
                categories[prop_type] = []
                
            categories[prop_type].append(prop)
        
        return categories
    
    def _preferences_to_filters(self, preferences: Dict[str, Any]) -> Dict[str, Any]:
        """Convert user preferences to search filters"""
        filters = {}
        
        # Map common preference fields to filter fields
        if 'min_price' in preferences:
            filters['min_price'] = preferences['min_price']
        if 'max_price' in preferences:
            filters['max_price'] = preferences['max_price']
        if 'min_bedrooms' in preferences:
            filters['min_bedrooms'] = preferences['min_bedrooms']
        if 'max_bedrooms' in preferences:
            filters['max_bedrooms'] = preferences['max_bedrooms']
        if 'min_bathrooms' in preferences:
            filters['min_bathrooms'] = preferences['min_bathrooms']
        if 'property_type' in preferences:
            filters['property_type'] = preferences['property_type']
        
        return filters
    
    def _score_properties(self, properties: List[Dict[str, Any]], 
                         preferences: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Score properties based on how well they match preferences"""
        scored_properties = []
        
        for prop in properties:
            # Start with a perfect score and deduct points for mismatches
            score = 100
            match_details = {}
            
            # Score based on price
            if 'max_price' in preferences and prop.get('price', 0) > preferences['max_price']:
                penalty = min(50, ((prop.get('price', 0) - preferences['max_price']) / preferences['max_price']) * 100)
                score -= penalty
                match_details['price'] = f"Above budget by ${prop.get('price', 0) - preferences['max_price']}"
            elif 'min_price' in preferences and prop.get('price', 0) < preferences['min_price']:
                # Small penalty for being under budget (may indicate lower quality)
                penalty = min(10, ((preferences['min_price'] - prop.get('price', 0)) / preferences['min_price']) * 20)
                score -= penalty
                match_details['price'] = f"Below budget by ${preferences['min_price'] - prop.get('price', 0)}"
            else:
                match_details['price'] = "Within budget"
            
            # Score based on bedrooms
            if 'bedrooms' in preferences:
                if prop.get('bedrooms', 0) != preferences['bedrooms']:
                    penalty = min(20, abs(prop.get('bedrooms', 0) - preferences['bedrooms']) * 10)
                    score -= penalty
                    match_details['bedrooms'] = f"Mismatch: {prop.get('bedrooms', 0)} vs {preferences['bedrooms']} preferred"
                else:
                    match_details['bedrooms'] = "Exact match"
            
            # Score based on bathrooms
            if 'bathrooms' in preferences:
                if prop.get('bathrooms', 0) != preferences['bathrooms']:
                    penalty = min(15, abs(prop.get('bathrooms', 0) - preferences['bathrooms']) * 10)
                    score -= penalty
                    match_details['bathrooms'] = f"Mismatch: {prop.get('bathrooms', 0)} vs {preferences['bathrooms']} preferred"
                else:
                    match_details['bathrooms'] = "Exact match"
            
            # Score based on property type
            if 'property_type' in preferences and prop.get('property_type', '') != preferences['property_type']:
                score -= 30
                match_details['property_type'] = f"Mismatch: {prop.get('property_type', '')} vs {preferences['property_type']} preferred"
            elif 'property_type' in preferences:
                match_details['property_type'] = "Exact match"
            
            # Add match score to property
            prop_with_score = prop.copy()
            prop_with_score.update({
                "match_score": max(0, round(score)),
                "match_details": match_details
            })
            
            scored_properties.append(prop_with_score)
        
        return scored_properties
    
    def _get_weather_insights(self, location: str) -> Dict[str, Any]:
        """Get weather insights for a location"""
        current_weather = self.weather.get_current_weather(location)
        forecast = self.weather.get_forecast(location, days=7)
        
        # Extract weather condition
        condition = current_weather.get('condition', {}).get('type', 'Unknown')
        
        # Check for extreme weather
        has_extreme_weather = condition in ["Thunderstorm", "Snowy", "Foggy"]
        
        # Count sunny days in forecast
        sunny_days = sum(1 for day in forecast.get('daily', []) 
                        if day.get('condition') in ["Sunny", "Partly Cloudy"])
        
        return {
            "current_condition": condition,
            "viewing_recommendation": "Not ideal for viewing" if has_extreme_weather else "Good for viewing",
            "sunny_days_next_week": sunny_days,
            "source": "weather"
        }
    
    def _get_investment_rating(self, cap_rate: float, appreciation_rate: float) -> str:
        """Get investment rating based on cap rate and appreciation"""
        # Combine cap rate and appreciation for overall rating
        combined_score = cap_rate + (appreciation_rate * 100 * 2)  # Weight appreciation more
        
        if combined_score > 15:
            return "Excellent"
        elif combined_score > 10:
            return "Good"
        elif combined_score > 5:
            return "Fair"
        else:
            return "Poor"
