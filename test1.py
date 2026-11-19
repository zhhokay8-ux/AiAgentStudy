from dotenv import load_dotenv
# 2、调用 load_dotenv 方法加载.env 文件
load_dotenv()
# 3、通过os模块读取环境变量
import os
api_key = os.getenv("OPENAI_API_KEY")
print(api_key)