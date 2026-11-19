from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

from test1 import api_key

load_dotenv()

def day_test():

    llm = init_chat_model(
        model="MiniMax-M3.1-Flash",
        model_provider="openai",
        base_url="https://api.minimax.cn/v1",
        temperature="0",
        api_key="sk-cp-fyd-8xZZTYZgmpv6s71zVL-nGnzWNfi4tUkHx_Z7ZtUhAEaHyojhvCbD0wTA5psj_-IqrwhpVKYRj9dnCojBpOf2bcXoxFJacAQb7MtgaxYvjCGGMDwhjJs"
    )

    system_message = """
        你是Test2Sql引擎，
        数据库表结构：
        - order_info(order_id, user_id, pay_amount, pay_status, pay_time)
        - pay_status: 1=待支付 2=已支付 3=退款中
        只输出 SQL，不加解释。
    """
    message = [("system",system_message),("user","{questions}")]
    chain =  ChatPromptTemplate.from_messages(message) | llm | StrOutputParser()

    questions = [
        "查询昨天已支付的订单数量",
        "查询上月销售额最高的 5 个用户",
        "查询今天退款中的订单金额总和"
    ]

    for q in questions:
        print(f"问：{q}")
        ans =  chain.invoke({'questions': q})
        print(f"SQL：{ans}")
    
    
if __name__ == '__main__':
    day_test()