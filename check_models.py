import os
from google import genai

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# 列出当前所有可用的模型
print("--- 可用模型列表 ---")
for m in client.models.list():
    print(f"模型名称: {m.name}, 支持的方法: {m.supported_actions}")

