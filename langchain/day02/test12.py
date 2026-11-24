import asyncio

from langchain.agents import create_agent
from langchain.chat_models import init_chat_model
from langchain_core.messages import AIMessage, HumanMessage, ToolMessage
from langchain_mcp_adapters.client import MultiServerMCPClient

client = MultiServerMCPClient(
    {
        "12306": {
          "transport": "streamable_http",
          "url": "https://mcp.api-inference.modelscope.net/2b09a4b129514b/mcp"
        }
    }

)

def print_message(message):
    if isinstance(message,AIMessage):
        print("AI回复：",message.content)
        print("AI决定调用工具",message.tool_calls)
    elif isinstance(message,HumanMessage):
        print("用户输入:",message.content)
    elif isinstance(message,ToolMessage):
        print("工具调用:", message.content)
    else:
        print("位置的消息类型")

async def main():
    tools = await client.get_tools()
    print(tools)

    def handle_tool_error(error) -> str:
        return f"Tool execution failed: {str(error)}"

    # 配置工具错误所对应的处理方式，避免工具调用错误导致整个 agent执行过程退出
    for tool in tools:
        tool.handle_tool_error = handle_tool_error

    llm = init_chat_model(
        model="MiniMax-M3.1-Flash",
        model_provider="openai",  # 提供者
        base_url="https://api.minimax.cn/v1",
        api_key="sk-cp-fyd-8xZZTYZgmpv6s71zVL-nGnzWNfi4tUkHx_Z7ZtUhAEaHyojhvCbD0wTA5psj_-IqrwhpVKYRj9dnCojBpOf2bcXoxFJacAQb7MtgaxYvjCGGMDwhjJs"
    )

    agent = create_agent(llm,
                 tools)

    while True:
        user_input = input(">")
        if user_input == "exit":
            break
        res = await agent.ainvoke({"messages": [{"role": "user", "content": user_input}]},
                                  config={"configurable": {"thread_id": "1"}})
        print(res)
        print(res['messages'][-1].content,end='\n\n')
        for message in res['messages']:
            print_message(message)
            print("\n")
        print("\n")


asyncio.run(main())