"""
Example script demonstrating how to use the created agents on the xpander.ai platform.
"""
import os
from xpander_sdk import XpanderClient, LLMProvider
from openai import OpenAI

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
    news_agent = next((a for a in agents if "news & market" in a.name.lower()), None)
    zillow_agent = next((a for a in agents if "zillow" in a.name.lower()), None)
    
    if news_agent:
        print(f"\n--- Using News & Market Analysis Agent ({news_agent.id}) ---")
        
        # Create a task for the news agent
        news_agent.add_task(input="What are the top tech news stories today and how might they impact the market?")
        
        # Process the task using the agent
        process_agent_task(news_agent, openai_client)
        
        # Get the result
        result = news_agent.retrieve_execution_result()
        if result.status == "COMPLETED":
            print("\nTask Result:")
            print(result.result)
    else:
        print("News & Market Analysis Agent not found. Run create_agents.py first.")
    
    if zillow_agent:
        print(f"\n--- Using Zillow Real Estate Agent ({zillow_agent.id}) ---")
        
        # Create a task for the Zillow agent
        zillow_agent.add_task(input="Find properties in Seattle with 3+ bedrooms under $1M and analyze their investment potential.")
        
        # Process the task using the agent
        process_agent_task(zillow_agent, openai_client)
        
        # Get the result
        result = zillow_agent.retrieve_execution_result()
        if result.status == "COMPLETED":
            print("\nTask Result:")
            print(result.result)
    else:
        print("Zillow Real Estate Agent not found. Run create_agents.py first.")

def process_agent_task(agent, openai_client):
    """Process a task using the agent and OpenAI"""
    print("Processing task...")
    
    # Run until the task is finished
    while not agent.is_finished():
        # Get LLM response using OpenAI
        response = openai_client.chat.completions.create(
            model="gpt-4o",
            messages=agent.messages,
            tools=agent.get_tools(llm_provider=LLMProvider.OPEN_AI),
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
            print(f"Executing {len(tool_calls)} tool calls...")
            agent.run_tools(tool_calls=tool_calls)
        
        # Get the current status
        status = agent.get_execution_status()
        print(f"Task status: {status.status}")
    
    print("Task processing complete!")

if __name__ == "__main__":
    main()
