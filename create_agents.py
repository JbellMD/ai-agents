"""
Script to create and configure agents on the xpander.ai platform using the SDK.
"""
import os
from dotenv import load_dotenv
from xpander_sdk import XpanderClient, LLMProvider

# Load environment variables from .env file
load_dotenv()

def main():
    # Initialize the client with your API key
    api_key = os.environ.get("XPANDER_API_KEY", "your-xpander-api-key")
    client = XpanderClient(api_key=api_key)
    
    print("Connected to xpander.ai platform")
    
    # Create News & Market Analysis Agent
    print("\nCreating News & Market Analysis Agent...")
    try:
        # Create the agent with minimal parameters
        news_agent = client.agents.create(
            name="News & Market Analysis Agent"
        )
        print(f"Created agent: {news_agent.name} with ID: {news_agent.id}")
        
        # After creation, set the instructions
        news_agent.instructions.general = "You are a News & Market Analysis Agent that integrates data from multiple sources."
        news_agent.instructions.goal = "Provide comprehensive analysis of news events and their correlation with market movements."
        news_agent.instructions.role = "Analyze news from HackerNews, Reddit, and other sources, correlate with market data, and generate insights."
        news_agent.update()
        
        # Retrieve available interfaces
        interfaces = news_agent.retrieve_agentic_interfaces()
        
        # Find and attach required interfaces
        required_interfaces = ["HackerNews", "Reddit", "Firecrawl", "Market Insights", "Company Monitor"]
        for interface_name in required_interfaces:
            interface = next((i for i in interfaces if interface_name.lower() in i.name.lower()), None)
            if interface:
                print(f"Found interface: {interface.name}")
                # Retrieve operations from this interface
                operations = news_agent.retrieve_agentic_operations(agentic_interface=interface)
                # Attach operations to the agent
                if operations:
                    news_agent.attach_operations(operations=operations)
                    print(f"Attached {len(operations)} operations from {interface.name}")
        
        # Sync changes to the agent
        news_agent.sync()
        
    except Exception as e:
        print(f"Error creating News & Market Analysis Agent: {e}")
    
    # Create Zillow Real Estate Agent
    print("\nCreating Zillow Real Estate Agent...")
    try:
        # Create the agent with minimal parameters
        zillow_agent = client.agents.create(
            name="Zillow Real Estate Agent"
        )
        print(f"Created agent: {zillow_agent.name} with ID: {zillow_agent.id}")
        
        # After creation, set the instructions
        zillow_agent.instructions.general = "You are a Zillow Real Estate Agent that combines property data with weather information."
        zillow_agent.instructions.goal = "Help users find properties that match their criteria and provide analysis on investment potential."
        zillow_agent.instructions.role = "Search for properties, analyze investment potential, and provide recommendations based on weather and market data."
        zillow_agent.update()
        
        # Retrieve available interfaces
        interfaces = zillow_agent.retrieve_agentic_interfaces()
        
        # Find and attach required interfaces
        required_interfaces = ["Zillow", "Weather"]
        for interface_name in required_interfaces:
            interface = next((i for i in interfaces if interface_name.lower() in i.name.lower()), None)
            if interface:
                print(f"Found interface: {interface.name}")
                # Retrieve operations from this interface
                operations = zillow_agent.retrieve_agentic_operations(agentic_interface=interface)
                # Attach operations to the agent
                if operations:
                    zillow_agent.attach_operations(operations=operations)
                    print(f"Attached {len(operations)} operations from {interface.name}")
        
        # Sync changes to the agent
        zillow_agent.sync()
        
    except Exception as e:
        print(f"Error creating Zillow Real Estate Agent: {e}")
    
    print("\nSetup complete! You can now use these agents through the xpander.ai platform.")

if __name__ == "__main__":
    main()
