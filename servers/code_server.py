import os
import logging
import aiohttp
from mcp.server.fastmcp import FastMCP

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

PORT = os.getenv("PORT", "9002")
HOST = os.getenv("HOST", "127.0.0.1")
SESSION_TIMEOUT = 30

mcp = FastMCP(name="code_server",        
        host=HOST,
        port=PORT,
        debug=True,
    )

session_timeout = aiohttp.ClientTimeout(total=SESSION_TIMEOUT)

# Gateway_GRPC
@mcp.tool(name="gateway_grpc_healthy")
async def gateway_grpc_healthy(context: dict = None) -> str:
    """
    Check the healthy status GATEWAY_GRPC service and get service enviroment variables

    Response:
        - information about the health status and enviroment variables
    Raises:
        - valueError: http status code
    """
    logger.info(f"function => gateway_grpc_healthy()")

    jwt_token = context.get("jwt") if context else None
    if not jwt_token:
        logger.error( "No JWT provided, NOT AUTHORIZED, statuscode: 403")
        return "No JWT provided, NOT AUTHORIZED, statuscode: 403"
 
    logger.info(f"jwt_token: {jwt_token}")
    
    headers = {"Authorization": f"Bearer {jwt_token}"}                  
    url = f"https://go-global-apex.architecture.caradhras.io/gateway-grpc/info"
    
    async with aiohttp.ClientSession(timeout=session_timeout) as session:
        async with session.get(url, headers=headers) as resp:
            if resp.status == 200:
                data = await resp.json()
                return f"{data}"
            else:
                return f"Failed to fetch gateway_grp healthy, statuscode: {resp.status}"
            
# Payment_Gateway
@mcp.tool(name="payment_gateway_healthy")
async def payment_gateway_healthy(context: dict = None) -> str:
    """
    Check the healthy status PAYMENT_GATEWAY service and get service enviroment variables

    Response:
        - information about the health status and enviroment variables
    Raises:
        - valueError: http status code
    """
    
    logger.info(f"function => payment_gateway_healthy()")
    
    jwt_token = context.get("jwt") if context else None
    if not jwt_token:
        logger.error( "No JWT provided, NOT AUTHORIZED, statuscode: 403")
        return "No JWT provided, NOT AUTHORIZED, statuscode: 403"
 
    logger.info(f"jwt_token: {jwt_token}")
    
    headers = {"Authorization": f"Bearer {jwt_token}"}                  
    url = f"https://go-global-apex.architecture.caradhras.io/payment-gateway/info"
    
    async with aiohttp.ClientSession(timeout=session_timeout) as session:
        async with session.get(url, headers=headers) as resp:
            if resp.status == 200:
                data = await resp.json()
                return f"{data}"
            else:
                return f"Failed to fetch payment_gateway healthy, statuscode: {resp.status}"

@mcp.tool(name="get_card_payment")
async def get_card_payment(card: str, date: str, context: dict = None) -> str:
    """
    Get all payments did by a CREDIT CARD or a DEBIT CARD such as payments (amount, date, type and model), card status, atc, mcc, holder

    Args:
        - card: card id with a strictly in the format: 999.999.999.999 (Exactly 12 digits split into 4 groups of 3 digits each)
        - card: payment date format YYYY-MM-DD
    Response:
        - list: A list of payments with information such as card type, card model, payment amount, terminal, payment status and payment date
    Raises:
        - valueError: http status code
    """
    
    logger.info(f"function => get_card_payment() card:{card} date:{date} ")
    
    jwt_token = context.get("jwt") if context else None
    if not jwt_token:
        logger.error( "No JWT provided, NOT AUTHORIZED, statuscode: 403")
        return "No JWT provided, NOT AUTHORIZED, statuscode: 403"
 
    logger.info(f"jwt_token: {jwt_token}")
    
    headers = {"Authorization": f"Bearer {jwt_token}"}                  
    url = f"https://go-global-apex.architecture.caradhras.io/payment-gateway/payment?card={card}&after={date}"
    
    async with aiohttp.ClientSession(timeout=session_timeout) as session:
        async with session.get(url, headers=headers) as resp:
            if resp.status == 200:
                data = await resp.json()

                print(f"data =========> {data}")
                
                return f"{data}"
            else:
                return f"Failed to fetch payment_gateway healthy, statuscode: {resp.status}"
                        
# Limit
@mcp.tool(name="limit_healthy")
async def limit_healthy(context: dict = None) -> str:
    """
    Check the healthy status LIMIT service and get service enviroment variables

    Response:
        - information about the health status and enviroment variables
    Raises:
        - valueError: http status code
    """
    
    logger.info(f"function => limit_healthy()")

    jwt_token = context.get("jwt") if context else None
    if not jwt_token:
        logger.error( "No JWT provided, NOT AUTHORIZED, statuscode: 403")
        return "No JWT provided, NOT AUTHORIZED, statuscode: 403"
 
    logger.info(f"jwt_token: {jwt_token}")
    
    headers = {"Authorization": f"Bearer {jwt_token}"}                   
    url = f"https://go-global.architecture.caradhras.io/limit/info"
    
    async with aiohttp.ClientSession(timeout=session_timeout) as session:
        async with session.get(url, headers=headers) as resp:
            if resp.status == 200:
                data = await resp.json()
                return f"{data}"
            else:
                return f"Failed to fetch limit healthy, statuscode: {resp.status}"
            
# Card
@mcp.tool(name="card_healthy")
async def card_healthy(context: dict = None) -> str:
    """
    Check the healthy status of CARD service and get service enviroment variables

    Response:
        - information about the health status and enviroment variables
    Raises:
        - valueError: http status code
    """

    logger.info(f"function => card_healthy()")

    jwt_token = context.get("jwt") if context else None
    if not jwt_token:
        logger.error( "No JWT provided, NOT AUTHORIZED, statuscode: 403")
        return "No JWT provided, NOT AUTHORIZED, statuscode: 403"
 
    logger.info(f"jwt_token: {jwt_token}")
    
    headers = {"Authorization": f"Bearer {jwt_token}"}                  
    url = f"https://go-global.architecture.caradhras.io/card/info"
    
    async with aiohttp.ClientSession(timeout=session_timeout) as session:
        async with session.get(url, headers=headers) as resp:
            if resp.status == 200:
                data = await resp.json()
                return f"{data}"
            else:
                logger.error(f"Failed to fetch card healthy, statuscode: {resp.status}")
                return f"Failed to fetch card healthy, statuscode: {resp.status}"

@mcp.tool(name="get_card")
async def get_card(card: str, context: dict = None) -> str:
    """
    Get card details from a given card id

    Args:
        - card: card id
    Response:
        - card: all card data
    Raises:
        - valueError: http status code
    """

    logger.info(f"function => get_card() = card:{card}")

    jwt_token = context.get("jwt") if context else None
    if not jwt_token:
        logger.error( "No JWT provided, NOT AUTHORIZED, statuscode: 403")
        return "No JWT provided, NOT AUTHORIZED, statuscode: 403"
 
    logger.info(f"jwt_token: {jwt_token}")
    
    headers = {"Authorization": f"Bearer {jwt_token}"}                  
    url = f"https://go-global.architecture.caradhras.io/card/card/{card}"
    
    async with aiohttp.ClientSession(timeout=session_timeout) as session:
        async with session.get(url, headers=headers) as resp:
            if resp.status == 200:
                data = await resp.json()
                return f"{data}"
            else:
                return f"Failed to fetch card from {card}, statuscode: {resp.status}"

# Account
@mcp.tool(name="account_healthy")
async def account_healthy(context: dict = None) -> str:
    """
    Check the healthy status ACCOUNT service and get service enviroment variables

    Response:
        - information about the health status and enviroment variables
    Raises:
        - valueError: http status code
    """

    logger.info(f"function => account_healthy()")

    jwt_token = context.get("jwt") if context else None
    if not jwt_token:
        logger.error( "No JWT provided, NOT AUTHORIZED, statuscode: 403")
        return "No JWT provided, NOT AUTHORIZED, statuscode: 403"
 
    logger.info(f"jwt_token: {jwt_token}")
    
    headers = {"Authorization": f"Bearer {jwt_token}"}                
    url = f"https://go-global-apex.architecture.caradhras.io/account/info"
    
    async with aiohttp.ClientSession(timeout=session_timeout) as session:
        async with session.get(url, headers=headers) as resp:
            if resp.status == 200:
                data = await resp.json()
                return f"{data}"
            else:
                return f"Failed to fetch account healthy, statuscode: {resp.status}"
            
@mcp.tool(name="get_account")
async def get_account(account: str, context: dict = None) -> str:
    """
    Get account details from a given account id

    Args:
        - account: account id
    Response:
        - account: all account data
    Raises:
        - valueError: http status code
    """

    logger.info(f"function => get_account() = account: {account}")

    jwt_token = context.get("jwt") if context else None
    if not jwt_token:
        logger.error( "No JWT provided, NOT AUTHORIZED, statuscode: 403")
        return "No JWT provided, NOT AUTHORIZED, statuscode: 403"
 
    logger.info(f"jwt_token: {jwt_token}")
    
    headers = {"Authorization": f"Bearer {jwt_token}"}                  
    url = f"https://go-global-apex.architecture.caradhras.io/account/get/{account}"
    
    async with aiohttp.ClientSession(timeout=session_timeout) as session:
        async with session.get(url, headers=headers) as resp:
            if resp.status == 200:
                data = await resp.json()
                return f"{data}"
            else:
                return f"Failed to fetch account from {account}, statuscode: {resp.status}"

@mcp.tool(name="get_accounts_from_person")
async def get_accounts_from_person(person: str, context: dict = None) -> str:
    """
    Get a list of accounts for person given

    Args:
        - person: person id
    Response:
        - list: a list of account´s with the person (owner)
    Raises:
        - valueError: http status code
    """

    logger.info(f"function => get_accounts_from_person() = person: {person}")

    jwt_token = context.get("jwt") if context else None
    if not jwt_token:
        logger.error( "No JWT provided, NOT AUTHORIZED, statuscode: 403")
        return "No JWT provided, NOT AUTHORIZED, statuscode: 403"
 
    logger.info(f"jwt_token: {jwt_token}")
    
    headers = {"Authorization": f"Bearer {jwt_token}"}   
    url = f"https://go-global-apex.architecture.caradhras.io/account/list/{person}"
    
    async with aiohttp.ClientSession(timeout=session_timeout) as session:
        async with session.get(url, headers=headers) as resp:

            if resp.status == 200:
                data = await resp.json()
                return f"{data}"
            else:
                return f"Failed to fetch account from {person}, statuscode: {resp.status}"

# Account bank statement (ledger)
@mcp.tool(name="ledger_healthy")
async def ledger_healthy(context: dict = None) -> str:
    """
    Check the healthy status account LEDGER and get service enviroment variables

    Response:
        - information about the health status and enviroment variables
    Raises:
        - valueError: http status code
    """
    logger.info(f"function => ledger_healthy()")
    
    jwt_token = context.get("jwt") if context else None
    if not jwt_token:
        logger.error( "No JWT provided, NOT AUTHORIZED, statuscode: 403")
        return "No JWT provided, NOT AUTHORIZED, statuscode: 403"
 
    logger.info(f"jwt_token: {jwt_token}")
    
    headers = {"Authorization": f"Bearer {jwt_token}"}                  
    url = f"https://go-global-apex.architecture.caradhras.io/ledger/info"
    
    async with aiohttp.ClientSession(timeout=session_timeout) as session:
        async with session.get(url, headers=headers) as resp:
            if resp.status == 200:
                data = await resp.json()
                return f"{data}"
            else:
                return f"Failed to fetch ledger healthy, statuscode: {resp.status}"
            
@mcp.tool(name="get_account_statement")
async def get_account_statement(account: str, context: dict = None) -> str:
    """
    Get account activity, balance and statement from a given account

    Args:
        - account: Account Id
    Response:
        - list: A list of bank statement, financial moviment, account activity and balance summary 
    Raises:
        - valueError: http status code
    """
    
    logger.info(f"function => get_account_statement() = account: {account}")
    
    jwt_token = context.get("jwt") if context else None
    if not jwt_token:
        logger.error( "No JWT provided, NOT AUTHORIZED, statuscode: 403")
        return "No JWT provided, NOT AUTHORIZED, statuscode: 403"
 
    logger.info(f"jwt_token: {jwt_token}")
    
    headers = {"Authorization": f"Bearer {jwt_token}"}   
    url = f"https://go-global-apex.architecture.caradhras.io/ledger/movimentStatement/{account}"
    
    async with aiohttp.ClientSession(timeout=session_timeout) as session:
        async with session.get(url, headers=headers) as resp:
            
            if resp.status == 200:
                data = await resp.json()
                return f"{data}"
            else:
                return f"Failed to fetch account from {account}, statuscode: {resp.status}"

# Memory
@mcp.tool(name="store_memory_graph_account")
async def store_memory_graph_account(person: str, account: str, relation: str, context: dict = None) -> str:
    """
    Store the ACCOUNT its relation with PERSON in memory graph account

    Args:
        - account: account identificator
        - person: person identificator
        - relations: relation between account and person, this relation MUST BE 'HAS'
    Response:
        - account: account identificator
        - person: person identificator
        - relations: relation between account and person
    Raises:
        - valueError: http status code
    """

    logger.info(f"function => store_memory_graph_account() = person: {person} account: {account} relation: {relation}")

    payload = {
        "nodes": {
            "person": {
                "person_id": person
            },
            "account": {
                "account_id": account
                }
            },
        "relations": {
            "description": relation
        },
    }

    jwt_token = context.get("jwt") if context else None
    if not jwt_token:
        logger.error( "No JWT provided, NOT AUTHORIZED, statuscode: 403")
        return "No JWT provided, NOT AUTHORIZED, statuscode: 403"
 
    logger.info(f"jwt_token: {jwt_token}")
    
    headers = {"Authorization": f"Bearer {jwt_token}"}   
    
    url = f"http://localhost:8001/graph"

    async with aiohttp.ClientSession(timeout=session_timeout) as session:
        async with session.post(url, headers=headers, json=payload) as resp:
            
            if resp.status == 200:
                data = await resp.json()
                return f"{data}"
            else:
                return f"Failed to post data {account}, statuscode: {resp.status}"

@mcp.tool(name="retrieve_memory_graph_account")
async def retrieve_memory_graph_account(account: str, context: dict = None) -> str:
    """
    Retrive from memory graph all account informations

    Args:
        - account: account identificator
    Response:
        - list: list of person_id (owner) of account
    Raises:
        - valueError: http status code
    """

    logger.info(f"function => retrieve_memory_graph_account() = account: {account}")

    jwt_token = context.get("jwt") if context else None
    if not jwt_token:
        logger.error( "No JWT provided, NOT AUTHORIZED, statuscode: 403")
        return "No JWT provided, NOT AUTHORIZED, statuscode: 403"
 
    logger.info(f"jwt_token: {jwt_token}")
    
    headers = {"Authorization": f"Bearer {jwt_token}"}   

    url = f"http://localhost:8001/person/account/{account}"

    async with aiohttp.ClientSession(timeout=session_timeout) as session:
        async with session.get(url, headers=headers) as resp:
            
            if resp.status == 200:
                data = await resp.json()
                return f"{data}"
            else:
                return f"Failed to get data from {account}, statuscode: {resp.status}"

@mcp.tool(name="store_memory_graph_card")
async def store_memory_graph_card(card: str, account: str, relation: str, context: dict = None) -> str:
    """
    Store the CARD its relation with ACCOUNT in memory graph account

    Args:
        - card: card identificator
        - account: account identificator
        - relations: relation between card and account, this relation MUST BE 'ISSUED'
    Response:
        - card: card identificator
        - account: account identificator
        - relations: relation between card and account
    Raises:
        - valueError: http status code
    """

    logger.info(f"function => store_memory_graph_card() = card: {card} account: {account} relation: {relation}")

    payload = {
        "nodes": {
            "card": {
                "card_id": card
            },
            "account": {
                "account_id": account
                }
            },
        "relations": {
            "description": relation
        },
    }

    jwt_token = context.get("jwt") if context else None
    if not jwt_token:
        logger.error( "No JWT provided, NOT AUTHORIZED, statuscode: 403")
        return "No JWT provided, NOT AUTHORIZED, statuscode: 403"
 
    logger.info(f"jwt_token: {jwt_token}")
    
    headers = {"Authorization": f"Bearer {jwt_token}"}   
    
    url = f"http://localhost:8001/graph"

    async with aiohttp.ClientSession(timeout=session_timeout) as session:
        async with session.post(url, headers=headers, json=payload) as resp:
            
            if resp.status == 200:
                data = await resp.json()
                return f"{data}"
            else:
                return f"Failed to post data {account}, statuscode: {resp.status}"

@mcp.tool(name="store_memory_graph_card_payment")
async def store_memory_graph_card_payment(card: str, payment: str, relation: str, context: dict = None) -> str:
    """
    Store the PAYMENT its relation with CARD in memory graph account

    Args:
        - card: card identificator
        - payment: payment identificator
        - relations: relation between card and payment, this relation MUST BE 'PAY'
    Response:
        - card: card identificator
        - payment: payment identificator
        - relations: relation between card and account
    Raises:
        - valueError: http status code
    """

    logger.info(f"function => store_memory_graph_card_payment() = card: {card} account: {payment} relation: {relation}")

    payload = {
        "nodes": {
            "card": {
                "card_id": card
            },
            "payment": {
                "payment_id": payment
                }
            },
        "relations": {
            "description": relation
        },
    }

    jwt_token = context.get("jwt") if context else None
    if not jwt_token:
        logger.error( "No JWT provided, NOT AUTHORIZED, statuscode: 403")
        return "No JWT provided, NOT AUTHORIZED, statuscode: 403"
 
    logger.info(f"jwt_token: {jwt_token}")
    
    headers = {"Authorization": f"Bearer {jwt_token}"}   
    
    url = f"http://localhost:8001/graph"

    async with aiohttp.ClientSession(timeout=session_timeout) as session:
        async with session.post(url, headers=headers, json=payload) as resp:
            
            if resp.status == 200:
                data = await resp.json()
                return f"{data}"
            else:
                return f"Failed to post data {account}, statuscode: {resp.status}"




if __name__ == "__main__":
    print("-" * 45)
    print(f"CODE SERVER {HOST}:{PORT}")
    print("-" * 45)
    
    mcp.run(transport="streamable-http")    