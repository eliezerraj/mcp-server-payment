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

################### WEATHER #################################
@mcp.tool(name="get_weather")
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

###################### GENERAL ##############################
@mcp.tool(name="get_current_time")
def get_current_time() -> str:
    """
    Get current date and time.

    Example: What time is it?

    Returns:
        str: The date and time
    """

    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')

@mcp.tool(name="save_note")
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

######################## Endpoint ###########################
@mcp.tool(name="get_account")
async def get_account(account: str) -> str:
    """
    Get account details from a endpoint via rest call api

    Example: https://go-global-apex.architecture.caradhras.io/account/get/ACC-500

    Args:
        account: Account Identificator
    Raises:
        ValueError: http status code
    """
    headers = {"Authorization": "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl91c2UiOiJhY2Nlc3MiLCJpc3MiOiJnby1vYXV0aC1sYW1iZGEiLCJ2ZXJzaW9uIjoiMi4xIiwiand0X2lkIjoiMDkzMTAxYTYtNTQwYy00MDQ4LTgwMmEtZjNhMGE1ZTNjZGVjIiwidXNlcm5hbWUiOiJ1c2VyLTAzIiwidGllciI6InRpZXItMDMiLCJhcGlfYWNjZXNzX2tleSI6IkFQSV9BQ0NFU1NfS0VZX1VTRVJfMDMiLCJzY29wZSI6WyJ0ZXN0LnJlYWQiLCJ0ZXN0LndyaXRlIiwiYWRtaW4iXSwiZXhwIjoxNzU4MDQxNDUzfQ.cPBIKyersyN1X_QfBpuEUhr2wStQqD3AaN-YSOyQmqJ7NA1IxXUKeWEjKNNHrZqYuOfOl9rPJLoEPhH1Jr-r9dHWsszN8hs4t63K40yJgzeYUXgtP_K68nD117Fv8Q7vT-4rDY27CZDGxe-teuocs6RcW5fobu_C2DdECnNzDhU-KeROYFl8uWXknVOKoAXyeX3PlK3BVBtKrOgzgutsPsamtdw1ivN98Zte-KsZuoxYXp_oDKiWmVyM8B3x-hAmcOUo_0VSp5y7P0-KUHiceEJmEeLIt7XeCOjPFNsiIypik8gIwWCN11KcMjLaoR-StMTnXHnoMbFK40mkpHS1IKu4KPqm9Yj5Im5bpK442uIn5FA5zRtWVhyM1bvnai3j66QjKP0mPJ3sMRroIo7rn6gFhqJdUgzxmNX0FLy_Oi0Vh9oLhT1ASmYO0U_wuGuzz4ZG4YkwK0_YD9sqVWq4CRDo2naK8lEPoAK65aAk-QS1eXrh7lMPTQg8eyZj2gtJh1NB04_HJjdZGZVZPgyx16hrq5Hy8Qm6PU6wBO8gfYWxbWcle7FvUfZx-_hhzhxgicsCeAPVHca9GnYEt0olrJvtqlTTMM8VT9CL75p-2swf82JSpV1zZmJnj4uQ-WhlNFu631OIIudF09rcxTghAXnAUwoUVkvRJCpnJpYysoI"}

    url = f"https://go-global-apex.architecture.caradhras.io/account/get/{account}"
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as resp:
            
            #print(resp)

            if resp.status == 200:
                data = await resp.json()
                return f"{data}"
            else:
                return f"Failed to fetch account from {account}, statuscode: {resp.status}"
            
@mcp.tool(name="get_account_statement")
async def get_account_statement(account: str) -> str:
    """
    Get all account bank statementor or moviments from a endpoint via rest call api

    Example: https://go-global-apex.architecture.caradhras.io/ledger/movimentStatement/ACC-1000

    Args:
        account: Account Identificator
    Raises:
        ValueError: http status code
    """
    headers = {"Authorization": "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl91c2UiOiJhY2Nlc3MiLCJpc3MiOiJnby1vYXV0aC1sYW1iZGEiLCJ2ZXJzaW9uIjoiMi4xIiwiand0X2lkIjoiMDkzMTAxYTYtNTQwYy00MDQ4LTgwMmEtZjNhMGE1ZTNjZGVjIiwidXNlcm5hbWUiOiJ1c2VyLTAzIiwidGllciI6InRpZXItMDMiLCJhcGlfYWNjZXNzX2tleSI6IkFQSV9BQ0NFU1NfS0VZX1VTRVJfMDMiLCJzY29wZSI6WyJ0ZXN0LnJlYWQiLCJ0ZXN0LndyaXRlIiwiYWRtaW4iXSwiZXhwIjoxNzU4MDQxNDUzfQ.cPBIKyersyN1X_QfBpuEUhr2wStQqD3AaN-YSOyQmqJ7NA1IxXUKeWEjKNNHrZqYuOfOl9rPJLoEPhH1Jr-r9dHWsszN8hs4t63K40yJgzeYUXgtP_K68nD117Fv8Q7vT-4rDY27CZDGxe-teuocs6RcW5fobu_C2DdECnNzDhU-KeROYFl8uWXknVOKoAXyeX3PlK3BVBtKrOgzgutsPsamtdw1ivN98Zte-KsZuoxYXp_oDKiWmVyM8B3x-hAmcOUo_0VSp5y7P0-KUHiceEJmEeLIt7XeCOjPFNsiIypik8gIwWCN11KcMjLaoR-StMTnXHnoMbFK40mkpHS1IKu4KPqm9Yj5Im5bpK442uIn5FA5zRtWVhyM1bvnai3j66QjKP0mPJ3sMRroIo7rn6gFhqJdUgzxmNX0FLy_Oi0Vh9oLhT1ASmYO0U_wuGuzz4ZG4YkwK0_YD9sqVWq4CRDo2naK8lEPoAK65aAk-QS1eXrh7lMPTQg8eyZj2gtJh1NB04_HJjdZGZVZPgyx16hrq5Hy8Qm6PU6wBO8gfYWxbWcle7FvUfZx-_hhzhxgicsCeAPVHca9GnYEt0olrJvtqlTTMM8VT9CL75p-2swf82JSpV1zZmJnj4uQ-WhlNFu631OIIudF09rcxTghAXnAUwoUVkvRJCpnJpYysoI"}

    url = f"https://go-global-apex.architecture.caradhras.io/ledger/movimentStatement/{account}"
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as resp:
            
            if resp.status == 200:
                data = await resp.json()
                return f"{data}"
            else:
                return f"Failed to fetch account from {account}, statuscode: {resp.status}"