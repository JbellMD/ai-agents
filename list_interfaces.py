"""
Script to list all available interfaces and operations on the xpander.ai platform.
"""
import os
import json
from dotenv import load_dotenv
from xpander_sdk import XpanderClient

# Load environment variables from .env file
load_dotenv()

def main():
    # Initialize the client with your API key
    api_key = os.environ.get("XPANDER_API_KEY", "your-xpander-api-key")
    client = XpanderClient(api_key=api_key)
    
    print("Connected to xpander.ai platform\n")
    
    # List all available agents
    agents = client.agents.list()
    print(f"Found {len(agents)} agents")
    
    # Find Zillow agent specifically
    zillow_agent_unloaded = next((a for a in agents if "zillow" in a.name.lower()), None)
    
    if not zillow_agent_unloaded:
        print("Zillow agent not found. Please run create_agents.py first.")
        return
        
    print(f"Loading Zillow agent: {zillow_agent_unloaded.id}")
    zillow_agent = client.agents.get(agent_id=zillow_agent_unloaded.id)
    print("Agent loaded successfully\n")
    
    # List all available interfaces
    print("Retrieving available interfaces...\n")
    interfaces = zillow_agent.retrieve_agentic_interfaces()
    print(f"Found {len(interfaces)} interfaces")
    
    # Create a directory to save interface details
    os.makedirs("interface_details", exist_ok=True)
    
    # Print and save detailed information about each interface
    for interface in interfaces:
        print(f"\n{'=' * 80}")
        print(f"INTERFACE: {interface.name} (ID: {interface.id})")
        print(f"{'=' * 80}")
        
        # Retrieve operations for this interface
        operations = zillow_agent.retrieve_agentic_operations(agentic_interface=interface)
        print(f"Found {len(operations)} operations")
        
        # Print and save details about each operation
        operations_data = []
        for op in operations:
            print(f"\n- {op.name}")
            if hasattr(op, 'description') and op.description:
                print(f"  Description: {op.description}")
            
            # Get operation details
            op_details = {}
            op_details["name"] = op.name
            op_details["id"] = op.id
            op_details["description"] = op.description if hasattr(op, 'description') else ""
            
            # Get parameters if available
            if hasattr(op, 'parameters'):
                op_details["parameters"] = op.parameters
                print(f"  Parameters: {json.dumps(op.parameters, indent=2)}")
            
            operations_data.append(op_details)
        
        # Save operations data to a file
        filename = f"interface_details/{interface.name.replace(' ', '_').lower()}.json"
        with open(filename, 'w') as f:
            json.dump(operations_data, f, indent=2)
        print(f"\nSaved details to {filename}")
    
    print("\nAll interface details have been saved to the 'interface_details' directory.")

if __name__ == "__main__":
    main()
