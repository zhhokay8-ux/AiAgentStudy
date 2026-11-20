from langchain_core.messages import HumanMessage,SystemMessage,AIMessage
from langchain_core.output_parsers import JsonOutputParser
from pydantic import BaseModel, Field
from langchain.chat_models import init_chat_model


class Prime(BaseModel):
    prime: list[int] = Field(description="素数")
    count: list[int] = Field(description="小于该素数的素数个数")


def json_out_parse():

    llm = init_chat_model(
        model="MiniMax-M3.1-Flash",
        model_provider="openai",  # 提供者
        base_url="https://api.minimax.cn/v1",
        api_key="sk-cp-fyd-8xZZTYZgmpv6s71zVL-nGnzWNfi4tUkHx_Z7ZtUhAEaHyojhvCbD0wTA5psj_-IqrwhpVKYRj9dnCojBpOf2bcXoxFJacAQb7MtgaxYvjCGGMDwhjJs"
    )

    json_parser = JsonOutputParser(pydantic_object=Prime)
    print(json_parser.get_format_instructions())
    res = llm.invoke([("system", json_parser.get_format_instructions()), #将解析器给系统的提示词给大模型
                      ("user", "任意生成5个1000-100000之间素数，并标出小于该素数的素数个数")])

    print(res.content)
    parsed_res = json_parser.invoke(res)
    print(type(parsed_res))


if __name__ == '__main__':
    json_out_parse()