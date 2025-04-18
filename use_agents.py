"""
Example script demonstrating how to use the created agents on the xpander.ai platform.
"""
import os
import json
from dotenv import load_dotenv
from xpander_sdk import XpanderClient, LLMProvider, ToolCall, ToolCallType, ToolCallResult
from openai import OpenAI
from datetime import datetime

# Load environment variables from .env file
load_dotenv()

# Define local tool function outside the main function
def track_company(params):
    """Local tool function for tracking analyzed companies"""
    ticker = params.get('ticker', 'UNKNOWN')
    name = params.get('name', 'Unknown Company')
    sector = params.get('sector', 'Unknown')
    importance = params.get('importance', 3)
    
    print(f"TRACKING COMPANY: {name} ({ticker}) - Sector: {sector}, Importance: {importance}/5")
    
    # In a real implementation, you might save this to a database or file
    tracked_companies_file = 'tracked_companies.json'
    
    try:
        # Load existing tracked companies
        if os.path.exists(tracked_companies_file):
            with open(tracked_companies_file, 'r') as f:
                tracked_companies = json.load(f)
        else:
            tracked_companies = []
        
        # Add the new company
        tracked_companies.append({
            'ticker': ticker,
            'name': name,
            'sector': sector,
            'importance': importance,
            'tracked_at': datetime.now().isoformat()
        })
        
        # Save the updated list
        with open(tracked_companies_file, 'w') as f:
            json.dump(tracked_companies, f, indent=2)
        
        return f"Successfully tracked {name} ({ticker}) with importance level {importance}/5"
    except Exception as e:
        return f"Error tracking company: {str(e)}"

def process_agent_task(agent, openai_client):
    """Process a task using the agent and OpenAI"""
    print("Processing task...")
    
    # Run until the task is finished
    iteration = 0
    while not agent.is_finished():
        iteration += 1
        print(f"\nIteration {iteration}:")
        
        # Get the tools formatted for OpenAI
        tools = agent.get_tools(llm_provider=LLMProvider.OPEN_AI)
        print(f"Available tools: {len(tools)}")
        
        # Get LLM response using OpenAI
        response = openai_client.chat.completions.create(
            model="gpt-4o",
            messages=agent.messages,
            tools=tools,
            tool_choice="auto",
            temperature=0
        )
        
        # Add the response to the agent's messages
        agent.add_messages(response.model_dump())
        
        # Extract tool calls from the response
        tool_calls = XpanderClient.extract_tool_calls(
            llm_response=response.model_dump(),
            llm_provider=LLMProvider.OPEN_AI
        )
        
        # Execute any tool calls
        if tool_calls:
            print(f"Executing {len(tool_calls)} tool calls:")
            for tc in tool_calls:
                print(f"  - {tc.name} (Type: {tc.type})")
            
            # Filter local tool calls if needed
            local_tool_calls = XpanderClient.retrieve_pending_local_tool_calls(tool_calls=tool_calls)
            
            # Handle any local tool calls separately (if needed)
            if local_tool_calls:
                print(f"  - Processing {len(local_tool_calls)} local tool calls")
                
                # In a more complex implementation, you might handle these differently
                # Here we're letting the agent.run_tools handle both local and remote tools
            
            # Run all tool calls - both XPANDER and LOCAL types
            results = agent.run_tools(tool_calls=tool_calls)
            
            # Log the results
            for result in results:
                status = "✓ Success" if result.is_success else "✗ Failed"
                print(f"  - {result.function_name}: {status}")
                if not result.is_success and result.error:
                    print(f"    Error: {result.error}")
        else:
            print("No tool calls in this iteration")
        
        # Get the current status
        status = agent.get_execution_status()
        print(f"Task status: {status.status}")
    
    print("Task processing complete!")

def main():
    # Initialize clients
    xpander_api_key = os.environ.get("XPANDER_API_KEY", "your-xpander-api-key")
    openai_api_key = os.environ.get("OPENAI_API_KEY", "your-openai-api-key")
    
    xpander_client = XpanderClient(api_key=xpander_api_key)
    openai_client = OpenAI(api_key=openai_api_key)
    
    # List available agents
    agents = xpander_client.agents.list()
    print(f"Found {len(agents)} agents")
    
    # Find our agents by name
    news_agent_unloaded = next((a for a in agents if "news & market" in a.name.lower()), None)
    zillow_agent_unloaded = next((a for a in agents if "zillow" in a.name.lower()), None)
    
    if news_agent_unloaded:
        print(f"\n--- Using News & Market Analysis Agent ({news_agent_unloaded.id}) ---")
        
        # Load the agent to get full functionality
        news_agent = xpander_client.agents.get(agent_id=news_agent_unloaded.id)
        print("Agent loaded successfully")
        
        # Add custom local tool for tracking analyzed companies
        news_agent.add_local_tools([
            {
                "name": "track_analyzed_company",
                "description": "Track a company that was analyzed for follow-up",
                "function": track_company,
                "parameters": {
                    "type": "object",
                    "properties": {
                        "ticker": {
                            "type": "string",
                            "description": "Company ticker symbol"
                        },
                        "name": {
                            "type": "string",
                            "description": "Company name"
                        },
                        "sector": {
                            "type": "string",
                            "description": "Company sector"
                        },
                        "importance": {
                            "type": "integer",
                            "description": "Importance level (1-5)"
                        }
                    },
                    "required": ["ticker", "name"]
                }
            }
        ])
        
        # Create a task for the news agent
        news_agent.add_task(input="What are the top tech news stories today and how might they impact the market? If you identify any key companies, please track them.")
        
        # Process the task using the agent
        process_agent_task(news_agent, openai_client)
        
        # Get the result
        result = news_agent.retrieve_execution_result()
        if result and hasattr(result, 'status') and result.status == "COMPLETED":
            print("\nTask Result:")
            print(result.result)
            if hasattr(result, 'thread_id'):
                print(f"\nThread ID for future reference: {result.thread_id}")
    else:
        print("News & Market Analysis Agent not found. Run create_agents.py first.")
    
    if zillow_agent_unloaded:
        print(f"\n--- Using Zillow Real Estate Agent ({zillow_agent_unloaded.id}) ---")
        
        # Load the agent to get full functionality
        zillow_agent = xpander_client.agents.get(agent_id=zillow_agent_unloaded.id)
        print("Agent loaded successfully")
        
        # Create a task for the Zillow agent
        zillow_agent.add_task(input="Find properties in Seattle with 3+ bedrooms under $1M and analyze their investment potential.")
        
        # Process the task using the agent
        process_agent_task(zillow_agent, openai_client)
        
        # Get the result
        result = zillow_agent.retrieve_execution_result()
        if result and hasattr(result, 'status') and result.status == "COMPLETED":
            print("\nTask Result:")
            print(result.result)
            if hasattr(result, 'thread_id'):
                print(f"\nThread ID for future reference: {result.thread_id}")
    else:
        print("Zillow Real Estate Agent not found. Run create_agents.py first.")

if __name__ == "__main__":
    main()
