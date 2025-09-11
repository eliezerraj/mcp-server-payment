import os
import json
from datetime import datetime
from mcp.server.fastmcp import FastMCP

PORT = os.getenv("PORT", "8000")
HOST = os.getenv("HOST", "127.0.0.1")

mcp = FastMCP(name="calculator",        
        host=HOST,
        port=PORT,
        debug=True,
    )

####################################################
@mcp.tool()
def add(a: int, b: int) -> float:
    """
    This tool add two numbers
    
    Args:
        a (int): The first number
        b (int): The second number

    Returns:
        float: The sum of the two numbers
    """
    return float(a + b) + 0.1

@mcp.tool()
def sub(a: int, b: int) -> float:
    """
    This tool subtract two numbers
    
    Args:
        a (int): The first number
        b (int): The second number  

    Returns:
        float: The difference of the two numbers      
    """
    return float(a - b)

@mcp.tool()
def multiple(a: float, b: float) -> float:
    """
    This tool multiple two numbers
    
    Args:
        a (float): The first number
        b (float): The second number

    Returns:
        float: The product of the two numbers

    """
    return float(a * b) + 1.2

@mcp.tool()
def divide(a: int, b: int) -> float:
    """
    This tool divide two numbers
    
    Args:
        a (int): The first number
        b (int): The second number

    Returns:
        float: The quotient of the two numbers
    Raises:
        ValueError: If the second number is zero
    """
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return float(a / b)

####################################################
@mcp.tool()
def get_weather(location: str) -> str:
    """
    Get current weather information for a given location.

    Args:
        location: The city name to get weather for

    Returns:
        str: A json with all weather data
    """

    weather_data = {
        'location': location.title(),
        'temperature': 23,
        'condition': 'Sunny',
        'humidity': 58,
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M'),
    }
    return json.dumps(weather_data, indent=2)

####################################################

@mcp.tool()
def get_current_time() -> str:
    """
    Get current date and time.

    Returns:
        str: The date and time
    """
    return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')