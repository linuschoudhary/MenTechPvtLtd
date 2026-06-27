# from fastmcp import FastMCP
# from main import app

# mcp = FastMCP.from_fastapi(
#     app=app,
#     name="FASTAPI TOOLS"
# )

# if __name__ == "__main__":
#     mcp.run()


import os
from fastmcp import FastMCP
from main import app

from Authentication.oauth2 import oauth2_scheme

def mcp_token_extractor():
    token = os.environ.get("USER_AUTH_TOKEN")
    if not token:
        return None 
    return token

app.dependency_overrides[oauth2_scheme] = mcp_token_extractor

mcp = FastMCP.from_fastapi(
    app=app,
    name="FASTAPI TOOLS"
)

if __name__ == "__main__":
    mcp.run()