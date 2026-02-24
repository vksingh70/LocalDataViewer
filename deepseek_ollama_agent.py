import os
import asyncio
from typing import Annotated, TypedDict
from dotenv import load_dotenv

# 1. Swapped Google for Ollama
from langchain_ollama import ChatOllama
from langchain_core.messages import BaseMessage, HumanMessage
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode

load_dotenv()

class AgentState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]

async def main():
    # 2. Configure Local DeepSeek-R1
    # Using 32b for your M3 Max 36GB; drop to 14b if you hit memory pressure
    llm = ChatOllama(
    model="MFDoom/deepseek-r1-tool-calling:32b", # Updated model tag
    temperature=0,
    num_ctx=8192,
)

    servers = {
        "local_data": {
            "command": "mcpmon", 
            "args": ["python", "my_local_data.py"],
            "transport": "stdio"
        }
    }

    # Initialize MCP Client
    client = MultiServerMCPClient(servers)
    
    # 3. Connect and Bind Tools
    # We must await the tool retrieval before binding
    tools = await client.get_tools()
    print(f"✅ Local Connection successful! Found tools: {[t.name for t in tools]}")
    
    # DeepSeek-R1 works best when tools are explicitly bound
    model_with_tools = llm.bind_tools(tools)

    # Graph Logic
    def call_model(state: AgentState):
        response = model_with_tools.invoke(state["messages"])
        return {"messages": [response]}

    tool_node = ToolNode(tools)

    def should_continue(state: AgentState):
        last_message = state["messages"][-1]
        return "tools" if last_message.tool_calls else END

    workflow = StateGraph(AgentState)
    workflow.add_node("agent", call_model)
    workflow.add_node("tools", tool_node)
    workflow.set_entry_point("agent")
    workflow.add_conditional_edges("agent", should_continue)
    workflow.add_edge("tools", "agent")
    app = workflow.compile()

    # 4. Interactive Loop
    print("\n--- Local DeepSeek-R1 MCP Agent Active ---")
    print("Type 'exit' to quit.")
    
    while True:
        # Use sync input in an async loop carefully or use aioconsole
        user_input = input("\nQuery: ")
        if user_input.lower() in ["exit", "quit"]:
            break

        async for event in app.astream(
            {"messages": [HumanMessage(content=user_input)]},
            stream_mode="values"
        ):
            if "messages" in event:
                msg = event["messages"][-1]
                
                if msg.content:
                    # DeepSeek-R1 often includes <think> tags. 
                    # This prints the reasoning and the final answer.
                    print(f"\n[DeepSeek]: {msg.content}")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nAgent shut down.")