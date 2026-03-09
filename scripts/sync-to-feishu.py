#!/usr/bin/env python3
"""
飞书文档内容同步脚本
将内容写入指定的飞书文档
"""

import os
import json
from pathlib import Path

# 飞书文档token
DOC_TOKEN = "GEUrddWeQo0CnMxVpC0cVkROnbf"

# 内容文件路径
CONTENT_FILE = "/root/.openclaw/workspace/docs/feishu-sync.md"

def read_content():
    """读取要同步的内容"""
    if not os.path.exists(CONTENT_FILE):
        print(f"❌ 内容文件不存在: {CONTENT_FILE}")
        return None

    with open(CONTENT_FILE, 'r', encoding='utf-8') as f:
        return f.read()

def main():
    print("📋 飞书文档内容同步")
    print(f"文档Token: {DOC_TOKEN}")
    print(f"内容文件: {CONTENT_FILE}")

    content = read_content()
    if content is None:
        return

    print(f"\n✅ 读取到内容（{len(content)} 字符）")
    print("\n📝 内容预览（前500字符）：")
    print(content[:500])
    print("...")

    print("\n⚠️ 需要通过OpenClaw的插件系统写入")
    print("请使用以下内容手动粘贴到飞书文档：")
    print("\n" + "="*60)
    print(content)
    print("="*60)

if __name__ == "__main__":
    main()
