#!/usr/bin/env python3
"""
心跳任务：记忆维护
每天检查一次，更新长期记忆
"""
import os
import re
from datetime import datetime, timedelta

# 配置
WORKSPACE = "/root/.openclaw/workspace"
MEMORY_DIR = f"{WORKSPACE}/memory"
MEMORY_FILE = f"{WORKSPACE}/MEMORY.md"

def get_recent_days(days=3):
    """获取最近几天的日期"""
    dates = []
    for i in range(days):
        date = (datetime.now() - timedelta(days=i)).strftime("%Y-%m-%d")
        dates.append(date)
    return dates

def read_memory_file(date):
    """读取某天的记忆文件"""
    path = f"{MEMORY_DIR}/{date}.md"
    if not os.path.exists(path):
        return ""

    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def extract_important_events(content):
    """提取重要事件"""
    events = []

    # 提取完成的事项
    for match in re.finditer(r'- ✅\s*(.+)', content):
        events.append(f"✅ {match.group(1).strip()}")

    # 提取待办事项
    for match in re.finditer(r'- 🚧\s*(.+)', content):
        events.append(f"🚧 {match.group(1).strip()}")

    return events

def update_long_term_memory():
    """更新长期记忆"""
    recent_dates = get_recent_days(3)

    # 收集最近几天的重要事件
    all_events = []
    for date in recent_dates:
        content = read_memory_file(date)
        if content:
            events = extract_important_events(content)
            if events:
                all_events.append(f"\n### {date}")
                all_events.extend(events)

    if not all_events:
        print("没有新事件需要记录")
        return

    # 读取现有长期记忆
    existing_memory = ""
    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, "r", encoding="utf-8") as f:
            existing_memory = f.read()

    # 检查是否需要更新
    update_marker = "\n## 最近动态\n"
    if update_marker in existing_memory:
        # 更新最近动态部分
        parts = existing_memory.split(update_marker)
        updated_memory = parts[0] + update_marker + "\n".join(all_events) + "\n\n" + "\n\n".join(parts[1].split("\n\n")[1:])
    else:
        # 添加最近动态部分
        updated_memory = existing_memory.rstrip() + "\n" + update_marker + "\n".join(all_events) + "\n"

    # 写回长期记忆
    with open(MEMORY_FILE, "w", encoding="utf-8") as f:
        f.write(updated_memory)

    print(f"✅ 长期记忆已更新: {MEMORY_FILE}")

def main():
    print(f"🧠 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - 记忆维护")
    update_long_term_memory()

if __name__ == "__main__":
    main()
