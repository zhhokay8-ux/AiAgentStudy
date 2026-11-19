from langchain_core.messages import HumanMessage,SystemMessage,AIMessage
import asyncio

def get_model_from_init():
    import os
    import dotenv
    dotenv.load_dotenv()
    from langchain.chat_models import init_chat_model
    llm = init_chat_model(
        model="MiniMax-M3.1-Flash",
        model_provider="openai", #提供者
        base_url="https://api.minimax.cn/v1",
        api_key="sk-cp-fyd-8xZZTYZgmpv6s71zVL-nGnzWNfi4tUkHx_Z7ZtUhAEaHyojhvCbD0wTA5psj_-IqrwhpVKYRj9dnCojBpOf2bcXoxFJacAQb7MtgaxYvjCGGMDwhjJs"
    )


    # resp = llm.invoke([SystemMessage(content="你是一个聊天助手"),HumanMessage(content="今天天气如何")])

    messages_list = [("system", "你是一个专业的数学助手"), ("user", "你好，你是谁")]  #列表加元组的方式。
    # message_list = [{"role": "system", "content": "你是一个专业的数学助手"}, {"role": "user", "content": "你好，你是谁"}] #列表加字符串的方式。
    resp = llm.invoke(messages_list)



    # resp = llm.invoke("你是谁")
    print(type(resp))  # <class 'langchain_core.messages.ai.AIMessage'>
    print(resp.content)  # 获取结果

async def get_model_from_init2():
    import os
    import dotenv
    dotenv.load_dotenv()
    from langchain.chat_models import init_chat_model
    llm = init_chat_model(
        model="MiniMax-M3.1-Flash",
        model_provider="openai", #提供者
        base_url="https://api.minimax.cn/v1",
        api_key="sk-cp-fyd-8xZZTYZgmpv6s71zVL-nGnzWNfi4tUkHx_Z7ZtUhAEaHyojhvCbD0wTA5psj_-IqrwhpVKYRj9dnCojBpOf2bcXoxFJacAQb7MtgaxYvjCGGMDwhjJs"
    )

    messages_list = [("system", "你是一个专业的数学助手"), ("user", "你好，你是谁")]  #列表加元组的方式。
    resp = await llm.ainvoke(messages_list)

    print(resp.content)  # 获取结果

def get_model_from_init3():
    import os
    import dotenv
    dotenv.load_dotenv()
    from langchain.chat_models import init_chat_model
    llm = init_chat_model(
        model="MiniMax-M3.1-Flash",
        model_provider="openai", #提供者
        base_url="https://api.minimax.cn/v1",
        api_key="sk-cp-fyd-8xZZTYZgmpv6s71zVL-nGnzWNfi4tUkHx_Z7ZtUhAEaHyojhvCbD0wTA5psj_-IqrwhpVKYRj9dnCojBpOf2bcXoxFJacAQb7MtgaxYvjCGGMDwhjJs"
    )

    messages_list = [("user", "什么是 LangChain")]  #列表加元组的方式。
    resp = llm.stream(messages_list)

    for message in resp:
        print(message.content, end="")

def get_model_from_init4():
    import os
    import dotenv
    dotenv.load_dotenv()
    from langchain.chat_models import init_chat_model
    llm = init_chat_model(
        model="MiniMax-M3.1-Flash",
        model_provider="openai", #提供者
        base_url="https://api.minimax.cn/v1",
        api_key="sk-cp-fyd-8xZZTYZgmpv6s71zVL-nGnzWNfi4tUkHx_Z7ZtUhAEaHyojhvCbD0wTA5psj_-IqrwhpVKYRj9dnCojBpOf2bcXoxFJacAQb7MtgaxYvjCGGMDwhjJs"
    )

    # llm.batch(HumanMessage=)
    messages_list = [("user", "什么是 LangChain"),("user","LangChain的核心模块")]  #列表加元组的方式。
    resp = llm.batch(messages_list)

    for response in resp:
        print(response.content, end="")


if __name__ == '__main__':
    get_model_from_init()
    # asyncio.run(get_model_from_init2());
    # get_model_from_init3()
    # get_model_from_init4()