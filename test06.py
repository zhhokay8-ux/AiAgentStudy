import os
from langchain.chat_models import init_chat_model
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableParallel
from langchain_core.output_parsers import StrOutputParser

def runnable_parallel_demo():
    llm = init_chat_model(
        model="MiniMax-M3.1-Flash",
        model_provider="openai",  # 提供者
        base_url="https://api.minimax.cn/v1",
        api_key="sk-cp-fyd-8xZZTYZgmpv6s71zVL-nGnzWNfi4tUkHx_Z7ZtUhAEaHyojhvCbD0wTA5psj_-IqrwhpVKYRj9dnCojBpOf2bcXoxFJacAQb7MtgaxYvjCGGMDwhjJs"
    )

    # english_chain = PromptTemplate.from_template("把这个句子{topic}翻译成英文") | llm | StrOutputParser()
    # korean_chain = PromptTemplate.from_template("把这个句子{topic}翻译成韩文") | llm | StrOutputParser()
    #
    english_chain = (PromptTemplate.from_template("把这个句子{topic}翻译成英文") | llm | StrOutputParser())

    korean_chain = (PromptTemplate.from_template("把这个句子{topic}翻译成韩文") | llm | StrOutputParser())

    # 参数名称任意,用于输出结果json的key
    map_chain = RunnableParallel(english=english_chain, korean=korean_chain)

    resp = map_chain.invoke({"topic": "人工智能是一种智能技术"})

    print(resp)

if __name__ == '__main__':
    runnable_parallel_demo()


