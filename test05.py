from langchain.chat_models import init_chat_model
from langchain_core.output_parsers import JsonOutputParser, PydanticOutputParser
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel
from typing import List

class CalendarEvent(BaseModel):
    name: str
    date: str
    participants: List[str]

def call_chain():
    llm = init_chat_model(
        model="MiniMax-M3.1-Flash",
        model_provider="openai",  # 提供者
        base_url="https://api.minimax.cn/v1",
        api_key="sk-cp-fyd-8xZZTYZgmpv6s71zVL-nGnzWNfi4tUkHx_Z7ZtUhAEaHyojhvCbD0wTA5psj_-IqrwhpVKYRj9dnCojBpOf2bcXoxFJacAQb7MtgaxYvjCGGMDwhjJs"
    )

    parser = PydanticOutputParser(pydantic_object=CalendarEvent)


    template = ChatPromptTemplate.from_messages([
        ("system", "你是信息抽取助手。只输出 JSON，不要输出 Markdown 或解释。{format_instructions}"),
        ("user", "{input_question}"),
    ]).partial(format_instructions=parser.get_format_instructions())

    # python 提供了魔法方法， __or__ 实现了 | 的操作
    chain = template | llm | parser

    resp = chain.invoke({
        "input_question": "2026 年 5 月 13 日,张三和李四要参与一场会议，会议名称为'和平之旅'"
    })
    print(resp)

if __name__ == '__main__':
    call_chain()