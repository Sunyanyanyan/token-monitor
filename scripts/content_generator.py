#!/usr/bin/env python3
"""
视频内容生产工具
生成脚本、AI语音、视觉素材
"""
import json
from pathlib import Path

CONTENT_DIR = Path("/root/.openclaw/workspace/content")
OUTPUT_DIR = Path("/root/.openclaw/workspace/output/videos")

def generate_video_script(topic, style="教育类"):
    """生成视频脚本"""
    prompts = {
        "程序员副业": {
            "title": "程序员下班后还能做什么？",
            "duration": "90秒",
            "style": "技术分享+成长激励",
            "segments": [
                {"time": "0-3s", "type": "标题", "content": "程序员下班后只能打游戏？"},
                {"time": "3-18s", "type": "痛点", "content": "每天写CRUD，感觉自己像个机器"},
                {"time": "18-38s", "type": "机会", "content": "每天1小时，一个月30小时"},
                {"time": "38-68s", "type": "方法", "content": "搭网站、做工具、写博客"},
                {"time": "68-80s", "type": "行动", "content": "下期手把手教你0成本搭网站"},
            ]
        }
    }

    return prompts.get(topic, {}).get("segments", [])

def generate_social_post(topic, platform="douyin"):
    """生成社交媒体文案"""
    posts = {
        "douyin": """
程序员下班后只能打游戏？🤔

做了5年Java，每天都在写CRUD，感觉自己越来越废...
其实每天只要1小时，一个月就有30小时！

下期手把手教你：0成本搭个人网站
关注我，一起搞副业！🚀

#程序员 #副业 #个人成长 #Java #技术博主
        """.strip(),
        "xiaohongshu": """
👩‍💻 程序员的下班时间怎么用？

做了5年Java，每天都在重复写增删改查...
直到我发现：每天1小时=30小时/月！

💡 3个方向：
✅ 搭建个人网站
✅ 做AI自动化工具
✅ 接外包项目

下期视频手把手教你：0成本搭个人网站
关注我，一起做个有副业的程序员～

#程序员 #副业 #个人成长 #java #技术博主 #职场
        """.strip()
    }
    return posts.get(platform, "")

def save_content(topic, data):
    """保存内容到文件"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # 保存脚本
    script_file = CONTENT_DIR / f"scripts/{topic}_{timestamp}.json"
    script_file.parent.mkdir(exist_ok=True)
    with open(script_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    # 保存文案
    for platform in ["douyin", "xiaohongshu"]:
        post_file = CONTENT_DIR / f"posts/{platform}/{topic}_{timestamp}.md"
        post_file.parent.mkdir(parents=True, exist_ok=True)
        with open(post_file, 'w', encoding='utf-8') as f:
            f.write(generate_social_post(topic, platform))
    
    return {
        "script": str(script_file),
        "posts": {
            "douyin": str(CONTENT_DIR / f"posts/douyin/{topic}_{timestamp}.md"),
            "xiaohongshu": str(CONTENT_DIR / f"posts/xiaohongshu/{topic}_{timestamp}.md")
        }
    }

if __name__ == "__main__":
    from datetime import datetime
    
    # 演示：生成程序员副业主题内容
    topic = "程序员副业"
    script = generate_video_script(topic)
    result = save_content(topic, script)
    
    print(f"✅ 已生成 {topic} 主题内容：")
    print(f"   脚本: {result['script']}")
    print(f"   抖音文案: {result['posts']['douyin']}")
    print(f"   小红书文案: {result['posts']['xiaohongshu']}")
