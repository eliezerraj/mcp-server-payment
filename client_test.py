import asyncio
from mcp import ClientSession
from mcp.client.streamable_http import streamablehttp_client
from langgraph.prebuilt import create_react_agent
from langchain_mcp_adapters.tools import load_mcp_tools

import boto3
from dotenv import load_dotenv
from langchain_aws import ChatBedrock

# Create a Bedrock Runtime client in the AWS Region you want to use.
load_dotenv()
client = boto3.client("bedrock-runtime", region_name="us-east-1")

# Set the model ID, e.g., Amazon Nova Lite.
model_id = "amazon.nova-pro-v1:0"

llm_aws = ChatBedrock(
    model=model_id,
    region_name="us-east-1",
    client=client,
)

SERVER_URL = "http://localhost:8000/mcp"

#prompt = "add 1 to 2 and multiple the result for 3"
#prompt = "what is the wheater in Sao Paulo ?"
#prompt = "Save a note called to file 'my_list' with my itens: dogs, cats, and birds"
#prompt = "add 1 to 2 and multiple the result for 3 and save the result in a file called calc_result_01"

async def main():
    async with streamablehttp_client(SERVER_URL) as (read, write, _):
        async with ClientSession(read, write) as session:
            # Initialize the connection
            await session.initialize()

            # Get tools
            mcp_tools = await load_mcp_tools(session)

            agent = create_react_agent(model=llm_aws, tools=mcp_tools)
            response = await agent.ainvoke({"messages": prompt})

            print(f"response: {response}")
            print("-" * 45)
            print(f"Response: {response['messages'][-1].content}")

if __name__ == '__main__':
    asyncio.run(main())