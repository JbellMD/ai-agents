# Zillow Real Estate Agent

This agent integrates Zillow real estate data with weather information to provide comprehensive property analysis, personalized recommendations, and investment insights.

## Features

- **Property Search**: Find properties based on location and detailed filters
- **Personalized Recommendations**: Get property recommendations based on your preferences
- **Investment Analysis**: Evaluate properties for their investment potential
- **Weather Integration**: Enhance property recommendations with weather context
- **Property Comparison**: Side-by-side comparison of multiple properties
- **Market Trends**: Track real estate market trends for specific locations

## Architecture

The agent is organized into three main components:

1. **Interfaces**: Connectors to external data sources
   - `zillow_interface.py`: Connects to Zillow API for real estate data
   - `weather_interface.py`: Connects to Weather API for location weather data

2. **Processors**: Business logic for data analysis
   - `property_processor.py`: Analyzes property data and generates insights

3. **Main Application**: Core agent functionality
   - `main.py`: Provides the agent's main capabilities and CLI

## Usage

### Installation

```bash
# Clone the repository
cd ai-agents/zillow-agent

# Install dependencies
pip install -r requirements.txt

# Set up environment variables (for API keys)
# Create a .env file with your API keys:
# ZILLOW_API_KEY=your_api_key
# WEATHER_API_KEY=your_api_key
```

### Running the Agent

The agent can be run in several modes:

#### Search for Properties

```bash
python src/main.py search "San Francisco, CA" --min_price 500000 --max_price 1000000 --bedrooms 2
```

#### Get Property Recommendations

```bash
python src/main.py recommend "New York, NY" --min_price 800000 --max_price 1500000 --bedrooms 3 --bathrooms 2 --property_type "Condo"
```

#### Analyze Investment Properties

```bash
python src/main.py invest "Austin, TX" --min_price 300000 --max_price 700000
```

#### Get Detailed Property Information

```bash
python src/main.py details property-austin-tx-5
```

#### Compare Multiple Properties

```bash
python src/main.py compare property-austin-tx-5 property-austin-tx-7 property-austin-tx-9
```

## Example Output

The agent generates JSON reports in the specified output directory (default: `reports/`). Each report includes:

- Property listings with detailed information
- Market trends and analysis
- Weather data and its impact on property viewing
- Investment metrics (for investment analysis)
- Comparative metrics (for property comparisons)

## Adapting for xpander.ai Platform

This agent is designed to work with the xpander.ai Agent Platform by leveraging the following interfaces:

- Zillow (Ready)
- Weather (Ready)

The agent's architecture allows for easy integration with the platform's Action Graphs for creating complex workflows.

## Notes on Implementation

This implementation includes mock data for demonstration purposes. In a production environment, you would replace these mock implementations with real API calls to Zillow and weather services.

## Future Enhancements

1. Integration with mortgage calculators for financing options
2. Neighborhood safety and school quality analysis
3. Commute time estimations to key locations
4. Historical price trend visualization
5. Predictive analytics for future property values
6. Natural language processing for conversational property search
