import os
import logging
import aiohttp

from datetime import datetime

from mcp.server.fastmcp import FastMCP

PORT = os.getenv("PORT", "9002")
HOST = os.getenv("HOST", "127.0.0.1")
SESSION_TIMEOUT = 600 

mcp = FastMCP(name="code_server",        
        host=HOST,
        port=PORT,
        debug=True,
    )

session_timeout = aiohttp.ClientTimeout(total=SESSION_TIMEOUT)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# truncate logging
class TruncatingFormatter(logging.Formatter):
    def __init__(self, fmt=None, datefmt=None, style='%', max_msg_length=100):
        super().__init__(fmt, datefmt, style)
        self.max_msg_length = max_msg_length

    def format(self, record):
        if len(record.msg) > self.max_msg_length:
            record.msg = record.msg[:self.max_msg_length] + "..."
        return super().format(record)

handler = logging.StreamHandler()
formatter = TruncatingFormatter('%(asctime)s - %(levelname)s - %(message)s', max_msg_length=250)
handler.setFormatter(formatter)
logger.addHandler(handler)

# -----------------------------------------------------
# Gateway_GRPC
# -----------------------------------------------------
@mcp.tool(name="gateway_grpc_healthy")
async def gateway_grpc_healthy(context: dict = None) -> str:
    """
    Check the healthy status of GATEWAY_GRPC service.
    
    Args:
        - context: context with a jwt embedded.
    Response:
        - content: all information about GATEWAY_GRPC service healthy status and enviroment variables.
    Raises:
        - valueError: http status code.
    """

    print('\033[31m =.=.= \033[0m' * 15)
    logger.info(f"function => gateway_grpc_healthy()")

    jwt_token = context.get("jwt") if context else None
    if not jwt_token:
        message_error = "No JWT provided, NOT AUTHORIZED, statuscode: 403"
        logger.error("message_error")
        return message_error
 
    logger.info(f"jwt_token: {jwt_token}")
    
    headers = {"Authorization": f"Bearer {jwt_token}"}                  
    url = f"https://go-global-apex.architecture.caradhras.io/gateway-grpc/info"
    
    async with aiohttp.ClientSession(timeout=session_timeout) as session:
        async with session.get(url, headers=headers) as resp:
            if resp.status == 200:
                data = await resp.json()
                
                logger.info(f"data: {data}")
                
                return f"{data}"
            else:
                message_error = f"Failed to fetch gateway_grp healthy, statuscode: {resp.status}"
                logger.error(message_error)
                return message_error
  
# -----------------------------------------------------          
# Payment_Gateway
# -----------------------------------------------------
@mcp.tool(name="payment_healthy")
async def payment_healthy(context: dict = None) -> str:
    """
    Check the healthy status PAYMENT service.

    Args:
        - context: context with a jwt embedded.
    Response:
        - content: all information about PAYMENT service healthy status and enviroment variables.
    Raises:
        - valueError: http status code.
    """

    print('\033[31m =.=.= \033[0m' * 15)
    logger.info(f"function => payment_healthy()")
    
    jwt_token = context.get("jwt") if context else None
    if not jwt_token:
        message_error = "No JWT provided, NOT AUTHORIZED, statuscode: 403"
        logger.error("message_error")
        return message_error
 
    logger.info(f"jwt_token: {jwt_token}")
    
    headers = {"Authorization": f"Bearer {jwt_token}"}                  
    url = f"https://go-global-apex.architecture.caradhras.io/payment-gateway/info"
    
    async with aiohttp.ClientSession(timeout=session_timeout) as session:
        async with session.get(url, headers=headers) as resp:
            if resp.status == 200:
                data = await resp.json()
                                
                logger.info(f"data: {data}")
                
                return f"{data}"
            else:
                message_error = f"Failed to fetch payment_gateway healthy, statuscode: {resp.status}"
                logger.error(message_error)
                return message_error

@mcp.tool(name="get_card_payment")
async def get_card_payment(card: str, 
                           date: str, 
                           context: dict = None) -> str:
    """
    Get all PAYMENT did by a card such as payments amount, currency, payment date, card number used to pay, mcc (merchant), etc.

    Args:
        - card: Exactly 12 digits split into 4 groups of 3 digits each.
        - date: search date in format YYYY-MM-DD.
        - context: context with a jwt embedded.        
    Response:
        - list: A list of payments with information such as card type, card model, payment amount, terminal, payment status and payment date.
    Raises:
        - valueError: http status code.
    """

    print('\033[31m =.=.= \033[0m' * 15)
    logger.info(f"function => get_card_payment() card:{card} date:{date} ")
    
    jwt_token = context.get("jwt") if context else None
    if not jwt_token:
        message_error = "No JWT provided, NOT AUTHORIZED, statuscode: 403"
        logger.error("message_error")
        return message_error

    logger.info(f"jwt_token: {jwt_token}")
    
    headers = {"Authorization": f"Bearer {jwt_token}"}                  
    url = f"https://go-global-apex.architecture.caradhras.io/payment-gateway/payment?card={card}&after={date}"
    
    async with aiohttp.ClientSession(timeout=session_timeout) as session:
        async with session.get(url, headers=headers) as resp:
            if resp.status == 200:
                data = await resp.json()

                logger.info(f"data: {data}")
                
                return f"{data}"
            else:
                message_error = f"Failed to fetch payment {card} : {date}, statuscode: {resp.status}"
                logger.error(message_error)
                return message_error

# -----------------------------------------------------                        
# Limit
# -----------------------------------------------------
@mcp.tool(name="limit_healthy")
async def limit_healthy(context: dict = None) -> str:
    """
    Check the healthy status LIMIT service.

    Args:
        - context: context with a jwt embedded.
    Response:
        - content: all information about LIMIT service health status and enviroment variables.
    Raises:
        - valueError: http status code.
    """

    print('\033[31m =.=.= \033[0m' * 15) 
    logger.info(f"function => limit_healthy()")

    jwt_token = context.get("jwt") if context else None
    if not jwt_token:
        message_error = "No JWT provided, NOT AUTHORIZED, statuscode: 403"
        logger.error("message_error")
        return message_error
 
    logger.debug(f"jwt_token: {jwt_token}")
    
    headers = {"Authorization": f"Bearer {jwt_token}"}                   
    url = f"https://go-global.architecture.caradhras.io/limit/info"
    
    async with aiohttp.ClientSession(timeout=session_timeout) as session:
        async with session.get(url, headers=headers) as resp:
            if resp.status == 200:
                data = await resp.json()

                logger.info(f"data: {data}")

                return f"{data}"
            else:
                message_error = f"Failed to fetch limit healthy, statuscode: {resp.status}"
                logger.error(message_error)
                return message_error

# -----------------------------------------------------            
# Card
# -----------------------------------------------------
@mcp.tool(name="card_healthy")
async def card_healthy(context: dict = None) -> str:
    """
    Check the healthy status CARD service.

    Args:
        - context: context with a jwt embedded.
    Response:
        - content: all information about CARD service health status and enviroment variables.
    Raises:
        - valueError: http status code.
    """

    print('\033[31m =.=.= \033[0m' * 15)
    logger.info(f"function => card_healthy()")

    jwt_token = context.get("jwt") if context else None
    if not jwt_token:
        message_error = "No JWT provided, NOT AUTHORIZED, statuscode: 403"
        logger.error("message_error")
        return message_error
 
    logger.info(f"jwt_token: {jwt_token}")
    
    headers = {"Authorization": f"Bearer {jwt_token}"}                  
    url = f"https://go-global.architecture.caradhras.io/card/info"
    
    async with aiohttp.ClientSession(timeout=session_timeout) as session:
        async with session.get(url, headers=headers) as resp:
            if resp.status == 200:
                data = await resp.json()
                logger.info(f"data: {data}")
                return f"{data}"
            else:
                message_error = f"Failed to fetch card healthy, statuscode: {resp.status}"
                logger.error(message_error)
                return message_error
            
@mcp.tool(name="get_card")
async def get_card(card: str, 
                   context: dict = None) -> str:
    """
    Get all CARD details such as card number, atc, card type, card model (CREDIT or DEBIT), card status from a given card number.

    Args:
        - card: Exactly 12 digits split into 4 groups of 3 digits each.
        - context: context with a jwt embedded.
    Response:
        - card: all card information.
    Raises:
        - valueError: http status code.
    """

    print('\033[31m =.=.= \033[0m' * 15)
    logger.info(f"function => get_card() = card:{card}")

    jwt_token = context.get("jwt") if context else None
    if not jwt_token:
        message_error = "No JWT provided, NOT AUTHORIZED, statuscode: 403"
        logger.error("message_error")
        return message_error
 
    logger.info(f"jwt_token: {jwt_token}")
    
    headers = {"Authorization": f"Bearer {jwt_token}"}                  
    url = f"https://go-global.architecture.caradhras.io/card/card/{card}"
    
    async with aiohttp.ClientSession(timeout=session_timeout) as session:
        async with session.get(url, headers=headers) as resp:
            if resp.status == 200:
                data = await resp.json()
                logger.info(f"data: {data}")
                return f"{data}"
            else:
                message_error = f"Failed to fetch card from {card}, statuscode: {resp.status}"
                logger.error(message_error)
                return message_error

@mcp.tool(name="create_card")
async def create_card(card: str,
                      account: str,
                      holder: str,
                      type: str,
                      model: str,
                      status: str,
                      context: dict = None) -> str:
    """
    Create a card.

    Args:
        - card: Exactly 12 digits split into 4 groups of 3 digits each.
        - account: account identificator (account_id) associated with a card. A account pattern is AAC-####.
        - holder: card holder name.
        - type: CREDIT or DEBIT, the default value is CREDIT.
        - model: CHIP or VIRTUAL, the default value is CHIP.
        - status: ISSUED or PEDING, the default value is ISSUED.
        - context: context with a jwt embedded.        
    Response:
        - card: a card created. 
    Raises:
        - valueError: http status code.
    """

    print('\033[31m =.=.= \033[0m' * 15)
    logger.info(f"function => create_account() = card: {card} account: {account}")

    jwt_token = context.get("jwt") if context else None
    if not jwt_token:
        message_error = "No JWT provided, NOT AUTHORIZED, statuscode: 403"
        logger.error("message_error")
        return message_error
 
    logger.info(f"jwt_token: {jwt_token}")

    payload = {
        "card_number": card,
        "account_id": account,
        "holder": holder,
        "type": type,
        "model": model,
        "status": status
    }

    headers = {"Authorization": f"Bearer {jwt_token}"}                  
    url = f"https://go-global.architecture.caradhras.io/card/card"
    
    async with aiohttp.ClientSession(timeout=session_timeout) as session:
        async with session.post(url, headers=headers, json=payload) as resp:
            if resp.status == 200:
                data = await resp.json()

                logger.info(f"data: {data}")

                return f"{data}"
            else:
                message_error = f"Failed to create card {card}, statuscode: {resp.status}"
                logger.error(message_error)
                return message_error

# -----------------------------------------------------
# Account
# -----------------------------------------------------
@mcp.tool(name="account_healthy")
async def account_healthy(context: dict = None) -> str:
    """
    Check the healthy status ACCOUNT service.

    Args:
        - context: context with a jwt embedded.
    Response:
        - content: all information about ACCOUNT service health status and enviroment variables.
    Raises:
        - valueError: http status code.
    """

    print('\033[31m =.=.= \033[0m' * 15)
    logger.info(f"function => account_healthy()")

    jwt_token = context.get("jwt") if context else None
    if not jwt_token:
        message_error = "No JWT provided, NOT AUTHORIZED, statuscode: 403"
        logger.error("message_error")
        return message_error
 
    logger.info(f"jwt_token: {jwt_token}")
    
    headers = {"Authorization": f"Bearer {jwt_token}"}                
    url = f"https://go-global-apex.architecture.caradhras.io/account/info"
    
    async with aiohttp.ClientSession(timeout=session_timeout) as session:
        async with session.get(url, headers=headers) as resp:
            if resp.status == 200:
                data = await resp.json()
                
                logger.info(f"data: {data}")
                
                return f"{data}"
            else:
                message_error = f"Failed to fetch account healthy, statuscode: {resp.status}"
                logger.error(message_error)
                return message_error
           
@mcp.tool(name="get_account")
async def get_account(account: str, 
                      context: dict = None) -> str:
    """
    Get account details from a given account id.
    All accounts has a pattern ACC-### or ACC-###.### 

    Args:
        - account: account identificator (account id).
        - context: context with a jwt embedded.        
    Response:
        - account: account details such as account id (account_id), person id (owner account), date of creation (created_at).
    Raises:
        - valueError: http status code.
    """

    print('\033[31m =.=.= \033[0m' * 15)
    logger.info(f"function => get_account() = account: {account}")

    jwt_token = context.get("jwt") if context else None
    if not jwt_token:
        message_error = "No JWT provided, NOT AUTHORIZED, statuscode: 403"
        logger.error("message_error")
        return message_error
 
    logger.info(f"jwt_token: {jwt_token}")
    
    headers = {"Authorization": f"Bearer {jwt_token}"}                  
    url = f"https://go-global-apex.architecture.caradhras.io/account/get/{account}"
    
    async with aiohttp.ClientSession(timeout=session_timeout) as session:
        async with session.get(url, headers=headers) as resp:
            if resp.status == 200:
                data = await resp.json()

                logger.info(f"data: {data}")

                return f"{data}"
            else:
                message_error = f"Failed to fetch account from {account}, statuscode: {resp.status}"
                logger.error(message_error)
                return message_error

@mcp.tool(name="create_account")
async def create_account(account: str,
                         person: str,
                         context: dict = None) -> str:
    """
    Create an account.

    The account has a pattern ACC-### or ACC-###.### 
    The person has a pattern P-### or P-###.###

    Args:
        - account: account identificator (account_id).
        - person: person identificator (person_id).
        - context: context with a jwt embedded.        
    Response:
        - account: account details such as account id (account_id), person id (owner account), date of creation (created_at).
    Raises:
        - valueError: http status code.
    """

    print('\033[31m =.=.= \033[0m' * 15)
    logger.info(f"function => create_account() = account: {account} person: {person}")

    jwt_token = context.get("jwt") if context else None
    if not jwt_token:
        message_error = "No JWT provided, NOT AUTHORIZED, statuscode: 403"
        logger.error("message_error")
        return message_error
 
    logger.info(f"jwt_token: {jwt_token}")

    payload = {
        "account_id": account,
        "person_id": person
    }

    headers = {"Authorization": f"Bearer {jwt_token}"}                  
    url = f"https://go-global-apex.architecture.caradhras.io/account/add"
    
    async with aiohttp.ClientSession(timeout=session_timeout) as session:
        async with session.post(url, headers=headers, json=payload) as resp:
            if resp.status == 200:
                data = await resp.json()

                logger.info(f"data: {data}")

                return f"{data}"
            else:
                message_error = f"Failed to create account {account}, statuscode: {resp.status}"
                logger.error(message_error)
                return message_error

@mcp.tool(name="get_account_from_person")
async def get_account_from_person(person: str, 
                                  context: dict = None) -> str:
    """
    Get all accounts associated/belongs a given person (person_id).
    The person has a pattern P-### or P-###.###

    Args:
        - person: person identificator (person_id).
        - context: context with a jwt embedded.
    Response:
        - list: List of accounts owned/belongs by a given person (person id).
    Raises:
        - valueError: http status code.
    """

    print('\033[31m =.=.= \033[0m' * 15)
    logger.info(f"function => get_account_from_person() = person: {person}")

    jwt_token = context.get("jwt") if context else None
    if not jwt_token:
        message_error = "No JWT provided, NOT AUTHORIZED, statuscode: 403"
        logger.error("message_error")
        return message_error
 
    logger.info(f"jwt_token: {jwt_token}")
    
    headers = {"Authorization": f"Bearer {jwt_token}"}   
    url = f"https://go-global-apex.architecture.caradhras.io/account/list/{person}"
    
    async with aiohttp.ClientSession(timeout=session_timeout) as session:
        async with session.get(url, headers=headers) as resp:

            if resp.status == 200:
                data = await resp.json()
                
                logger.info(f"data: {data}")
                
                return f"{data}"
            else:
                message_error = f"Failed to fetch account from {person}, statuscode: {resp.status}"
                logger.error(message_error)
                return message_error
         
# -----------------------------------------------------
# Ledger Account bank statement
# -----------------------------------------------------
@mcp.tool(name="ledger_healthy")
async def ledger_healthy(context: dict = None) -> str:
    """
    Check the healthy status account LEDGER service.

    Args:
        - context: context with a jwt embedded.    
    Response:
        - content: all information about LEDGER service health status and enviroment variables.
    Raises:
        - valueError: http status code.
    """

    print('\033[31m =.=.= \033[0m' * 15)
    logger.info(f"function => ledger_healthy()")
    
    jwt_token = context.get("jwt") if context else None
    if not jwt_token:
        message_error = "No JWT provided, NOT AUTHORIZED, statuscode: 403"
        logger.error("message_error")
        return message_error
 
    logger.info(f"jwt_token: {jwt_token}")
    
    headers = {"Authorization": f"Bearer {jwt_token}"}                  
    url = f"https://go-global-apex.architecture.caradhras.io/ledger/info"
    
    async with aiohttp.ClientSession(timeout=session_timeout) as session:
        async with session.get(url, headers=headers) as resp:
            if resp.status == 200:
                data = await resp.json()
                logger.info(f"data: {data}")
                return f"{data}"
            else:
                message_error = f"Failed to fetch ledger healthy, statuscode: {resp.status}"
                logger.error(message_error)
                return message_error
            
@mcp.tool(name="get_account_statement")
async def get_account_statement(account: str, 
                                context: dict = None) -> str:
    """
    Get LEDGER informations such as account activity, account balances and statements from a given account (account id).

    Args:
        - account: account identificator (account_id).
        - context: context with a jwt embedded.    
    Response:
        - list: A list of bank statement, financial moviment, account activity and balance summary.
    Raises:
        - valueError: http status code.
    """

    print('\033[31m =.=.= \033[0m' * 15)
    logger.info(f"function => get_account_statement() = account: {account}")
    
    jwt_token = context.get("jwt") if context else None
    if not jwt_token:
        message_error = "No JWT provided, NOT AUTHORIZED, statuscode: 403"
        logger.error("message_error")
        return message_error
 
    logger.info(f"jwt_token: {jwt_token}")
    
    headers = {"Authorization": f"Bearer {jwt_token}"}   
    url = f"https://go-global-apex.architecture.caradhras.io/ledger/movimentStatement/{account}"
    
    async with aiohttp.ClientSession(timeout=session_timeout) as session:
        async with session.get(url, headers=headers) as resp:
            
            if resp.status == 200:
                data = await resp.json()

                logger.info(f"data: {data}")

                return f"{data}"
            else:
                message_error = f"Failed to fetch ledger account from {account}, statuscode: {resp.status}"
                logger.error(message_error)
                return message_error

@mcp.tool(name="create_moviment_transaction")
async def create_moviment_transaction(account: str,
                                      type: str,
                                      currency: str,
                                      amount: float,
                                      context: dict = None) -> str:
    """
    Create a transaction from a given account (account id).

    Args:
        - account: account identificator (account_id) associated. A account pattern is ACC-###.### or ACC-###.
        - type: DEPOSIT or WITHDRAW, the default value is DEPOSIT.
        - currency: transaction currency as BRL, the default value is BRL.
        - amount: transaction amount. 
    Response:
         transaction: all transaction information.
    Raises:
        - valueError: http status code.
    """

    print('\033[31m =.=.= \033[0m' * 15)
    logger.info(f"function => create_moviment_transaction() = account: {account}: {type} : {currency} : {amount}")
    
    jwt_token = context.get("jwt") if context else None
    if not jwt_token:
        message_error = "No JWT provided, NOT AUTHORIZED, statuscode: 403"
        logger.error("message_error")
        return message_error
 
    logger.info(f"jwt_token: {jwt_token}")

    payload = {
        "account_from": {
                "account_id": account
        },
        "type" : type,
        "currency": currency,
        "amount": amount
    }

    logger.info(f"payload: {payload}")

    headers = {"Authorization": f"Bearer {jwt_token}"} 

    url = f"https://go-global.architecture.caradhras.io/ledger/movimentTransaction"
    
    async with aiohttp.ClientSession(timeout=session_timeout) as session:
        async with session.post(url, headers=headers, json=payload) as resp:
            
            if resp.status == 200:
                data = await resp.json()

                logger.info(f"data: {data}")

                return f"{data}"
            else:
                message_error = f"Failed to create ledger a transaction moviment from {account}, statuscode: {resp.status}"
                logger.error(message_error)
                return message_error
            
# ------------------------------------------------------------------- #
# Memory
# ------------------------------------------------------------------- #
@mcp.tool(name="retrieve_memory_graph_account")
async def retrieve_memory_graph_account(account: str, 
                                        context: dict = None) -> str:
    """
    Retrieve all ACCOUNT memories from knowledge base graph database.

    Args:
        - account: account id.
        - context: context with a jwt embedded.    
    Response:
        - list: list of person_id (owner) of account.
    Raises:
        - valueError: http status code.
    """

    print('\033[1;33m =.=.= \033[0m' * 15)
    logger.info(f"function => retrieve_memory_graph_account() = account: {account}")

    jwt_token = context.get("jwt") if context else None
    if not jwt_token:
        message_error = "No JWT provided, NOT AUTHORIZED, statuscode: 403"
        logger.error("message_error")
        return message_error
 
    logger.info(f"jwt_token: {jwt_token}")
    
    headers = {"Authorization": f"Bearer {jwt_token}"}   

    url = f"http://localhost:8001/person/account/{account}"

    async with aiohttp.ClientSession(timeout=session_timeout) as session:
        async with session.get(url, headers=headers) as resp:
            
            if resp.status == 200:
                data = await resp.json()

                logger.info(f"data: {data}")
            
                return f"{data}"
            else:
                message_error = f"Failed to get data from {account}, statuscode: {resp.status}"
                logger.error(message_error)
                return message_error

@mcp.tool(name="store_account_memory")
async def store_account_memory(person: str,
                               account: str,
                               relation: str = None,
                               context: dict = None) -> str:
    """
    Store the ACCOUNT and its relation with PERSON in knowledge base graph database.

    Args:
        - account: account identificator (account_id).
        - person: person identificator (person_id).
        - relations: relation between account and person, this relation MUST BE 'HAS'.
        - context: context with a jwt embedded.
    Response:
        - account: account_id.
        - person: person_id.
        - relations: relation between account and person.
    Raises:
        - valueError: http status code.
    """

    print('\033[1;33m =.=.= \033[0m' * 15)
    logger.info(f"function => store_account_memory() = person: {person} account: {account} relation: {relation}")

    # set relation
    if relation is None:
        relation = 'HAS'

    # set properties
    properties = {}
    properties["create_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

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
            "description": relation,
            "properties": properties
        },
    }

    logger.info(f"payload: {payload}")

    jwt_token = context.get("jwt") if context else None
    #if not jwt_token:
    #    logger.error( "No JWT provided, NOT AUTHORIZED, statuscode: 403")
    #    return "No JWT provided, NOT AUTHORIZED, statuscode: 403"

    logger.info(f"jwt_token: {jwt_token}")
    
    headers = {"Authorization": f"Bearer {jwt_token}"}   
    url = f"http://localhost:8001/graph"

    async with aiohttp.ClientSession(timeout=session_timeout) as session:
        async with session.post(url, headers=headers, json=payload) as resp:
            
            if resp.status == 200:
                data = await resp.json()
                logger.debug(f"data: {data}")
                return f"{data}"
            else:
                message_error = f"Failed to post data {account}, statuscode: {resp.status}"
                logger.error(message_error)
                return message_error
            
@mcp.tool(name="store_card_memory")
async def store_card_memory(card: str,
                            type: str,
                            model: str,
                            account: str, 
                            relation: str = None,
                            context: dict = None) -> str:
    """
    Store the CARD and its relation with ACCOUNT in knowledge base graph database.

    Args:
        - card: card number.
        - type: card type (credit or debit)
        - model: card model (chip)         
        - account: account identificator (account_id).
        - relations: relation between card and account, this relation MUST BE 'ISSUED'.
        - context: context with a jwt embedded.
    Response:
        - card: card id, type, model.
        - account: account identificator (account_id).
        - relations: relation between card and account.
    Raises:
        - valueError: http status code.
    """

    print('\033[1;33m =.=.= \033[0m' * 15)
    logger.info(f"function => store_card_memory() = card: {card}:{type}:{model} account: {account} relation: {relation}")

    # set relation
    if relation is None:
        relation = 'ISSUED'

    # set properties
    properties = {}
    properties["create_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    payload = {
        "nodes": {
            "card": {
                "card_id": card,
                "type": type,
                "model": model,
            },
            "account": {
                "account_id": account
                }
            },
        "relations": {
            "description": relation,
            "properties": properties
        },
    }

    logger.info(f"payload: {payload}")

    jwt_token = context.get("jwt") if context else None
    #if not jwt_token:
    #    logger.error( "No JWT provided, NOT AUTHORIZED, statuscode: 403")
    #    return "No JWT provided, NOT AUTHORIZED, statuscode: 403"
 
    logger.info(f"jwt_token: {jwt_token}")
    
    headers = {"Authorization": f"Bearer {jwt_token}"}   
    
    url = f"http://localhost:8001/graph"

    async with aiohttp.ClientSession(timeout=session_timeout) as session:
        async with session.post(url, headers=headers, json=payload) as resp:
            
            if resp.status == 200:
                data = await resp.json()

                logger.info(f"data: {data}")

                return f"{data}"
            else:
                message_error = f"Failed to post data {account}, statuscode: {resp.status}"
                logger.error(message_error)
                return message_error

@mcp.tool(name="store_payment_memory")
async def store_payment_memory(card: str, 
                                payment: str,
                                mcc: str,
                                currency: str,
                                amount: str, 
                                payment_date: str,
                                relation: str = None, 
                                status:str = None,
                                context: dict = None) -> str:
    """
    Store the PAYMENT ans its relation with CARD in knowledge base graph database.
    
    Args:
        - card: card number or card id.
        - payment: payment id.
        - currency: payment currency, eg: BRL.
        - amount: payment amount.
        - payment_date: date of payment.
        - status: payment status.
        - relations: relation between card and account, this relation MUST BE 'PAY'.
        - context: context with a jwt embedded.
    Response:
        - payment: payment id, currency, amount, mcc, date payment, status.
        - card: card id.
        - relations: relation between card and account.
    Raises:
        - valueError: http status code.
    """

    print('\033[1;33m =.=.= \033[0m' * 15)
    logger.info(f"function => store_payment_memory() = card:{card} payment:{payment} {payment_date} {mcc} {currency} {amount} relation:{relation} status:{status}")

    # set relation
    if relation is None:
        relation = 'PAY'

    # set properties
    properties = {}
    properties["create_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if status:
        properties["status"] = status

    payload = {
        "nodes": {
            "card": {
                "card_id": card
            },
            "payment": {
                "payment_id": payment,
                "date": payment_date,
                "currency": currency,
                "amount": amount
                }
            },
        "relations": {
            "description": relation,
            "properties": properties
        },
    }

    logger.info(f"payload: {payload}")
    
    jwt_token = context.get("jwt") if context else None
    #if not jwt_token:
    #    logger.error( "No JWT provided, NOT AUTHORIZED, statuscode: 403")
    #    return "No JWT provided, NOT AUTHORIZED, statuscode: 403"
 
    logger.info(f"jwt_token: {jwt_token}")
    
    headers = {"Authorization": f"Bearer {jwt_token}"}   
    url = f"http://localhost:8001/graph"

    async with aiohttp.ClientSession(timeout=session_timeout) as session:
        async with session.post(url, headers=headers, json=payload) as resp:
            
            if resp.status == 200:
                data = await resp.json()
                
                logger.info(f"data: {data}")

                return f"{data}"
            else:
                message_error = f"Failed to post data {card}, statuscode: {resp.status}"
                logger.error(message_error)
                return message_error

# ------------------------------------------------------------------- #
# Main
# ------------------------------------------------------------------- #
if __name__ == "__main__":
    print("-" * 45)
    print(f"CODE SERVER {HOST}:{PORT}")
    print("-" * 45)
    
    mcp.run(transport="streamable-http")    