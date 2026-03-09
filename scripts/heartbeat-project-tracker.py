#!/usr/bin/env python3
"""
心跳任务：项目进度跟踪
每30分钟检查一次项目状态并更新记忆
"""
import os
import subprocess
import json
from datetime import datetime

# 配置
WORKSPACE = "/root/.openclaw/workspace"
CONTENT_DIR = f"{WORKSPACE}/content"
MEMORY_DIR = f"{WORKSPACE}/memory"
TODAY = datetime.now().strftime("%Y-%m-%d")
LOG_FILE = f"{MEMORY_DIR}/{TODAY}.md"

def check_git_status():
    """检查 Git 仓库状态"""
    os.chdir(CONTENT_DIR)
    result = subprocess.run(
        ["git", "status", "--short"],
        capture_output=True,
        text=True
    )
    return result.stdout.strip()

def count_content_files():
    """统计内容文件内容"""
    counts = {
        "scripts": 0,
        "posts_douyin": 0,
        "posts_xiaohongshu": 0,
        "posts_bilibili": 0
    }

    # 统计脚本
    if os.path.exists(f"{CONTENT_DIR}/scripts"):
        counts["scripts"] = len(os.listdir(f"{CONTENT_DIR}/scripts"))

    # 统计文案
    for platform in ["douyin", "xiaohongshu", "bilibili"]:
        path = f"{CONTENT_DIR}/posts/{platform}"
        if os.path.exists(path):
            counts[f"posts_{platform}"] = len(os.listdir(path))

    return counts

def get_latest_commit():
    """获取最新提交"""
    os.chdir(CONTENT_DIR)
    result = subprocess.run(
        ["git", "log", "-1", "--format=%h - %s (%ar)"],
        capture_output=True,
        text=True
    )
    return result.stdout.strip()

def update_log():
    """更新今日日志"""
    now = datetime.now().strftime("%H:%M:%S")
    log_entry = f"""
## {now} 心跳检查

### 项目状态
- 最新提交：{get_latest_commit()}
- Git 状态：{check_git_status() or "无未提交更改"}

### 内容统计
"""

    counts = count_content_files()
    for key, value in counts.items():
        log_entry += f"- {key}: {value}\n"

    # 追加到日志文件
    if not os.path.exists(MEMORY_DIR):
        os.makedirs(MEMORY_DIR)

    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(log_entry)

    print(f"✅ 心跳日志已更新: {LOG_FILE}")

def main():
    print(f"📊 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - 项目进度跟踪")
    update_log()

if __name__ == "__main__":
    main()
