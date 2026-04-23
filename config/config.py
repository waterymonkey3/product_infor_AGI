import os
import dotenv
from langchain_openai import ChatOpenAI


dotenv.load_dotenv()

chat_model = ChatOpenAI(
    model="gpt-5.1-fast",
    base_url=os.getenv("OPENAI_API_BASE"),
    api_key=os.getenv("OPENAI_API_KEY"),
    max_tokens=100,
)




'''
# 测试代码
message = "who are you?"

print("message: ", message)

response = chat_model.invoke(message)


print("response: ", response)
'''