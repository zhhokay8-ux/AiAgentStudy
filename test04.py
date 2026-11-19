from langchain_core.messages import HumanMessage,SystemMessage,AIMessage
from langchain_core.output_parsers import JsonOutputParser
from langchain.chat_models import init_chat_model
from langchain_core.prompts import ChatPromptTemplate


def prompt_template():

    llm = init_chat_model(
        model="MiniMax-M3.1-Flash",
        model_provider="openai",  # 提供者
        base_url="https://api.minimax.cn/v1",
        api_key="sk-cp-fyd-8xZZTYZgmpv6s71zVL-nGnzWNfi4tUkHx_Z7ZtUhAEaHyojhvCbD0wTA5psj_-IqrwhpVKYRj9dnCojBpOf2bcXoxFJacAQb7MtgaxYvjCGGMDwhjJs"
    )

    prompt_template_message = [("system","你是一个专业的评论员"),("user","请评价{product}的优缺点，包括{aspect1}和{aspect2}。")]
    # prompt_template_message = [SystemMessage("你是一个专业的评论员"),HumanMessage("请评价{product}的优缺点，包括{aspect1}和{aspect2}。")]
    #`SystemMessage` 和 `HumanMessage` 只是普通消息对象，里面的 `{product}` 会被当成普通文字，不会自动替换。

    #提示词模版
    template = ChatPromptTemplate.from_messages(prompt_template_message)

    chat_list = template.invoke({"product":"Iphone 15","aspect1":"优点","aspect2":"外观"})


    resp = llm.invoke(chat_list)

    print(resp.content,end="")

if __name__ == '__main__':
    prompt_template()

