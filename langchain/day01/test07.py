import os
from langchain.chat_models import init_chat_model
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

def runnable_parallel_use_lcel_demo():
    llm1 = init_chat_model(
        model="MiniMax-M3.1-Flash",
        model_provider="openai",  # 提供者
        base_url="https://api.minimax.cn/v1",
        api_key="sk-cp-fyd-8xZZTYZgmpv6s71zVL-nGnzWNfi4tUkHx_Z7ZtUhAEaHyojhvCbD0wTA5psj_-IqrwhpVKYRj9dnCojBpOf2bcXoxFJacAQb7MtgaxYvjCGGMDwhjJs"
    )

    llm2 = init_chat_model(
        model="MiniMax-M3.1-Flash",
        model_provider="openai",  # 提供者
        base_url="https://api.minimax.cn/v1",
        api_key="sk-cp-fyd-8xZZTYZgmpv6s71zVL-nGnzWNfi4tUkHx_Z7ZtUhAEaHyojhvCbD0wTA5psj_-IqrwhpVKYRj9dnCojBpOf2bcXoxFJacAQb7MtgaxYvjCGGMDwhjJs"
    )

    pargh_01 = PromptTemplate.from_template("对这首诗{poem}做一下赏析，分析他蕴含的意义") | llm1 | StrOutputParser()

    pargh_02 = PromptTemplate.from_template("对这首诗{poem}做一下赏析，分析他蕴含的意义") | llm2 | StrOutputParser()

    summary_chain = PromptTemplate.from_template(
        "这两种赏析，第一种：{paragraph_1}，第二种：{paragraph_2}，哪个更好，为什么") | llm2 | StrOutputParser()

    # 4、构造 LCEL：将前面的两个 chain并行运行，然后将结果传递给summary_chain
    map_chain = {
                    "paragraph_1": pargh_01,
                    "paragraph_2": pargh_02,
                } | summary_chain

    poem = """
        菩提本无树，
        明镜亦非台，
        本来无一物，
        何处惹尘埃。
        """
    resp = map_chain.invoke({"poem": poem})
    print(resp)

if __name__ == '__main__':
    runnable_parallel_use_lcel_demo()