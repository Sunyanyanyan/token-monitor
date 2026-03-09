#!/usr/bin/env python3
"""
飞书Wiki内容同步脚本
将内容写入指定的飞书知识库页面
"""

import os
from pathlib import Path

# 飞书Wiki token
WIKI_TOKEN = "I3U2wdQmXiOJLFkd9X4cbUtYngg"

# 内容文件路径
CONTENT_FILE = "/root/.openclaw/workspace/docs/feishu-wiki-sync.md"

def read_content():
    """读取要同步的内容"""
    if not os.path.exists(CONTENT_FILE):
        print(f"❌ 内容文件不存在: {CONTENT_FILE}")
        return None

    with open(CONTENT_FILE, 'r', encoding='utf-8') as f:
        return f.read()

def main():
    print("📋 飞书Wiki内容同步")
    print(f"Wiki Token: {WIKI_TOKEN}")
    print(f"内容文件: {CONTENT_FILE}")

    content = read_content()
    if content is None:
        return

    print(f"\n✅ 读取到内容（{len(content)} 字符，{content.count(chr(10))} 行）")
    print("\n📝 内容预览（前800字符）：")
    print(content[:800])
    print("...")

    print("\n⚠️ 需要通过OpenClau的插件系统写入")
    print("请使用以下内容手动粘贴到飞书Wiki：")
    print("\n" + "="*60)
    print(content)
    print("="*60)

if __name__ == "__main__":
    main()
