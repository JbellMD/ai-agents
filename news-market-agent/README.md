# News & Market Analysis Agent

This agent integrates data from multiple sources (HackerNews, Reddit, Firecrawl, Market Insights, Company Monitor) to provide comprehensive analysis of news and market trends with actionable insights.

## Features

- **Multi-Source News Aggregation**: Collects and consolidates news from HackerNews and Reddit
- **Content Enrichment**: Expands news content with related articles via Firecrawl
- **Market Analysis**: Monitors market trends, sector performance, and economic indicators
- **Company Tracking**: Follows specific companies mentioned in news stories
- **Correlation Analysis**: Identifies relationships between news events and market movements
- **Automated Reporting**: Generates comprehensive daily digests and specific analyses
- **Sentiment Analysis**: Analyzes the sentiment of news content to gauge market mood

## Architecture

The agent is organized into three main components:

1. **Interfaces**: Connectors to external data sources
   - `hackernews_interface.py`: Connects to HackerNews API
   - `reddit_interface.py`: Connects to Reddit API
   - `firecrawl_interface.py`: Connects to Firecrawl service
   - `market_insights_interface.py`: Connects to market data
   - `company_monitor_interface.py`: Monitors company information

2. **Processors**: Business logic for data analysis
   - `news_processor.py`: Processes and correlates news from multiple sources
   - `market_processor.py`: Analyzes market data and relates it to news

3. **Reports**: Output generation
   - `report_generator.py`: Creates structured reports and insights

## Usage

### Installation

```bash
# Clone the repository
cd ai-agents/news-market-agent

# Install dependencies
pip install -r requirements.txt

# Set up environment variables (for API keys)
# Create a .env file with your API keys:
# REDDIT_CLIENT_ID=your_client_id
# REDDIT_CLIENT_SECRET=your_client_secret
# FIRECRAWL_API_KEY=your_api_key
# MARKET_INSIGHTS_API_KEY=your_api_key
# COMPANY_MONITOR_API_KEY=your_api_key
```

### Running the Agent

The agent can be run in several modes:

#### Generate a Daily Digest

```bash
python src/main.py daily
```

Optional parameters:
- `--topics`: Filter news by specific topics (e.g., "ai", "crypto")
- `--output`: Specify output directory for reports

#### Generate Company Analysis

```bash
python src/main.py company AAPL
```

Replace `AAPL` with any stock ticker symbol.

#### Generate Sector Analysis

```bash
python src/main.py sector Technology
```

Replace `Technology` with any market sector.

#### Schedule Daily Digest

```bash
python src/main.py schedule --hour 8 --minute 0
```

This will schedule the daily digest to run at 8:00 AM every day.

## Example Output

The agent generates JSON reports in the specified output directory (default: `reports/`). Each report includes:

- Market summary with key indices and trends
- Top news stories with sentiment analysis
- Sector performance analysis
- Company mentions and correlations
- Actionable insights based on news and market correlation

## Adapting for xpander.ai Platform

This agent is designed to work with the xpander.ai Agent Platform by leveraging the following interfaces:

- HackerNews (Ready)
- Reddit (Ready)
- Firecrawl (Ready)
- Market Insights (Ready)
- Company monitor (Ready)

The agent's modular architecture allows for easy integration with the platform's Action Graphs for creating complex workflows.

## Notes on Implementation

This implementation includes mock data for demonstration purposes. In a production environment, you would replace these mock implementations with real API calls to the respective services.

## Future Enhancements

1. Integration with trading platforms for automated trading signals
2. Advanced NLP for better entity extraction and relationship mapping
3. Customizable alerting system for significant market events
4. Historical analysis and trend prediction
5. Portfolio-specific impact analysis
