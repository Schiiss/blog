from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Weather & More")

@mcp.tool()
async def get_weather(location: str) -> str:
    """Get weather for location."""
    # Pretend to call a weather API
    if location.lower() == "new york":
        return "It's always sunny in New York."
    return f"Mocked weather for {location}: 72°F, partly cloudy."

@mcp.tool()
async def get_joke() -> str:
    """Get a random joke (mocked)."""
    # Pretend to call an open jokes API
    return "Why did the developer go broke? Because he used up all his cache!"

@mcp.tool()
async def get_crypto_price(symbol: str) -> str:
    """Get the current price of a cryptocurrency (mocked)."""
    # Pretend to call a crypto price API
    prices = {"BTC": "$67,000", "ETH": "$3,500", "DOGE": "$0.12"}
    price = prices.get(symbol.upper(), "$???")
    return f"The current price of {symbol.upper()} is {price}. (mocked)"

@mcp.tool()
async def get_quote() -> str:
    """Get a random inspirational quote (mocked)."""
    # Pretend to call a quotes API
    return "The best way to get started is to quit talking and begin doing. – Walt Disney"

if __name__ == "__main__":
    mcp.run(transport="streamable-http")