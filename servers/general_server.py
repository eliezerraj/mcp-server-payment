import os
import json
from datetime import datetime
from mcp.server.fastmcp import FastMCP

PORT = os.getenv("PORT", "9000")
HOST = os.getenv("HOST", "127.0.0.1")

mcp = FastMCP(name="general_server",        
        host=HOST,
        port=PORT,
        debug=True,
    )

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
    

if __name__ == "__main__":
    print("-" * 45)
    print(f"GENERAL SERVER {HOST}:{PORT}")
    print("-" * 45)

    mcp.run(transport="streamable-http")