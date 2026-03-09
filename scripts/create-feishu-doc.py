#!/usr/bin/env python3
"""
飞书文档创建和写入脚本
"""
import os
import sys
import json

# 内容文件路径
CONTENT_FILE = "/root/.openclaw/workspace/docs/feishu-wiki-sync.md"

def read_content():
    """读取要写入的内容"""
    if not os.path.exists(CONTENT_FILE):
        print(f"❌ 内容文件不存在: {CONTENT_FILE}")
        return None

    with open(CONTENT_FILE, 'r', encoding='utf-8') as f:
        return f.read()

def main():
    content = read_content()
    if content is None:
        return

    print(f"📋 飞书文档创建和写入")
    print(f"内容文件: {CONTENT_FILE}")
    print(f"内容长度: {len(content)} 字符，{content.count(chr(10))} 行")

    print("\n⚠️ 需要通过OpenClau的插件系统写入")
    print("\n📝 飞书API需要的信息：")
    print("1. app_id: 飞书应用的App ID")
    print("2. app_secret: 飞书应用的App Secret")
    print("3. wiki_token: 知识库页面token")
    print("4. user_open_id: 你的飞书用户Open ID")

    print("\n💡 或者，你可以：")
    print("1. 手动创建一个空Wiki页面")
    print("2. 把下面的内容复制粘贴进去")

    print("\n" + "="*60)
    print(content)
    print("="*60)

if __name__ == "__main__":
    main()
