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
# 这里我们抓取第 9 到 16 条，避免与 deep 版内容重复
url_rss = "https://news.google.com/rss?hl=zh-CN&gl=CN&ceid=CN:zh-Hans"
feed = feedparser.parse(url_rss)
news_text = "\n".join([f"- {e.title}" for e in feed.entries[2:4]])

# 3. 准备提示词 (针对奇闻异见风格)
prompt = f"""
你现在是“猫笔刀”，一位观察力极强且文风辛辣的评论员。
任务：从以下新闻素材中，挑选一件最荒诞、最反直觉或最有趣的事件，写一篇轻松幽默的短评。
写作原则：
1. [叙事风格]：辛辣讽刺，语调轻松，多用反讽，拒绝说教。
2. [深度挖掘]：用极短的篇幅揭露表象之下的荒谬逻辑。
3. [排版]：精炼简短，段落分明，结尾要有让人会心一笑的“梗”。

素材：
{news_text}
"""

# 4. 执行生成与保存
text = generate_with_retry(prompt)

if text:
    filename = f"article_odd_{datetime.now().strftime('%Y-%m-%d')}.md"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(f"# 猫笔刀·奇闻异见\n\n{text}")
    print(f"成功生成文件: {filename}")
else:
    print("生成失败，已达到最大重试次数。")
    exit(1)


