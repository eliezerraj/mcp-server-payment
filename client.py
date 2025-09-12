import asyncio
import json
from langgraph.graph import StateGraph, END
from mcp import ClientSession
from mcp.client.streamable_http import streamablehttp_client
from langgraph.prebuilt import create_react_agent
from langchain_mcp_adapters.tools import load_mcp_tools
from typing import TypedDict, Literal
from langchain_core.messages import SystemMessage, HumanMessage

import boto3
from dotenv import load_dotenv
from langchain_aws import ChatBedrock

# Create a Bedrock Runtime client in the AWS Region you want to use.
load_dotenv()
client = boto3.client("bedrock-runtime", region_name="us-east-1")

# Set the model ID, e.g., Amazon Nova Lite.
model_id_general = "amazon.nova-pro-v1:0"       # General
model_id_math    = "amazon.nova-lite-v1:0"      # Math
model_id_code    = "amazon.nova-premier-v1:0"   # Code

llm_aws_general = ChatBedrock(
    model=model_id_general,
    temperature=0,
    region_name="us-east-1",
    client=client,
)

llm_math = ChatBedrock(
    model=model_id_math,
    temperature=0,
    region_name="us-east-1",
    client=client,
)

llm_code = ChatBedrock(
    model=model_id_general,
    temperature=0,
    region_name="us-east-1",
    client=client,
)

SERVER_URL = "http://localhost:8000/mcp"

# Define the state structure
class AgentState(TypedDict):
    query: str
    route: str
    response: str
    reasoning: str

###########################  Mock LLM responses (replace with actual LLM calls) #############################
def code_llm(query: str) -> str:
    """Specialized LLM for coding questions"""

    print("-" * 45)
    print(f"  [CODE LLM] Code response to: {query}")

    response = ""
    async def _run():
        async with streamablehttp_client(SERVER_URL) as (read, write, _):
            async with ClientSession(read, write) as session:
                await session.initialize()

                # Get tools
                mcp_tools = await load_mcp_tools(session)

                agent = create_react_agent(model=llm_code, tools=mcp_tools)
                response = await agent.ainvoke({"messages": query})
                return response['messages'][-1].content

    print("-" * 45)
    return asyncio.run(_run())

def math_llm(query: str) -> str:
    """Specialized LLM for math questions"""

    print("-" * 45)
    print(f"  [MATH LLM] Mathematical response to: {query}")

    response = ""
    async def _run():
        async with streamablehttp_client(SERVER_URL) as (read, write, _):
            async with ClientSession(read, write) as session:
                await session.initialize()

                # Get tools
                mcp_tools = await load_mcp_tools(session)

                agent = create_react_agent(model=llm_math, tools=mcp_tools)
                response = await agent.ainvoke({"messages": query})
                return response['messages'][-1].content

    print("-" * 45)
    return asyncio.run(_run())

def general_llm(query: str) -> str:
    """General purpose LLM"""
    
    print("-" * 45)
    print(f"  [GENERAL LLM] General response to: {query}")

    response = ""
    async def _run():
        async with streamablehttp_client(SERVER_URL) as (read, write, _):
            async with ClientSession(read, write) as session:
                await session.initialize()

                # Get tools
                mcp_tools = await load_mcp_tools(session)

                agent = create_react_agent(model=llm_aws_general, tools=mcp_tools)
                response = await agent.ainvoke({"messages": query})
                return response['messages'][-1].content

    print("-" * 45)
    return asyncio.run(_run())

############################## Agent #############################
def handle_code_query(state: AgentState) -> AgentState:
    """Process query with code-specialized LLM"""
    response = code_llm(state['query'])
    state['response'] = response
    return state

def handle_math_query(state: AgentState) -> AgentState:
    """Process query with math-specialized LLM"""
    response = math_llm(state['query'])
    state['response'] = response
    return state

def handle_general_query(state: AgentState) -> AgentState:
    """Process query with general LLM"""
    response = general_llm(state['query'])
    state['response'] = response
    return state

def route_query(state: AgentState) -> AgentState:
    """ Classify the user's query into a specific domain using an LLM.
    Fall back to heuristic parsing if the LLM response is not valid JSON."""
    
    # Extract and clean the user query from the state.
    query = state["query"].strip()

    # Initialize the LLM for classification.

    # Define the system prompt to instruct the LLM on its role and required output format.
    system = SystemMessage(content="""
        You are a routing classifier. Given a user query, respond ONLY with one token from this set:
        code | math | general
        Definitions:
        - code: programming, software engineering, APIs, debugging, algorithms.
        - math: equations, calculus, probability, statistics, numeric problem solving.
        - general: anything else (explanations, science, history, general knowledge).
        If ambiguous, choose the most plausible specialized category else 'general'.
        Return a JSON object: {"route": <one of above>, "reasoning": "short explanation"}.
        Strict JSON.
        """.strip())
    
    # Prepare the user's query for the LLM.
    human = HumanMessage(content=f"Query: {query}")

    # Send the request to the LLM.
    raw = llm_aws_general.invoke([system, human])
    
    # Normalize the LLM response to a string.
    text = raw.content if hasattr(raw, 'content') else str(raw)

    # Set default values in case parsing fails.
    route = "general"
    reasoning = "Default routing to general"

    lowered = text.lower()
    for candidate in ["code", "math", "general"]:
        if candidate in lowered:
            route = candidate
            reasoning = f"Reason parsed from LLM output: {text}"
            break

    # Update the agent state with the routing decision.
    state["route"] = route
    state["reasoning"] = reasoning
    
    return state

############################## Router / Edge #############################
def determine_next_node(state: AgentState) -> Literal['code', 'math', 'creative', 'general']:
    """Return the next node based on routing decision"""
    return state['route']

def create_routing_agent(use_llm: bool = True):
    """Create and return the LangGraph routing agent.

    Args:
        use_llm: If True and LLM available, use LLM router; otherwise keyword router.
    """

    workflow = StateGraph(AgentState)
    
    # Add nodes
    workflow.add_node('router', route_query)
    workflow.add_node('code', handle_code_query)
    workflow.add_node('math', handle_math_query)
    workflow.add_node('general', handle_general_query)

    workflow.set_entry_point('router')

    workflow.add_conditional_edges(
        'router', determine_next_node, {'code': 'code', 'math': 'math', 'general': 'general'}
    )

    workflow.add_edge('code', END)
    workflow.add_edge('math', END)
    workflow.add_edge('general', END)

    return workflow.compile()

agent = create_routing_agent(use_llm=True)

print(agent.get_graph().draw_ascii())

from rich.panel import Panel
from rich.rule import Rule

test_queries = [
    "Get the account information from account ACC-501 via rest api endpoint",
    #"What's the result 10 * 2 and show the result from mcp tools?",
    #"Show me how many person have in database",
    #"What is the weather in Sao Paulo ?",
    #"add 2 to 2",
]

print("LangGraph Routing Agent")

for i, query in enumerate(test_queries, 1):
    print("#" * 50)
    print(f"->Query: {i} => {query} \n")

    # Run the agent
    result = agent.invoke({'query': query})

    # Print results with rich formatting
    print(f"->Route: {result['route']}")
    print(f"->Reasoning: {result['reasoning']}")
    print(f"->Response: {result['response']}")