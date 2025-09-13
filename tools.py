import os
import json
import aiohttp
from datetime import datetime
from mcp.server.fastmcp import FastMCP

PORT = os.getenv("PORT", "8000")
HOST = os.getenv("HOST", "127.0.0.1")

mcp = FastMCP(name="calculator",        
        host=HOST,
        port=PORT,
        debug=True,
    )

################## MATH ##################################
@mcp.tool()
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

@mcp.tool()
def sub(a: float, b: float) -> float:
    """
    This tool subtract two numbers
    
    Args:
        a (float): The first number
        b (float): The second number  

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

################### WEATHER #################################
@mcp.tool()
def get_weather(location: str) -> str:
    """
    Get current weather information for a given location.

    Example: What is the wheater in Sao Paulo ?

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

###################### TIME ##############################

@mcp.tool()
def get_current_time() -> str:
    """
    Get current date and time.

    Example: What time is it?

    Returns:
        str: The date and time
    """

    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')

######################## SAVE ###########################

@mcp.tool()
def save_note(filename: str, content: str) -> str:
    """
    Save a text note for the user to a file.
    Example: Save a note called to file 'my_list' with my itens: dogs, cats, and birds 

    Args:
        filename: Name of the file to save (without extension)
        content: The text content to save
    Raises:
        ValueError: If the file cannot be saved
    """
    try:
        filepath = f'notes/{filename}.txt'
        os.makedirs('notes', exist_ok=True)

        with open(filepath, 'w') as f:
            f.write(f'Note saved at {datetime.now()}\n')
            f.write('-' * 40 + '\n')
            f.write(content)

        return f'Note saved successfully to {filepath}'
    except Exception as e:
        return f'Error saving note: {str(e)}'
    
    ####################################################

@mcp.tool()
async def get_account(account: str) -> str:
    """
    Get account details from a endpoint via rest call api

    Example: https://go-global-apex.architecture.caradhras.io/account/get/ACC-500

    Args:
        account: Account Identificator
    Raises:
        ValueError: http status code
    """
    headers = {"Authorization": "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl91c2UiOiJhY2Nlc3MiLCJpc3MiOiJnby1vYXV0aC1sYW1iZGEiLCJ2ZXJzaW9uIjoiMi4xIiwiand0X2lkIjoiY2VjZDU0OWYtYmMxMC00YzRmLWIxMWItMWEwZjZhMjA0ODQzIiwidXNlcm5hbWUiOiJ1c2VyLTAzIiwidGllciI6InRpZXItMDMiLCJhcGlfYWNjZXNzX2tleSI6IkFQSV9BQ0NFU1NfS0VZX1VTRVJfMDMiLCJzY29wZSI6WyJ0ZXN0LnJlYWQiLCJ0ZXN0LndyaXRlIiwiYWRtaW4iXSwiZXhwIjoxNzU3Nzg4OTYwfQ.LVUB3K3UXrVggvt8rkT_1ipIAj_jQReAJYKAdhLZk1m2a-S9gkF2FyH0N3qe6zRmbedBXsj33jKxF2UHmDdLZ1-M9Z0ar43I9JUGfXN2emoUWkjCb0xxFfmiEJ7ddEqIOOmNOGqHdxMWnmLgSJXZX-0zBt7o-DU35YT2-_OteibRot9DXf3sUOUzPf1PzFQGqG5aNC0W5Qp2mySCmmmEjM3PuV0_qx6H9HbTY7Tn-E8UhjK4YOIEadVNqH5jMN5lpsbl8K0HzduDgSNOOT28dijuq5AzzDhuLRw9p5C3Bwe3YoK7A7iDb67EekM6-jFR_CyF-E8y2XzEcJAm2Lm4JsreUGoh-_EUeNa1z-qMDmAFTA5cTm7P9tE0RjHhRdl0lrFOPxG-j08AYtW5Eu00wr912riUlVpkknlieWYowmWOHT1T3p2K_rH8a4nJhgQbEpK9JjBoNv_IVFPZZZnO8NTeIuLX6aoWapqgaOv0RQph6JgGRkfrd7ko-kZNLmBJxrL64RtMqyzwM8LCYRdQ-m-erykg8iY8Y46msSUgTFo4AN859kY2KrYufqHAjem7-aIQYg7jge5yrzwypCphb2VTT1SoHHMOuF2TKFMDFOBMGfh7HYwqQSc_g0oETyHodz8ZGLlBMbfuyR8qUtkjgtR3dfZ4alLs6ti1o7_qi3k"}

    url = f"https://go-global-apex.architecture.caradhras.io/account/get/{account}"
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as resp:
            
            #print(resp)

            if resp.status == 200:
                data = await resp.json()
                return f"{data}"
            else:
                return f"Failed to fetch account from {account}, statuscode: {resp.status}"
            
@mcp.tool()
async def get_account_statement(account: str) -> str:
    """
    Get all account bank statementor or moviments from a endpoint via rest call api

    Example: https://go-global-apex.architecture.caradhras.io/ledger/movimentStatement/ACC-1000

    Args:
        account: Account Identificator
    Raises:
        ValueError: http status code
    """
    headers = {"Authorization": "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl91c2UiOiJhY2Nlc3MiLCJpc3MiOiJnby1vYXV0aC1sYW1iZGEiLCJ2ZXJzaW9uIjoiMi4xIiwiand0X2lkIjoiY2VjZDU0OWYtYmMxMC00YzRmLWIxMWItMWEwZjZhMjA0ODQzIiwidXNlcm5hbWUiOiJ1c2VyLTAzIiwidGllciI6InRpZXItMDMiLCJhcGlfYWNjZXNzX2tleSI6IkFQSV9BQ0NFU1NfS0VZX1VTRVJfMDMiLCJzY29wZSI6WyJ0ZXN0LnJlYWQiLCJ0ZXN0LndyaXRlIiwiYWRtaW4iXSwiZXhwIjoxNzU3Nzg4OTYwfQ.LVUB3K3UXrVggvt8rkT_1ipIAj_jQReAJYKAdhLZk1m2a-S9gkF2FyH0N3qe6zRmbedBXsj33jKxF2UHmDdLZ1-M9Z0ar43I9JUGfXN2emoUWkjCb0xxFfmiEJ7ddEqIOOmNOGqHdxMWnmLgSJXZX-0zBt7o-DU35YT2-_OteibRot9DXf3sUOUzPf1PzFQGqG5aNC0W5Qp2mySCmmmEjM3PuV0_qx6H9HbTY7Tn-E8UhjK4YOIEadVNqH5jMN5lpsbl8K0HzduDgSNOOT28dijuq5AzzDhuLRw9p5C3Bwe3YoK7A7iDb67EekM6-jFR_CyF-E8y2XzEcJAm2Lm4JsreUGoh-_EUeNa1z-qMDmAFTA5cTm7P9tE0RjHhRdl0lrFOPxG-j08AYtW5Eu00wr912riUlVpkknlieWYowmWOHT1T3p2K_rH8a4nJhgQbEpK9JjBoNv_IVFPZZZnO8NTeIuLX6aoWapqgaOv0RQph6JgGRkfrd7ko-kZNLmBJxrL64RtMqyzwM8LCYRdQ-m-erykg8iY8Y46msSUgTFo4AN859kY2KrYufqHAjem7-aIQYg7jge5yrzwypCphb2VTT1SoHHMOuF2TKFMDFOBMGfh7HYwqQSc_g0oETyHodz8ZGLlBMbfuyR8qUtkjgtR3dfZ4alLs6ti1o7_qi3k"}

    url = f"https://go-global-apex.architecture.caradhras.io/ledger/movimentStatement/{account}"
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as resp:
            
            #print(resp)

            if resp.status == 200:
                data = await resp.json()
                return f"{data}"
            else:
                return f"Failed to fetch account from {account}, statuscode: {resp.status}"