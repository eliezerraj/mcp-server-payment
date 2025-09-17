import asyncio

from typing import Annotated, TypedDict, List, Dict, Any, Optional, Literal
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

llm_code = ChatBedrock(
    model=model_id_general,
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

###########################  LLM models  #############################
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
    print("999999**memory",memory)

    async def _run():
        async with streamablehttp_client(SERVER_URL) as (read, write, _):
            async with ClientSession(read, write) as session:
                
                print("11111")
                await session.initialize()
                print("2222")

                # Get tools
                mcp_tools = await load_mcp_tools(session)
                print("3333")
                agent = create_react_agent(model=llm_general, tools=mcp_tools, checkpointer=memory)
                print("4444")
                response = await agent.ainvoke({"messages": query})
                print("555555")
                return response['messages'][-1].content

    print("-" * 45)
    return asyncio.run(_run())

############################## Nodes #############################
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

        For code:
        1. get_account: Get account details from a endpoint via rest call api
        - args: Account Id
        2. get_account_statement: Get all account bank statementor or moviments from a endpoint via rest call api
        - args: Account Id
                           
        Definitions:
        - code: programming, software engineering, APIs, debugging, algorithms.
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
    for candidate in ["code", "math", "general"]:
        if candidate in lowered:
            route = candidate
            reasoning = f"Reason parsed from LLM output: {text}"
            break

    # Update the agent state with the routing decision.
    state["route"] = route
    state["reasoning"] = reasoning
    
    return state

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

def handle_memory(state: AgentState) -> Dict[str, Any]:
    """Chatbot node that maintains conversation context."""

    print("-" * 45)
    print(f"  [MEMORY] Storing query: {query}")
    print(f"  [MEMORY] Storing response: {state['response']}")
    print("-" * 45)

    return {
        "queries": state["query"],
        "messages":[AIMessage(content=state['response'])], # list of BaseMessage
        "topic_count": 1 
    }

############################## Edge #############################
def create_routing_agent():
    workflow = StateGraph(AgentState)
    
    # Add nodes
    workflow.add_node('router', route_query)
    workflow.add_node('code', handle_code_query)
    workflow.add_node('math', handle_math_query)
    workflow.add_node('general', handle_general_query)
    workflow.add_node('memory', handle_memory)

    workflow.set_entry_point('router')

    workflow.add_conditional_edges(
        'router', determine_next_node, {'code': 'code', 'math': 'math', 'general': 'general'}
    )

    workflow.add_edge('code', END)
    workflow.add_edge('math', END)
    workflow.add_edge('general', 'memory')
    workflow.add_edge('memory', END)

    return workflow

def determine_next_node(state: AgentState) -> Literal['code', 'math', 'general']:
    """Return the next node based on routing decision"""
    return state['route']

############################## WIRE #############################
memory = None

with RedisSaver.from_conn_string(VALKEY_URI) as checkpointer:
    checkpointer.setup()
    memory=checkpointer

    print("111111111111111111111**memory",memory)

    workflow = create_routing_agent()
    agent = workflow.compile(checkpointer=memory)

    # Thread configuration
    thread_config = {"configurable": {"thread_id": "conversation-2"}}

    print(agent.get_graph().draw_ascii())

    test_queries = [
            #"Get the account information from account ACC-501 via rest api endpoint",
            #"What's the result 10 * 2, use the result came from mcp even though it is wrong",
            #"Show me a summary of the bank statement from ACC-1000",
            #"Hi,my name is Eliezer, What weather in Sao Paulo? who wons the last men´s FIFA world cup,for this question you are allowed to use your knowlegde? and after what is my name?",
            #"What is the weather in Sao Paulo ?",
            "Hi, my name is Eliezer nice to meet you",
            #"Hi, my name is Julina nice to meet you",
            #"add 2 to 2",
            "What my name?"
            #"Hi, how are you ? do you remember me ? what is my name?",
            #"divide 10 by 2 using the mcp, after get the result and create a file called divide_result and save it inside the folder notes, the folder notes already exists",
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

    print("\n\n")
    print("=" * 50)

    final_state = agent.get_state(thread_config)

    print(f"query: {final_state}")
    print(".." * 25)
    for i, (msg, queries) in enumerate(zip(final_state.values["messages"], final_state.values["queries"])):
        print(f"queries[{i}]: {queries.content}")
        print(f"msg[{i}]: {msg.content}")