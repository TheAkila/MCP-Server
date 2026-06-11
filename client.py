import os
import asyncio
from dotenv import load_dotenv
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_openai import ChatOpenAI
from langchain.agents import create_agent

load_dotenv()

MCP_SERVERS = {
    "file-service": {
        "url": "http://localhost:8000/mcp",
        "transport": "streamable_http",
    },
    "calculator-service": {
        "url": "http://localhost:8001/mcp",
        "transport": "streamable_http",
    },
}


async def run_chat():
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is not set (use a .env file or export it)")
    os.environ["OPENAI_API_KEY"] = api_key

    client = MultiServerMCPClient(MCP_SERVERS)
    tools = await client.get_tools()

    model = ChatOpenAI(model="gpt-4.1-mini", temperature=0)
    agent = create_agent(model, tools)

    while True:
        user_text = input("You: ").strip()
        if not user_text:
            continue
        if user_text.lower() in {"exit", "quit"}:
            break

        result = await agent.ainvoke({"messages": [{"role": "user", "content": user_text}]})
        assistant_text = result["messages"][-1].content
        print(f"AI: {assistant_text}\n")


if __name__ == "__main__":
    asyncio.run(run_chat())
