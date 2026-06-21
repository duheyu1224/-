import os
import subprocess
from datetime import datetime
from openai import OpenAI

# 初始化 OpenAI (确保在 GitHub Secrets 中设置了 OPENAI_API_KEY)
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

def get_git_logs():
    # 获取最近7天的提交记录
    result = subprocess.run(['git', 'log', '--since="7 days ago"', '--oneline'], 
                            capture_output=True, text=True)
    return result.stdout

def generate_report(logs):
    prompt = f"""
    你是一个资深的研发工程师助理。请根据以下 Git 提交记录，整理一份周报。
    
    格式要求：
    1. 【本周工作概览】：用简练的语言总结本周研发核心。
    2. 【代码提交记录】：基于下方提供的 logs 整理分类，分为“开发/重构”、“修复”、“文档/其他”。
    3. 【技术与研究总结】：（此处留白，我后续会手动补充研究进展）。
    4. 【下周规划】：基于本周工作自动推断。

    Git 记录：
    {logs}
    """
    
    response = client.chat.completions.create(
        model="gpt-4o", # 或者 gpt-3.5-turbo
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

if __name__ == "__main__":
    logs = get_git_logs()
    report = generate_report(logs)
    
    # 保存周报
    date_str = datetime.now().strftime("%Y-%m-%d")
    os.makedirs("reports", exist_ok=True)
    with open(f"reports/weekly-{date_str}.md", "w", encoding="utf-8") as f:
        f.write(f"# 周报 {date_str}\n\n{report}")
