"""
Example script demonstrating how to use the created agents on the xpander.ai platform.
"""
import os
import json
import time
import textwrap
from dotenv import load_dotenv
from xpander_sdk import XpanderClient, LLMProvider
from openai import OpenAI
from datetime import datetime

# Load environment variables from .env file
load_dotenv()

def print_box(title, content):
    """Print content in a formatted box for better visibility"""
    width = 80
    print("\n" + "=" * width)
    print(f" {title} ".center(width, "="))
    print("=" * width)
    wrapped_content = textwrap.fill(content, width=width-4) if content else "No content available"
    for line in wrapped_content.split('\n'):
        print(f"| {line.ljust(width-4)} |")
    print("=" * width + "\n")

def process_agent_task(agent, openai_client):
    """Process a task using the agent and OpenAI"""
    print_box("STARTING TASK", f"Processing task with agent: {agent.name}")
    
    # Run until the task is finished
    iteration = 0
    max_iterations = 10
    is_finished = False
    
    while not is_finished and iteration < max_iterations:
        iteration += 1
        print(f"\n--- Iteration {iteration} ---")
        
        # Get the tools formatted for OpenAI
        tools = agent.get_tools(llm_provider=LLMProvider.OPEN_AI)
        print(f"Available tools: {len(tools)}")
        
        # Get LLM response using OpenAI
        print("Sending request to OpenAI...")
        response = openai_client.chat.completions.create(
            model="gpt-4o",
            messages=agent.messages,
            tools=tools,
            tool_choice="auto",
            temperature=0
        )
        print("Received response from OpenAI")
        
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
            for idx, tc in enumerate(tool_calls):
                print(f"  {idx+1}. {tc.name}")
            
            try:
                # Run all tool calls
                results = agent.run_tools(tool_calls=tool_calls)
                
                # Log the results
                print("\nTool call results:")
                for idx, result in enumerate(results):
                    status = "✓ Success" if result.is_success else "✗ Failed"
                    print(f"  {idx+1}. {result.function_name}: {status}")
                    
                    # Check for completion signal
                    if result.function_name == "xpfinish-agent-execution-finished":
                        print("\n✓ Agent execution completed!")
                        is_finished = True
            except Exception as e:
                print(f"❌ Error executing tool calls: {str(e)}")
        else:
            print("No tool calls in this iteration")
        
        # If we haven't explicitly finished, check if we're done by other means
        if not is_finished:
            try:
                # Check if agent has finished via the is_finished method
                is_finished = agent.is_finished()
                if is_finished:
                    print("\n✓ Agent has finished processing the task")
            except Exception as e:
                print(f"❌ Error checking if agent is finished: {str(e)}")
                # Wait a bit before next iteration
                time.sleep(1)
    
    if iteration >= max_iterations:
        print("\n⚠️ Reached maximum iterations limit")
    
    # Give the agent a moment to finalize any processing
    print("\nFinalizing task processing...")
    time.sleep(3)
    
    print("\n✅ Task processing complete!")

def run_agent(agent_unloaded, xpander_client, openai_client, prompt):
    """Run a task with the specified agent"""
    print_box("AGENT INFORMATION", f"ID: {agent_unloaded.id}\nName: {agent_unloaded.name}")
    
    # Load the agent to get full functionality
    agent = xpander_client.agents.get(agent_id=agent_unloaded.id)
    print("✓ Agent loaded successfully")
    
    # Create a task for the agent
    agent.add_task(input=prompt)
    print(f"✓ Task created: {prompt[:50]}...")
    
    try:
        # Process the task using the agent
        process_agent_task(agent, openai_client)
        
        # Get the result
        try:
            print("\nRetrieving execution result...")
            result = agent.retrieve_execution_result()
            
            if result:
                if hasattr(result, 'status'):
                    print(f"Execution status: {result.status}")
                
                if hasattr(result, 'status') and result.status == "COMPLETED":
                    if hasattr(result, 'result'):
                        print_box("TASK RESULT", result.result)
                    else:
                        print("❌ Result object has no 'result' attribute")
                    
                    if hasattr(result, 'thread_id'):
                        print(f"\nThread ID for future reference: {result.thread_id}")
                else:
                    print("⚠️ Task did not complete successfully")
            else:
                print("❌ No result returned from retrieve_execution_result()")
        except Exception as e:
            print(f"❌ Error retrieving result: {str(e)}")
    except Exception as e:
        print(f"❌ Error processing agent task: {str(e)}")

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
    
    # Run the News & Market Analysis Agent
    if news_agent_unloaded:
        print_box("USING NEWS AGENT", "Starting News & Market Analysis Agent execution")
        run_agent(
            news_agent_unloaded, 
            xpander_client, 
            openai_client,
            "What are the top tech news stories today and how might they impact the market?"
        )
    else:
        print("❌ News & Market Analysis Agent not found. Run create_agents.py first.")
    
    # Run the Zillow Real Estate Agent
    if zillow_agent_unloaded:
        print_box("USING ZILLOW AGENT", "Starting Zillow Real Estate Agent execution")
        run_agent(
            zillow_agent_unloaded, 
            xpander_client, 
            openai_client,
            "Find properties in Seattle with 3+ bedrooms under $1M and analyze their investment potential."
        )
    else:
        print("❌ Zillow Real Estate Agent not found. Run create_agents.py first.")

if __name__ == "__main__":
    main()
