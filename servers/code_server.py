import os
import json
import aiohttp
from mcp.server.fastmcp import FastMCP

PORT = os.getenv("PORT", "9002")
HOST = os.getenv("HOST", "127.0.0.1")

mcp = FastMCP(name="code_server",        
        host=HOST,
        port=PORT,
        debug=True,
    )

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
    headers = {"Authorization": "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl91c2UiOiJhY2Nlc3MiLCJpc3MiOiJnby1vYXV0aC1sYW1iZGEiLCJ2ZXJzaW9uIjoiMi4xIiwiand0X2lkIjoiZTYxODAxNTItMDQzMC00ZTYwLWI1ZWYtYzAwOGI3MzRlZDJkIiwidXNlcm5hbWUiOiJ1c2VyLTAzIiwidGllciI6InRpZXItMDMiLCJhcGlfYWNjZXNzX2tleSI6IkFQSV9BQ0NFU1NfS0VZX1VTRVJfMDMiLCJzY29wZSI6WyJ0ZXN0LnJlYWQiLCJ0ZXN0LndyaXRlIiwiYWRtaW4iXSwiZXhwIjoxNzU4MTIzMDc0fQ.IKRV7WHrZ79mCkefWnh-MNqyE-4Lf1s6Q1Iabhw_iQC2Fb6W7AYzBdTdMCiTa8SKHzi8-lJ6bkIBa3mJc46PIn_ctRBYiqAdfVCHJ1nCX4ZcKWXq0tKF7SzTf6rYDUQdfOHaEzA9u5EBvoKS3VI37r1TEcOKX10CgsOU0pfWkng3Q8UlvVtQt8_ykHg-c-S6wpS6j5_tr9MR9m4ysz9BCpDKhYPCFh7zY9hneZpA0cheGR43bl1QmR4x_qBodJzYH1Hr_3opXZBJhbVlBMJuKUw_PsgwaEpsbwAdkz00cK3uBld9EhOcld8r1ov9WBcgdDw6jLRb6nYPd5Juuq_LnPT1r6kI_0sgSp6M2StKykYTLbr7oYzk3YeK8ThqDOwC0cMyxQAGCCNigeLv-Jykr2rai4ZIUH70RjdV0tjphLF7UlB5VFlfuPIJfH0YYFoUbI_XqlV0RcHhl9s1bd4vBkfusNvriy2brJLf-yHvH3rxUQGYvRlWLPwd9MmbGXgll2CfcfMXY3qjT8sZwpUJ2KcQ6R5xI1OrD1vGRX4RSHsJihY0WyAI1gZmwuJoAeu8jQqeba94bsr3T6XDZ1FR6hsWsCYnd_MYVBb_U9bVjlvFWgqxlnCIGfz4lC1hQyTiIVXfNHNjleuEfhtNkw_wPiaMKx5u5uL4qXRxktxQG0E"}

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
    headers = {"Authorization": "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl91c2UiOiJhY2Nlc3MiLCJpc3MiOiJnby1vYXV0aC1sYW1iZGEiLCJ2ZXJzaW9uIjoiMi4xIiwiand0X2lkIjoiZTYxODAxNTItMDQzMC00ZTYwLWI1ZWYtYzAwOGI3MzRlZDJkIiwidXNlcm5hbWUiOiJ1c2VyLTAzIiwidGllciI6InRpZXItMDMiLCJhcGlfYWNjZXNzX2tleSI6IkFQSV9BQ0NFU1NfS0VZX1VTRVJfMDMiLCJzY29wZSI6WyJ0ZXN0LnJlYWQiLCJ0ZXN0LndyaXRlIiwiYWRtaW4iXSwiZXhwIjoxNzU4MTIzMDc0fQ.IKRV7WHrZ79mCkefWnh-MNqyE-4Lf1s6Q1Iabhw_iQC2Fb6W7AYzBdTdMCiTa8SKHzi8-lJ6bkIBa3mJc46PIn_ctRBYiqAdfVCHJ1nCX4ZcKWXq0tKF7SzTf6rYDUQdfOHaEzA9u5EBvoKS3VI37r1TEcOKX10CgsOU0pfWkng3Q8UlvVtQt8_ykHg-c-S6wpS6j5_tr9MR9m4ysz9BCpDKhYPCFh7zY9hneZpA0cheGR43bl1QmR4x_qBodJzYH1Hr_3opXZBJhbVlBMJuKUw_PsgwaEpsbwAdkz00cK3uBld9EhOcld8r1ov9WBcgdDw6jLRb6nYPd5Juuq_LnPT1r6kI_0sgSp6M2StKykYTLbr7oYzk3YeK8ThqDOwC0cMyxQAGCCNigeLv-Jykr2rai4ZIUH70RjdV0tjphLF7UlB5VFlfuPIJfH0YYFoUbI_XqlV0RcHhl9s1bd4vBkfusNvriy2brJLf-yHvH3rxUQGYvRlWLPwd9MmbGXgll2CfcfMXY3qjT8sZwpUJ2KcQ6R5xI1OrD1vGRX4RSHsJihY0WyAI1gZmwuJoAeu8jQqeba94bsr3T6XDZ1FR6hsWsCYnd_MYVBb_U9bVjlvFWgqxlnCIGfz4lC1hQyTiIVXfNHNjleuEfhtNkw_wPiaMKx5u5uL4qXRxktxQG0E"}

    url = f"https://go-global-apex.architecture.caradhras.io/ledger/movimentStatement/{account}"
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as resp:
            
            if resp.status == 200:
                data = await resp.json()
                return f"{data}"
            else:
                return f"Failed to fetch account from {account}, statuscode: {resp.status}"

if __name__ == "__main__":
    print("-" * 45)
    print(f"CODE SERVER {HOST}:{PORT}")
    print("-" * 45)
    
    mcp.run(transport="streamable-http")