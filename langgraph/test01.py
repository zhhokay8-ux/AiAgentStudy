from typing import TypedDict
import time

from langgraph.constants import START, END
from langgraph.graph import StateGraph

"""

目标：通过问题搜索答案
1.定义图状态
2.定义节点函数
3.通过状态创建图实例
4.添加节点
5.添加边
6.编译图
7.启动工作流
8.输出结果
"""

# 1.定义图状态
class MyState(TypedDict):
    query: str #用户输入
    rag_result:str #rag向量查询结果
    web_result:str #web查询结果
    final_result:str #最终回复


def rag_search_node(state:MyState):
    query = state.get("query");
    print("📚【技术知识库】开始检索学术定义...")
    # 2 模拟调用RAG搜索
    time.sleep(2)
    rag_result = f"📚【学术定义】{query}：指大语言模型（LLM）生成的内容虽然看似合理且流畅，但实际上与源上下文或现实世界事实不符，甚至完全虚构的现象。"
    # 3 将搜索结果写入到图状态中
    print("📚【技术知识库】检索完成！")
    return {"rag_result":rag_result};


def web_search_node(state:MyState):
    # 1 获取用户输入
    print("🌏【实时网络搜索】全网查询最新案例...")
    query = state["query"]

    # 2 模拟调用网络搜索
    time.sleep(2)
    web_search_result = f"🌏【通俗解释】{query}：常被戏称为AI在“一本正经地胡说八道”。比如AI可能会捏造不存在的历史事件、错误的代码库引用或虚假的论文出处。"

    # 3 将搜索结果写入到图状态中
    print("🌏【实时网络搜索】搜索完毕！")
    return {"web_result": web_search_result}

def final_answer_node(state:MyState):
    # 1 从图状态中获取多路搜索结果
    print("🤖【AI助手】正在综合多方信息生成回答...")
    rag_result = state["rag_result"]
    web_search_result = state["web_result"]

    # 2 模拟调用大模型
    final_answer = f"""
                   🤖【AI助手总结】：
                   {rag_result}
                   {web_search_result}
                   需要我教你如何降低模型的幻觉率吗❓
                   """
    time.sleep(2)

    # 3 将最终回复写入到图状态中
    print("🤖【AI助手】回答生成结束！")
    return {"final_result": final_answer}

#3.通过状态创建图实例
graph = StateGraph(MyState)

#4.添加节点
graph.add_node(rag_search_node)
graph.add_node(web_search_node)
graph.add_node(final_answer_node)

#5.添加边
graph.add_edge(START,"rag_search_node")
graph.add_edge(START,"web_search_node")

graph.add_edge("rag_search_node","final_answer_node")
graph.add_edge("web_search_node","final_answer_node")
graph.add_edge("final_answer_node",END)

#6.编译图
compile_graph = graph.compile()

#7.启动图
state = compile_graph.invoke({"query":"大模型中的幻觉是什么意思?"})

print(state["final_result"])

compile_graph.get_graph().print_ascii()


