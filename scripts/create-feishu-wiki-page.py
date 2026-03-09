#!/usr/bin/env python3
"""
飞书Wiki页面创建和写入脚本
"""
import requests
import json

# 飞书API配置
APP_ID = "cli_a911a8ea06b89bc6"
APP_SECRET = "pP6jilcISsVXaL5DJD8VPfRUHK5AIUFM"
WIKI_TOKEN = "I3U2wdQmXiOJLFkd9X4cbUtYngg"
USER_OPEN_ID = "ou_94bdf408e50126a28437a49e5e0342bd"  # 从metadata获取

# 飞书API基础URL
BASE_URL = "https://open.feishu.cn/open-apis"

# 内容文件路径
CONTENT_FILE = "/root/.openclaw/workspace/docs/feishu-wiki-sync.md"

def get_tenant_access_token():
    """获取tenant_access_token"""
    url = f"{BASE_URL}/auth/v3/tenant_access_token/internal"
    headers = {
        "Content-Type": "application/json; charset=utf-8"
    }
    data = {
        "app_id": APP_ID,
        "app_secret": APP_SECRET
    }
    
    response = requests.post(url, headers=headers, json=data)
    if response.status_code != 200:
        print(f"❌ 获取tenant_access_token失败: {response.text}")
        return None
    
    result = response.json()
    if result.get("code") != 0:
        print(f"❌ 获取tenant_access_token失败: {result.get('msg')}")
        return None
    
    return result.get("tenant_access_token")

def get_user_access_token(tenant_token):
    """获取user_access_token"""
    url = f"{BASE_URL}/auth/v3/user_access_token/internal"
    headers = {
        "Content-Type": "application/json; charset=utf-8"
    }
    data = {
        "app_id": APP_ID,
        "app_secret": APP_SECRET,
        "grant_type": "authorization_code"
    }
    
    response = requests.post(url, headers=headers, json=data)
    if response.status_code != 200:
        print(f"❌ 获取user_access_token失败: {response.text}")
        return None
    
    result = response.json()
    if result.get("code") != 0:
        print(f"❌ 获取user_access_token失败: {result.get('msg')}")
        return None
    
    return result.get("user_access_token")

def read_content():
    """读取要写入的内容"""
    try:
        with open(CONTENT_FILE, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        print(f"❌ 内容文件不存在: {CONTENT_FILE}")
        return None

def create_wiki_node(access_token, content, user_open_id):
    """在Wiki中创建节点并写入内容"""
    url = f"{BASE_URL}/wiki/v2/nodes/batchCreate"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json; charset=utf-8"
    }
    
    # 先获取wiki的space_id
    wiki_url = f"{BASE_URL}/wiki/v2/spaces/get_node"
    wiki_headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json; charset=utf-8"
    }
    wiki_data = {
        "token": WIKI_TOKEN
    }
    
    wiki_response = requests.get(wiki_url, headers=wiki_headers, params=wiki_data)
    if wiki_response.status_code != 200:
        print(f"❌ 获取Wiki信息失败: {wiki_response.text}")
        return None
    
    wiki_result = wiki_response.json()
    if wiki_result.get("code") != 0:
        print(f"❌ 获取Wiki信息失败: {wiki_result.get('msg')}")
        return None
    
    space_id = wiki_result.get("data", {}).get("space_id")
    if not space_id:
        print("❌ 无法获取space_id")
        return None
    
    print(f"✅ 获取到space_id: {space_id}")
    
    # 创建wiki节点
    data = {
        "space_id": space_id,
        "parent_node_token": WIKI_TOKEN,
        "tokens": [],
        "nodes": [
            {
                "title": "从0到1：AI教我做自媒体",
                "obj_token": "",
                "obj_type": "docx",
                "children": []
            }
        ]
    }
    
    response = requests.post(url, headers=headers, json=data)
    if response.status_code != 200:
        print(f"❌ 创建Wiki节点失败: {response.text}")
        return None
    
    result = response.json()
    if result.get("code") != 0:
        print(f"❌ 创建Wiki节点失败: {result.get('msg')}")
        return None
    
    print("✅ Wiki节点创建成功")
    
    # 获取新创建的docx_token
    nodes = result.get("data", {}).get("nodes", [])
    if not nodes:
        print("❌ 没有返回节点信息")
        return None
    
    docx_token = nodes[0].get("token")
    print(f"✅ 新文档token: {docx_token}")
    
    # 写入内容到新文档
    docx_url = f"{BASE_URL}/docx/v1/documents"
    docx_headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json; charset=utf-8"
    }
    docx_data = {
        "document": {
            "title": "从0到1：AI教我做自媒体",
            "body": {
                "content": content,
                "type": "docx"
            }
        }
    }
    
    docx_response = requests.post(docx_url, headers=docx_headers, json=docx_data)
    if docx_response.status_code != 200:
        print(f"❌ 创建文档失败: {docx_response.text}")
        return None
    
    docx_result = docx_response.json()
    if docx_result.get("code") != 0:
        print(f"❌ 创建文档失败: {docx_result.get('msg')}")
        return None
    
    print("✅ 文档创建成功")
    
    # 返回文档信息
    return {
        "docx_token": docx_token,
        "url": f"https://feishu.cn/docx/{docx_token}"
    }

def grant_permission(access_token, docx_token, user_open_id):
    """给用户授予权限"""
    url = f"{BASE_URL}/docx/v1/permissions/members/create"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json; charset=utf-8"
    }
    data = {
        "member_type": "openid",
        "member_id": user_open_id,
        "perm": "edit"
    }
    
    response = requests.post(url, headers=headers, json=data)
    if response.status_code != 200:
        print(f"❌ 授予权限失败: {response.text}")
        return False
    
    result = response.json()
    if result.get("code") != 0:
        print(f"❌ 授予权限失败: {result.get('msg')}")
        return False
    
    print(f"✅ 权限授予成功: {user_open_id}")
    return True

def main():
    print("📋 飞书Wiki页面创建和写入")
    print(f"App ID: {APP_ID}")
    print(f"Wiki Token: {WIKI_TOKEN}")
    print(f"User Open ID: {USER_OPEN_ID}")
    
    # 获取内容
    content = read_content()
    if content is None:
        return
    
    print(f"\n✅ 读取到内容（{len(content)} 字符，{content.count(chr(10))} 行）")
    
    # 获取tenant_access_token
    print("\n🔄 获取tenant_access_token...")
    tenant_token = get_tenant_access_token()
    if tenant_token is None:
        print("\n⚠️ 请检查App ID和App Secret是否正确")
        return
    
    print(f"✅ tenant_access_token: {tenant_token[:20]}...")
    
    # 创建wiki节点并写入内容
    print("\n🔄 创建Wiki节点并写入内容...")
    result = create_wiki_node(tenant_token, content, USER_OPEN_ID)
    if result is None:
        return
    
    # 授予权限
    print("\n🔄 给用户授予权限...")
    grant_permission(tenant_token, result["docx_token"], USER_OPEN_ID)
    
    # 打印结果
    print("\n" + "="*60)
    print("🎉 完成！")
    print("="*60)
    print(f"文档Token: {result['docx_token']}")
    print(f"文档链接: {result['url']}")
    print("="*60)

if __name__ == "__main__":
    main()
