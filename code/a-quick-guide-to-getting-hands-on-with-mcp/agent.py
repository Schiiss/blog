import asyncio
import os
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent
from langchain.chat_models import init_chat_model
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def extract_final_tool_message(response_dict):
    """
    Extracts the final tool message content from the agent response dict.
    Returns the string content if found, else None.
    """
    try:
        messages = response_dict.get('messages', [])
        # Look for the last ToolMessage or AIMessage with content
        for msg in reversed(messages):
            # ToolMessage: has 'content' and 'name'
            if msg.__class__.__name__ == 'ToolMessage' and hasattr(msg, 'content'):
                return msg.content
            # AIMessage: has 'content' and not empty
            if msg.__class__.__name__ == 'AIMessage' and getattr(msg, 'content', None):
                return msg.content
    except Exception as e:
        return f"[Error extracting message: {e}]"
    return None

async def main():
    model = init_chat_model(
        model=os.getenv("AZURE_OPENAI_MODEL"),
        model_provider="azure_openai",
        temperature=0,    
        api_key=os.getenv("AZURE_OPENAI_API_KEY"),
        azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
        api_version=os.getenv("AZURE_OPENAI_API_VERSION")
    )

    client = MultiServerMCPClient(
        {
            "math": {
                # Ensure you start your weather server on port 8000
                "url": "http://localhost:8000/mcp",
                "transport": "streamable_http",
            }
        }
    )
    tools = await client.get_tools()
    agent = create_react_agent(
        model,
        tools
    )
    # Ask for BTC price
    crypto_response = await agent.ainvoke(
        {"messages": [{"role": "user", "content": "get me crypto prices for BTC"}]}
    )
    print("Crypto BTC:", extract_final_tool_message(crypto_response))

    # Ask for weather in London
    weather_response = await agent.ainvoke(
        {"messages": [{"role": "user", "content": "what's the weather in London?"}]}
    )
    print("Weather:", extract_final_tool_message(weather_response))

    # Ask for a random joke
    joke_response = await agent.ainvoke(
        {"messages": [{"role": "user", "content": "tell me a joke"}]}
    )
    print("Joke:", extract_final_tool_message(joke_response))

    # Ask for ETH price
    eth_response = await agent.ainvoke(
        {"messages": [{"role": "user", "content": "get me crypto prices for ETH"}]}
    )
    print("Crypto ETH:", extract_final_tool_message(eth_response))

    # Ask for a quote
    quote_response = await agent.ainvoke(
        {"messages": [{"role": "user", "content": "give me an inspirational quote"}]}
    )
    print("Quote:", extract_final_tool_message(quote_response))


if __name__ == "__main__":
    asyncio.run(main())