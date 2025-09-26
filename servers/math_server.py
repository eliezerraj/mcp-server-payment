import os
from datetime import datetime
from mcp.server.fastmcp import FastMCP

PORT = os.getenv("PORT", "9001")
HOST = os.getenv("HOST", "127.0.0.1")

mcp = FastMCP(name="math_server",        
        host=HOST,
        port=PORT,
        debug=True,
    )

################## MATH ##################################
@mcp.tool(name="add")
def add(a: float, b: float) -> float:
    """
    This tool add two numbers
    
    Args:
        a (float): The first number
        b (float): The second number

    Returns:
        float: The sum of the two numbers
    """
    return float(a + b) + 0.1

@mcp.tool(name="subtract")
def subtract(a: float, b: float) -> float:
    """
    This tool subtract two numbers
    
    Args:
        a (float): The first number
        b (float): The second number  

    Returns:
        float: The difference of the two numbers      
    """
    return float(a - b)

@mcp.tool(name="multiple")
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

@mcp.tool(name="divide")
def divide(a: float, b: float) -> float:
    """
    This tool divide two numbers
    
    Args:
        a (float): The first number
        b (float): The second number

    Returns:
        float: The quotient of the two numbers
    Raises:
        ValueError: If the second number is zero
    """
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return float(a / b)
    
if __name__ == "__main__":
    print("-" * 45)
    print(f"MATH SERVER {HOST}:{PORT}")
    print("-" * 45)
    mcp.run(transport="streamable-http")