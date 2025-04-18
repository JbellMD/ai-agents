"""
Weather Interface - Connects to Weather API to retrieve weather data for locations
"""
import requests
import logging
from typing import Dict, Any, Optional
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta

load_dotenv()

logger = logging.getLogger(__name__)

class WeatherInterface:
    """Interface for retrieving weather data"""
    
    # For demo purposes, we'll mock the API endpoints
    BASE_URL = "https://api.weather.io/v1"
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the Weather interface
        
        Args:
            api_key: Optional API key (defaults to env variable)
        """
        self.api_key = api_key or os.getenv('WEATHER_API_KEY', 'demo_api_key')
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
    
    def get_current_weather(self, location: str) -> Dict[str, Any]:
        """
        Get current weather for a location
        
        Args:
            location: Location to get weather for (city, zip code, etc.)
            
        Returns:
            Dictionary with current weather data
        """
        try:
            # In a real implementation, this would make an API call
            # For demo, we'll just return mock data
            return self._get_mock_current_weather(location)
        except Exception as e:
            logger.error(f"Error retrieving current weather for {location}: {e}")
            return {}
    
    def get_forecast(self, location: str, days: int = 7) -> Dict[str, Any]:
        """
        Get weather forecast for a location
        
        Args:
            location: Location to get forecast for
            days: Number of days to forecast
            
        Returns:
            Dictionary with forecast data
        """
        try:
            # Mock data for demo
            return self._get_mock_forecast(location, days)
        except Exception as e:
            logger.error(f"Error retrieving forecast for {location}: {e}")
            return {}
    
    def get_historical_weather(self, location: str, days_ago: int = 30) -> Dict[str, Any]:
        """
        Get historical weather data for a location
        
        Args:
            location: Location to get historical data for
            days_ago: Days in the past to retrieve data for
            
        Returns:
            Dictionary with historical weather data
        """
        try:
            # Mock data for demo
            return self._get_mock_historical_weather(location, days_ago)
        except Exception as e:
            logger.error(f"Error retrieving historical weather for {location}: {e}")
            return {}
    
    def _get_mock_current_weather(self, location: str) -> Dict[str, Any]:
        """Generate mock current weather data for demo purposes"""
        # Generate a seed based on location for consistent mocks
        location_seed = sum(ord(c) for c in location)
        
        # Generate weather based on seed
        weather_types = ["Sunny", "Partly Cloudy", "Cloudy", "Rainy", "Thunderstorm", "Snowy", "Foggy"]
        weather_index = location_seed % len(weather_types)
        weather_type = weather_types[weather_index]
        
        # Temperature based on weather type and some randomness
        base_temp = 70  # Base temperature in Fahrenheit
        if weather_type == "Sunny":
            temp = base_temp + 10 + (location_seed % 10)
        elif weather_type in ["Partly Cloudy", "Cloudy"]:
            temp = base_temp + (location_seed % 10)
        elif weather_type in ["Rainy", "Thunderstorm"]:
            temp = base_temp - 5 + (location_seed % 10)
        elif weather_type == "Snowy":
            temp = 30 + (location_seed % 10)
        else:  # Foggy
            temp = base_temp - 2 + (location_seed % 10)
        
        # Humidity based on weather type
        if weather_type in ["Rainy", "Thunderstorm", "Foggy"]:
            humidity = 70 + (location_seed % 20)  # 70-90%
        elif weather_type == "Snowy":
            humidity = 60 + (location_seed % 20)  # 60-80%
        else:
            humidity = 40 + (location_seed % 30)  # 40-70%
        
        # Wind speed based on weather type
        if weather_type in ["Thunderstorm", "Snowy"]:
            wind_speed = 10 + (location_seed % 15)  # 10-25 mph
        else:
            wind_speed = 5 + (location_seed % 10)  # 5-15 mph
        
        return {
            "location": location,
            "timestamp": datetime.now().isoformat(),
            "condition": {
                "type": weather_type,
                "description": f"{weather_type} conditions in {location}"
            },
            "temperature": {
                "fahrenheit": temp,
                "celsius": round((temp - 32) * 5/9, 1)
            },
            "humidity": humidity,
            "wind": {
                "speed": wind_speed,
                "direction": ["N", "NE", "E", "SE", "S", "SW", "W", "NW"][location_seed % 8]
            },
            "precipitation": {
                "probability": 80 if weather_type in ["Rainy", "Thunderstorm", "Snowy"] else 
                              30 if weather_type in ["Partly Cloudy", "Cloudy"] else 10,
                "type": "rain" if weather_type in ["Rainy", "Thunderstorm"] else 
                       "snow" if weather_type == "Snowy" else "none"
            },
            "source": "weather"
        }
    
    def _get_mock_forecast(self, location: str, days: int) -> Dict[str, Any]:
        """Generate mock forecast data for demo purposes"""
        # Generate a seed based on location for consistent mocks
        location_seed = sum(ord(c) for c in location)
        
        # Generate daily forecasts
        daily_forecasts = []
        
        for i in range(days):
            # Seed for this day
            day_seed = location_seed + i
            
            # Weather changes over days with some pattern
            weather_types = ["Sunny", "Partly Cloudy", "Cloudy", "Rainy", "Thunderstorm", "Snowy", "Foggy"]
            weather_index = (day_seed % len(weather_types))
            
            # Adjust for seasonality - more likely sunny in summer, etc.
            current_month = datetime.now().month
            if current_month in [6, 7, 8]:  # Summer
                if weather_index >= 4:  # Reduce chance of bad weather
                    weather_index = weather_index % 4
            elif current_month in [12, 1, 2]:  # Winter
                if weather_index == 0:  # Reduce chance of sunny
                    weather_index = 2
            
            weather_type = weather_types[weather_index]
            
            # Temperature ranges
            if weather_type == "Sunny":
                high_temp = 75 + (day_seed % 15)
                low_temp = high_temp - 15 - (day_seed % 5)
            elif weather_type in ["Partly Cloudy", "Cloudy"]:
                high_temp = 70 + (day_seed % 10)
                low_temp = high_temp - 12 - (day_seed % 5)
            elif weather_type in ["Rainy", "Thunderstorm"]:
                high_temp = 65 + (day_seed % 10)
                low_temp = high_temp - 10 - (day_seed % 5)
            elif weather_type == "Snowy":
                high_temp = 35 + (day_seed % 10)
                low_temp = high_temp - 15 - (day_seed % 8)
            else:  # Foggy
                high_temp = 60 + (day_seed % 15)
                low_temp = high_temp - 10 - (day_seed % 5)
            
            # Date for this forecast
            forecast_date = (datetime.now() + timedelta(days=i)).strftime("%Y-%m-%d")
            
            daily_forecasts.append({
                "date": forecast_date,
                "condition": weather_type,
                "temperature": {
                    "high": {
                        "fahrenheit": high_temp,
                        "celsius": round((high_temp - 32) * 5/9, 1)
                    },
                    "low": {
                        "fahrenheit": low_temp,
                        "celsius": round((low_temp - 32) * 5/9, 1)
                    }
                },
                "precipitation": {
                    "probability": 80 if weather_type in ["Rainy", "Thunderstorm", "Snowy"] else 
                                 30 if weather_type in ["Partly Cloudy", "Cloudy"] else 10,
                    "amount": round(0.5 + (day_seed % 10) / 10, 1) if weather_type in ["Rainy", "Thunderstorm"] else 
                             round(1.0 + (day_seed % 20) / 10, 1) if weather_type == "Snowy" else 0
                }
            })
        
        return {
            "location": location,
            "forecast_created": datetime.now().isoformat(),
            "daily": daily_forecasts,
            "source": "weather"
        }
    
    def _get_mock_historical_weather(self, location: str, days_ago: int) -> Dict[str, Any]:
        """Generate mock historical weather data for demo purposes"""
        # Similar implementation to forecast but for past days
        historical_data = []
        location_seed = sum(ord(c) for c in location)
        
        for i in range(days_ago, 0, -1):
            # Seed for this historical day
            day_seed = location_seed + i
            
            # Weather for this day
            weather_types = ["Sunny", "Partly Cloudy", "Cloudy", "Rainy", "Thunderstorm", "Snowy", "Foggy"]
            weather_index = (day_seed % len(weather_types))
            weather_type = weather_types[weather_index]
            
            # Date for this historical data
            hist_date = (datetime.now() - timedelta(days=i)).strftime("%Y-%m-%d")
            
            # Temperature
            avg_temp = 65 + (day_seed % 20) - 10
            
            historical_data.append({
                "date": hist_date,
                "condition": weather_type,
                "temperature": {
                    "average": {
                        "fahrenheit": avg_temp,
                        "celsius": round((avg_temp - 32) * 5/9, 1)
                    },
                    "high": {
                        "fahrenheit": avg_temp + 10,
                        "celsius": round((avg_temp + 10 - 32) * 5/9, 1)
                    },
                    "low": {
                        "fahrenheit": avg_temp - 10,
                        "celsius": round((avg_temp - 10 - 32) * 5/9, 1)
                    }
                },
                "precipitation": {
                    "amount": round(0.5 + (day_seed % 10) / 10, 1) if weather_type in ["Rainy", "Thunderstorm"] else 
                             round(1.0 + (day_seed % 20) / 10, 1) if weather_type == "Snowy" else 0
                }
            })
        
        return {
            "location": location,
            "historical_data": historical_data,
            "source": "weather"
        }
