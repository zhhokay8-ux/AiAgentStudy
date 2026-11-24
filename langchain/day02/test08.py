from langchain.chat_models import init_chat_model
from langchain_core.messages import HumanMessage, ToolMessage
from langchain_core.tools import tool


@tool
def get_weather(city,date) ->str:
    """
    获取指定城市在指定日期的天气
    """
    return f"{city}在{date}天气多云,又下雨的可能"




llm = init_chat_model(
    model="MiniMax-M3.1-Flash",
    model_provider="openai",  # 提供者
    base_url="https://api.minimax.cn/v1",
    api_key="sk-cp-fyd-8xZZTYZgmpv6s71zVL-nGnzWNfi4tUkHx_Z7ZtUhAEaHyojhvCbD0wTA5psj_-IqrwhpVKYRj9dnCojBpOf2bcXoxFJacAQb7MtgaxYvjCGGMDwhjJs"
)
# HumanMessage
message_list = [HumanMessage(content="北京2026-11-24的天气")]

llm = llm.bind_tools([get_weather])  #注意，必须重新赋值
res = llm.invoke(message_list)

#AIMessage
message_list.append(res)
#当前结果当中包含调用工具的出参
print('LLM的首次回复：',res)

#解析调用工具的出参,手动调用工具
tool_call = res.tool_calls[0]
args = tool_call['args']
id = tool_call["id"]
#
#       @tool 装饰器的作用
# 		将普通 Python 函数包装成 StructuredTool 对象
# 		StructuredTool 继承自 LangChain 的 Runnable 基类
# 		因此具备了 .invoke()、.ainvoke() 等标准调用方法。不能再按照普通函数正常调用。但可以绕过封装，直接调用底层函数：
# 		get_weather.func(args['city'],args['date'])

tool_call_res = get_weather.invoke(args)

#构造ToolMessage对象
toolMessage = ToolMessage(tool_call_id=id,content=tool_call_res)
message_list.append(toolMessage)

print("message_list",message_list)
res = llm.invoke(message_list)
print("基于调用工具返回信息后,LLM的回复",res)

