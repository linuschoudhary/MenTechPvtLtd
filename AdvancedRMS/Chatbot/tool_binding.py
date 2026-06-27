from langchain.agents import create_agent
from langchain_ollama import ChatOllama
from langchain_mcp_adapters.client import MultiServerMCPClient
import os
from langgraph.checkpoint.memory import InMemorySaver

memory = InMemorySaver()

async def build_agent(user_token:str):
    agent_env=os.environ.copy()
    agent_env["USER_AUTH_TOKEN"]=user_token

    client = MultiServerMCPClient(
        {
            "fastapi_tools": {
                "command": "python",
                "args": ["-m", "MCP.mcpserver"],
                "transport": "stdio",
                "env":agent_env,
            }
        }
    )

    tools = await client.get_tools()
    print("Tools Loaded:",[t.name for t in tools])
    agent = create_agent(
        model=ChatOllama(
            model="qwen3.5:4b",
            num_ctx=32768, #or 64000 for higher context size.
            temperature=0
        ),
        tools=tools,
        checkpointer=memory
    )

    return agent