import asyncio

from mcp import ClientSession
from mcp.client.streamable_http import streamable_http_client


async def streamablehttp_run():
    url ="http://127.0.0.1:8000/mcp"
    async with streamable_http_client(url=url) as(read,write):
        async with ClientSession(read,write) as session:

            #初始化链接
            await session.initialize()

            #获取链接工具
            tools = await session.list_tools()
            print(tools)
            print()

            call_res = await session.call_tool("add",{"a":"1","b":"2"})
            print(call_res)
            print()

            # 获取可用资源
            resources = await session.list_resources()
            print(resources)
            print()

            # 调用资源
            read_res = await session.read_resource("greeting://default")
            print(read_res)
            print()

            # 获取可用提示
            prompts = await session.list_prompts()
            print(prompts)
            print()

            # 调用提示
            get_res = await session.get_prompt("greet_user", {"name": "Jack"})
            print(get_res)
            print()

asyncio.run(streamablehttp_run())


