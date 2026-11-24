from mcp.server import FastMCP

mcp = FastMCP("Demo")

@mcp.tool()
def add(a:int,b:int) -> int:
    return a+b


# 为 MCP 实例添加资源
@mcp.resource("greeting://default")
def get_greeting() -> str:
    return "Hello from static resource!"


# 为 MCP 实例添加提示词
@mcp.prompt()
def greet_user(name: str, style: str = "friendly") -> str:
    styles = {
        "friendly": "写一句友善的问候",
        "formal": "写一句正式的问候",
        "casual": "写一句轻松的问候",
    }
    return f"为{name}{styles.get(style, styles['friendly'])}"
"""
stdio客户端使用 MCP的流程为：
通过 stdio_client 启动进程：构建 stdio 启动参数
建立会话：通过 ClientSession 构建会话 session
握手初始化：调用 session.initialize()
获取能力: 通过 session.list_tools() / session.call_tools() 等获取或者使用 MCP 能力
"""
if __name__ == '__main__':
    # mcp.run(transport="stdio")
    mcp.run(transport="streamable-http")