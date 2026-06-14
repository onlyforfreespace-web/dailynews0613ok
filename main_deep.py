import os
import time
import random
from google import genai
from datetime import datetime
import feedparser

# 1. 初始化客户端
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def generate_with_retry(prompt, max_retries=3):
    """带重试功能的生成函数"""
    for attempt in range(max_retries):
        try:
            # 切换到 2.0 模型以确保兼容性
            response = client.models.generate_content(
                model='models/gemini-3.5-flash',
                contents=prompt
            )
            return response.text
        except Exception as e:
            print(f"尝试第 {attempt+1} 次重试，错误信息: {e}")
            time.sleep(15 + random.randint(0, 10))
    return None

# 2. 获取资讯
url_rss = "https://news.google.com/rss?hl=zh-CN&gl=CN&ceid=CN:zh-Hans"
feed = feedparser.parse(url_rss)
news_text = "\n".join([f"- {e.title}" for e in feed.entries[:2]])

# 3. 准备提示词
prompt = f"""
你现在是“猫笔刀”，一位在金融圈摸爬滚打 20 年的资深观察者。
任务：针对以下新闻素材，撰写一篇犀利的财经深度时评。
写作原则：
1. [极致洞察]：不要重复新闻事实，直接剖析背后的资本博弈与趋势。
2. [快节奏感]：使用短句，多用反问，拒绝公文式铺垫。
3. [Markdown排版]：强制使用 ## 标题，核心观点【加粗】。
4. [金句结尾]：末尾留下一句引发共鸣的金句。

素材：
{news_text}
"""

# 4. 执行生成与保存
text = generate_with_retry(prompt)

if text:
    filename = f"article_deep_{datetime.now().strftime('%Y-%m-%d')}.md"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(f"# 猫笔刀·财经深读\n\n{text}")
    print(f"成功生成文件: {filename}")
else:
    print("生成失败，已达到最大重试次数。")
    exit(1) # 触发错误码，让 GitHub Action 报错


