import asyncio

from typing import Annotated, TypedDict, List, Dict, Any, Literal
from operator import add

#mcp
from mcp import ClientSession
from mcp.client.streamable_http import streamablehttp_client

#langraph
from langgraph.prebuilt import create_react_agent
from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages
from langgraph.checkpoint.redis import RedisSaver

# langchain
from langchain_core.messages import SystemMessage, HumanMessage, BaseMessage, AIMessage
from langchain_mcp_adapters.tools import load_mcp_tools

# aws
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

llm_general = ChatBedrock(
    model=model_id_general,
    temperature=0, #0 =full deterministic
    region_name="us-east-1",
    client=client,
)

llm_math = ChatBedrock(
    model=model_id_math,
    temperature=0, #0 =full deterministic
    region_name="us-east-1",
    client=client,
)

#mcp tools url
SERVER_URL = "http://localhost:8000/mcp"
VALKEY_URI = "redis://localhost:6379"

# Define the state structure
class AgentState(TypedDict):
    query: str
    route: str
    response: str
    reasoning: str
    messages: Annotated[List[BaseMessage], add_messages]
    queries: Annotated[List[str], add_messages]
    topic_count: Annotated[int, add]
    session_info: Dict[str, Any]

#load tools
global_session = None
global_tools = None

async def setup_mcp_client():
    """Initialize MCP session and load tools once."""
    global global_session, global_tools
    print("[INFO] Connecting to MCP server...")

    read, write, _ = await streamablehttp_client(SERVER_URL)
    global_session = ClientSession(read, write)
    await global_session.initialize()

    global_tools = await load_mcp_tools(global_session)
    print(f"[INFO] MCP tools loaded: {list(global_tools)}")

# Run once at startup
asyncio.run(setup_mcp_client())

print(f"global_session: {global_session}")
print(f"global_tools: {global_tools}")

"""" 
def load_tools_sync():
    async def _load():
        async with streamablehttp_client(SERVER_URL) as (read, write, _):
            async with ClientSession(read, write) as session:
                global global_session, global_tools

                global_session = session
                await global_session.initialize()

                global_tools = await load_mcp_tools(global_session)
                #return global_tools
    return asyncio.run(_load())

load_tools_sync()
#print(f"[INFO] MCP tools loaded: {list(mcp_server_tools)}")

print(f"global_session: {global_session}")
print(f"global_tools: {global_tools}")
"""

###########################  LLM models  #############################
def math_llm(state: AgentState) -> AgentState:
    """Specialized LLM for math questions"""

    print("-" * 45)
    print(f"  [MATH LLM] Mathematical response to: {query}")

    # Pass the global mcp_server_tools directly
    agent = create_react_agent(model=llm_math, tools=global_tools)
    response = asyncio.run(agent.ainvoke({"messages": state['query']}))
    return response['messages'][-1].content

def general_llm(state: AgentState) -> AgentState:
    """General purpose LLM"""
    
    print("-" * 45)
    print(f"  [GENERAL LLM] General response to: {query}")

    # Pass the global mcp_server_tools directly
    agent = create_react_agent(model=llm_general, tools=global_tools) # Corrected model and tool usage
    response = asyncio.run(agent.ainvoke({"messages": state['query']}, config={'configurable': {'session': global_session}}))
    return response['messages'][-1].content

############################## Nodes #############################
def route_query(state: AgentState) -> AgentState:  
    # Extract and clean the user query from the state.
    query = state["query"].strip()

    # Define the system prompt to instruct the LLM on its role and required output format.
    system = SystemMessage(content="""
        You are a routing classifier. Given a user query, respond ONLY with one token from this set:
        code | math | general

        You have access to MCP tools bellow:

        For math:
        1. add: add two numbers
        - args: a (float) the first number and b (float) the second number
        2. sub: subtract two numbers
        - args: a (float) the first number and b (float) the second number
        3. multiple: multiplication two numbers
        - args: a (float) the first number and b (float) the second number
        4. divide: divide two numbers
        - args: a (float) the first number and b (float) the second number

        For general:
        1. get_weather: Get current weather information for a given location.
            - args: location: The city name to get weather for
        2. get_current_time: Get current date and time.
        3. save_note: Save a text note for the user to a file.
        - args: filename (name of the file to save without extension) and content (The text content to save)

        Definitions:
        - math: equations, calculus, probability, statistics, numeric problem solving.
        - general: anything else (explanations, science, weather, sports, general knowledge, greeting, personal information).
        
        Always consider the result from these tools are the right answer, do not question any result.
        Whenever the availables tools do not support a query, you must use your knowledge.
        If ambiguous, choose the most plausible specialized category else 'general'.
        Return a JSON object: {"route": <one of above>, "reasoning": "short explanation"}.
        Strict JSON.
        """.strip())
    
    # Prepare the user's query for the LLM.
    human = HumanMessage(content=f"Query: {query}")

    # Send the request to the LLM.
    raw = llm_general.invoke([system, human])
    
    # Normalize the LLM response to a string.
    text = raw.content if hasattr(raw, 'content') else str(raw)

    # Set default values in case parsing fails.
    route = "general"
    reasoning = "Default routing to general"

    lowered = text.lower()
    for candidate in ["math", "general"]:
        if candidate in lowered:
            route = candidate
            reasoning = f"Reason parsed from LLM output: {text}"
            break

    # Update the agent state with the routing decision.
    state["route"] = route
    state["reasoning"] = reasoning
    
    return state

def handle_math_query(state: AgentState) -> AgentState:
    """Process query with math-specialized LLM"""
    response = math_llm(state)
    state['response'] = response
    return state

def handle_general_query(state: AgentState) -> AgentState:
    """Process query with general LLM"""
    response = general_llm(state)
    state['response'] = response
    return state

def handle_memory(state: AgentState) -> Dict[str, Any]:
    """Chatbot node that maintains conversation context."""

    print("-" * 45)
    print(f"  [MEMORY] Storing query: {state['query']}")
    print(f"  [MEMORY] Storing response: {state['response']}")
    print("-" * 45)

    return {
        "queries": state["query"],
        "messages":[AIMessage(content=state['response'])], # list of BaseMessage
        "topic_count": 1 
    }

############################## Edge #############################
def create_routing_agent():
    """Create and return the LangGraph routing agent."""

    workflow = StateGraph(AgentState)
    
    # Add nodes
    workflow.add_node('router', route_query)
    workflow.add_node('math', handle_math_query)
    workflow.add_node('general', handle_general_query)
    workflow.add_node('memory', handle_memory)

    workflow.set_entry_point('router')

    workflow.add_conditional_edges(
        'router', determine_next_node, {'math': 'math', 'general': 'general'}
    )

    workflow.add_edge('math', END)
    workflow.add_edge('general', 'memory')
    workflow.add_edge('memory', END)

    return workflow

def determine_next_node(state: AgentState) -> Literal['code', 'math', 'general']:
    """Return the next node based on routing decision"""
    return state['route']

############################## WIRE ########################

memory = None
with RedisSaver.from_conn_string(VALKEY_URI) as checkpointer:
    checkpointer.setup()
    memory=checkpointer

    workflow = create_routing_agent()
    agent = workflow.compile()

    # Thread configuration
    thread_config = {"configurable": {"thread_id": "conversation-3"}}

    print(agent.get_graph().draw_ascii())

    test_queries = [
            "What the weather in Paris?",
            "add 2 to 2",
    ]

    print("*** LangGraph Routing Agent *** \n\n")
    print("**" * 50)
    for i, query in enumerate(test_queries, 1):
        print(f"Query: {i} => {query} \n")
        # Run the agent
        result = agent.invoke({'query': query, "topic_count": i}, thread_config)
        # Print results with rich formatting
        print(f"Route: {result['route']}")
        print(f"Reasoning: {result['reasoning']}")
        print("**" * 50)
        print(f"Response: {result['response']}")
        print("**" * 50)
