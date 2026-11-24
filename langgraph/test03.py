from typing import TypedDict, List, NotRequired


#1.定义结构
class AdvancedState(TypedDict):
    user_query:str
    conversation_history: List[str]

    #可选字段 - 使用NotRequired表示该字段可以缺失
    rag_documents: NotRequired[List[dict]]
    search_results: NotRequired[List[dict]]

simple_state:AdvancedState = {
    "user_query": "请解释LangGraph的状态管理",
    "conversation_history": ["你好，我是AI助手，","我能帮你了解LangGraph"]
}

# 2.1 创建完整的状态
full_state: AdvancedState = {
    "user_query": "请解释LangGraph的状态管理",
    "conversation_history": ["你好，我是AI助手", "我能帮您了解LangGraph"],
    "rag_documents": [
        {"title": "LangGraph文档", "content": "状态管理章节..."},
        {"title": "最佳实践", "content": "TypedDict是推荐方式..."}
    ]
}
