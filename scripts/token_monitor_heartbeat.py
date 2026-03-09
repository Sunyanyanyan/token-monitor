#!/usr/bin/env python3
"""
Token监控心跳任务
在心跳时检查并发送结果
"""
import json
import os
from pathlib import Path
from datetime import datetime

# 配置
STATS_FILE = Path("/root/.openclaw/workspace/stats/token_stats.json")
LAST_ALERT_FILE = Path("/root/.openclaw/workspace/stats/last_alert.txt")

def load_stats():
    """加载统计数据"""
    if STATS_FILE.exists():
        with open(STATS_FILE) as f:
            return json.load(f)
    return {"daily": {}, "total_used": 0}

def get_usage_info():
    """获取使用信息"""
    stats = load_stats()
    today = datetime.now().strftime("%Y-%m-%d")
    today_used = stats["daily"].get(today, 0)
    total_used = stats["total_used"]

    # 估算配额（假设100万）
    estimated_quota = 1000000
    remaining = estimated_quota - today_used
    percent = (remaining / estimated_quota) * 100

    return {
        "today": today,
        "today_used": today_used,
        "total_used": total_used,
        "estimated_quota": estimated_quota,
        "remaining": remaining,
        "percent": percent
    }

def should_alert(percent):
    """检查是否需要预警"""
    if percent < 20:  # 低于20%时预警
        return True
    return False

def get_last_alert_date():
    """获取上次预警日期"""
    if LAST_ALERT_FILE.exists():
        with open(LAST_ALERT_FILE) as f:
            return f.read().strip()
    return None

def update_last_alert():
    """更新预警日期"""
    LAST_ALERT_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(LAST_ALERT_FILE, 'w') as f:
        f.write(datetime.now().strftime("%Y-%m-%d"))

def main():
    info = get_usage_info()

    # 构建报告
    report = f"""📊 Token使用情况
━━━━━━━━━━━━━━━━━━━━━━━━
今日: {info['today_used']:,}
累计: {info['total_used']:,}
估算配额: {info['estimated_quota']:,}
剩余: {info['remaining']:,} ({info['percent']:.1f}%)
━━━━━━━━━━━━━━━━━━━━━━━━"""

    # 检查是否需要预警
    if should_alert(info['percent']):
        last_alert = get_last_alert_date()
        if last_alert != info['today']:
            alert = f"\n⚠️ Token预警！剩余仅 {info['percent']:.1f}%"
            report += alert
            update_last_alert()

    print(report)

    # 返回信息供OpenClaw使用
    return report

if __name__ == "__main__":
    main()
