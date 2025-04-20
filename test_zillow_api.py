"""
Script to test Zillow API operations directly to troubleshoot issues.
"""
import os
import json
from dotenv import load_dotenv
from xpander_sdk import XpanderClient, ToolCall, ToolCallType

# Load environment variables from .env file
load_dotenv()

def main():
    # Initialize the client with your API key
    api_key = os.environ.get("XPANDER_API_KEY", "your-xpander-api-key")
    client = XpanderClient(api_key=api_key)
    
    print("Connected to xpander.ai platform\n")
    
    # Find the Zillow agent
    agents = client.agents.list()
    zillow_agent_unloaded = next((a for a in agents if "zillow" in a.name.lower()), None)
    
    if not zillow_agent_unloaded:
        print("Zillow agent not found. Please run create_agents.py first.")
        return
        
    print(f"Loading Zillow agent: {zillow_agent_unloaded.id}")
    zillow_agent = client.agents.get(agent_id=zillow_agent_unloaded.id)
    print("Agent loaded successfully\n")
    
    # Test 1: First, get location suggestions for Seattle
    print("\n=== TEST 1: Get Location Suggestions ===")
    location_tool_call = ToolCall(
        name="Provide Location Suggestions",
        type=ToolCallType.XPANDER,
        payload={
            "bodyParams": {
                "q": "Seattle, WA"
            }
        },
        tool_call_id="test_call_1"
    )
    
    try:
        location_result = zillow_agent.run_tool(tool=location_tool_call)
        print(f"Success: {location_result.is_success}")
        if location_result.is_success:
            print("Location suggestions:")
            location_data = json.loads(location_result.result)
            print(json.dumps(location_data, indent=2))
            
            # Extract location data for next step
            # Typically would be something like a region_id or similar from the result
            location_id = None
            if location_data and isinstance(location_data, list) and len(location_data) > 0:
                location_item = location_data[0]
                if "metaData" in location_item and "regionId" in location_item["metaData"]:
                    location_id = location_item["metaData"]["regionId"]
                    print(f"Found region ID: {location_id}")
    except Exception as e:
        print(f"Error getting location suggestions: {str(e)}")
        location_id = None
    
    # Test 2: Create a Zillow search URL with correct parameter format
    print("\n=== TEST 2: Create Zillow Search URL ===")
    search_url_tool_call = ToolCall(
        name="Create Zillow Search URL",
        type=ToolCallType.XPANDER,
        payload={
            "queryParams": {
                "location": "Seattle, WA",
                "home_type": "apartment",  # lowercase is important
                "beds": 2,
                "price_max": 800000
            },
            "bodyParams": {}
        },
        tool_call_id="test_call_2"
    )
    
    try:
        url_result = zillow_agent.run_tool(tool=search_url_tool_call)
        print(f"Success: {url_result.is_success}")
        if url_result.is_success:
            print(f"Search URL: {url_result.result}")
        else:
            print(f"Error creating URL: {url_result}")
            
        # Try alternative format if first attempt fails
        if not url_result.is_success or not url_result.result or url_result.result == '':
            print("\nTrying alternative parameter format...")
            alt_search_url_tool_call = ToolCall(
                name="Create Zillow Search URL",
                type=ToolCallType.XPANDER,
                payload={
                    "bodyParams": {
                        "location": "Seattle, WA",
                        "home_type": "apartment",
                        "beds": 2,
                        "price_max": 800000
                    }
                },
                tool_call_id="test_call_2b"
            )
            
            alt_url_result = zillow_agent.run_tool(tool=alt_search_url_tool_call)
            print(f"Alternative Success: {alt_url_result.is_success}")
            if alt_url_result.is_success:
                print(f"Alternative Search URL: {alt_url_result.result}")
    except Exception as e:
        print(f"Error creating search URL: {str(e)}")
    
    # Test 3: Use minimal parameters (just location) as last resort
    print("\n=== TEST 3: Create Zillow Search URL (Minimal) ===")
    minimal_url_tool_call = ToolCall(
        name="Create Zillow Search URL",
        type=ToolCallType.XPANDER,
        payload={
            "queryParams": {
                "location": "Seattle, WA"
            },
            "bodyParams": {}
        },
        tool_call_id="test_call_3"
    )
    
    try:
        minimal_result = zillow_agent.run_tool(tool=minimal_url_tool_call)
        print(f"Success: {minimal_result.is_success}")
        if minimal_result.is_success:
            print(f"Minimal Search URL: {minimal_result.result}")
    except Exception as e:
        print(f"Error creating minimal search URL: {str(e)}")
    
    print("\nTesting complete!")

if __name__ == "__main__":
    main()
