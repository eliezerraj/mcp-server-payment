import asyncio
from mcp import ClientSession
from mcp.client.streamable_http import streamablehttp_client

from langgraph.prebuilt import create_react_agent
from langchain_mcp_adapters.tools import load_mcp_tools

import boto3
from dotenv import load_dotenv
from langchain_aws import ChatBedrock

# Create a Bedrock Runtime client in the AWS Region you want to use.
client = boto3.client("bedrock-runtime", region_name="us-east-1")

# Set the model ID, e.g., Amazon Nova Lite.
model_id = "amazon.nova-pro-v1:0"

llm_aws = ChatBedrock(
    model=model_id,
    region_name="us-east-1",
    client=client,
)

SERVER_URL = "http://localhost:8000/mcp"

async def main():
    async with streamablehttp_client(SERVER_URL) as (read, write, _):
        async with ClientSession(read, write) as session:
            # Initialize the connection
            await session.initialize()

            # Get tools
            mcp_tools = await load_mcp_tools(session)

            direct_return_agent = create_react_agent(model=llm_aws,
                                                    tools =mcp_tools,
                                                    )
            
            agent = create_react_agent("openai:gpt-4.1", tools)
            math_response = await agent.ainvoke({"messages": "what's (3 + 5) x 12?"})

if __name__ == '__main__':
    asyncio.run(main())