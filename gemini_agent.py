import os
import asyncio
from typing import Annotated, TypedDict
from dotenv import load_dotenv

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import BaseMessage, HumanMessage
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode

load_dotenv()

class AgentState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]

async def main():
    # 1. Use the more active 2026 model
    llm = ChatGoogleGenerativeAI(
        model="gemini-3.1-pro-preview", 
        google_api_key=os.getenv("GOOGLE_API_KEY"),
        temperature=0
    )

    servers = {
        "local_data": {
            "command": "mcpmon", # Wrap your command in mcpmon
            "args": ["python", "my_local_data.py"],
            "transport": "stdio"
        }
    }

    
    client = MultiServerMCPClient(servers)
    
    # 2. Get tools and PRINT them to verify connection
    tools = await client.get_tools()
    print(f"✅ Connection successful! Found tools: {[t.name for t in tools]}")
    
    model_with_tools = llm.bind_tools(tools)

    # 3. Graph Logic
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

    # 4. Interactive Loop (Prevents script from exiting)
    print("\n--- Local Infrastructure Agent Active ---")
    print("Type 'exit' to quit.")
    
    while True:
        user_input = input("\nQuery: ")
        if user_input.lower() in ["exit", "quit"]:
            break

        async for event in app.astream(
            {"messages": [HumanMessage(content=user_input)]}
        ):
            for node, value in event.items():
                if "messages" in value:
                    msg = value["messages"][-1]
                    
                    # 1. Extract the text content safely
                    if hasattr(msg, "content") and msg.content:
                        # If content is a list (multimodal), join it; otherwise just print
                        content = msg.content
                        if isinstance(content, list):
                            content = " ".join([c.get("text", "") for c in content if isinstance(c, dict)])
                        
                        # 2. Print only the clean text
                        print(f"\n[{node}]: {content}")

if __name__ == "__main__":
    asyncio.run(main())