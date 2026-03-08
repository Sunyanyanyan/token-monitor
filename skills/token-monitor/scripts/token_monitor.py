#!/usr/bin/env python3
"""
Token使用监控脚本
统计火山引擎ARK API的token使用情况
"""
import json
import os
import requests
from datetime import datetime, timedelta
from pathlib import Path

CONFIG_FILE = Path("/root/.openclaw/workspace/config/token_monitor.json")
LOG_FILE = Path("/root/.openclaw/workspace/logs/token_usage.log")
STATS_FILE = Path("/root/.openclaw/workspace/stats/token_stats.json")

# 火山引擎API Key
API_KEY = "9a225f97-1692-4ab1-8886-7f7a443dca92"
API_BASE = "https://ark.cn-beijing.volces.com/api/coding/v3"

def load_config():
    default = {
        "total_quota": None,  # 总配额（token数）
        "threshold_percent": 20,  # 预警阈值
        "last_daily_report": None,
        "estimated_quota": None,  # 估算配额
    }
    if CONFIG_FILE.exists():
        with open(CONFIG_FILE) as f:
            return {**default, **json.load(f)}
    return default

def save_config(config):
    CONFIG_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f, indent=2)

def load_stats():
    if STATS_FILE.exists():
        with open(STATS_FILE) as f:
            return json.load(f)
    return {"daily": {}, "total_used": 0}

def save_stats(stats):
    STATS_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(STATS_FILE, 'w') as f:
        json.dump(stats, f, indent=2)

def estimate_from_activity():
    """基于使用情况估算配额"""
    # 如果使用不频繁，可能是小额测试配额
    stats = load_stats()
    recent_days = list(stats["daily"].items())[-7:]  # 最近7天

    if not recent_days:
        return 1000000  # 默认假设100万token

    avg_daily = sum(v for _, v in recent_days) / len(recent_days)

    # 根据日均使用估算配额
    if avg_daily < 1000:
        return 100000  # 10万token
    elif avg_daily < 10000:
        return 1000000  # 100万token
    elif avg_daily < 100000:
        return 10000000  # 1000万token
    else:
        return 50000000  # 5000万token

def get_quota_info():
    """尝试获取配额信息（火山引擎暂无公开API）"""
    config = load_config()

    # 使用估算配额
    if config["estimated_quota"] is None:
        config["estimated_quota"] = estimate_from_activity()
        save_config(config)

    return {
        "total": config["estimated_quota"],
        "source": "estimated",
        "note": "火山引擎未提供配额查询API，使用估算值。如需准确值请手动设置。"
    }

def get_daily_usage():
    """获取今天的token使用量"""
    stats = load_stats()
    today = datetime.now().strftime("%Y-%m-%d")
    return stats["daily"].get(today, 0)

def record_usage(tokens):
    """记录token使用"""
    stats = load_stats()
    today = datetime.now().strftime("%Y-%m-%d")
    stats["daily"][today] = stats["daily"].get(today, 0) + tokens
    stats["total_used"] += tokens
    save_stats(stats)

def check_and_report():
    """检查并汇报"""
    config = load_config()
    quota_info = get_quota_info()
    used = get_daily_usage()
    total = quota_info["total"]
    remaining = total - used
    percent = (remaining / total) * 100

    today = datetime.now().strftime("%Y-%m-%d")

    # 每日报表
    if config["last_daily_report"] != today:
        report = f"""📊 Token使用日报 ({today})
━━━━━━━━━━━━━━━━━━━━━━━━━━
总配额: {total:,} ({quota_info['source']})
今日使用: {used:,}
剩余: {remaining:,} ({percent:.1f}%)
━━━━━━━━━━━━━━━━━━━━━━━━━━
{quota_info['note']}
"""
        send_feishu_message(report)
        config["last_daily_report"] = today
        save_config(config)

    # 预警检查
    if percent < config["threshold_percent"]:
        alert = f"⚠️ Token预警！剩余 {remaining:,} ({percent:.1f}%) < 阈值 {config['threshold_percent']}%"
        send_feishu_message(alert)

    return {
        "total": total,
        "used": used,
        "remaining": remaining,
        "percent": percent
    }

def send_feishu_message(message):
    """发送飞书消息"""
    print(f"[飞书] {message}")
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(LOG_FILE, 'a') as f:
        f.write(f"{datetime.now().isoformat()} {message}\n")

if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        if sys.argv[1] == "--set-quota":
            config = load_config()
            config["estimated_quota"] = int(sys.argv[2])
            save_config(config)
            print(f"已设置配额: {sys.argv[2]:,}")
        elif sys.argv[1] == "--report":
            result = check_and_report()
            print(f"总: {result['total']:,}, 已用: {result['used']:,}, 剩余: {result['remaining']:,} ({result['percent']:.1f}%)")
        elif sys.argv[1] == "--status":
            quota_info = get_quota_info()
            used = get_daily_usage()
            print(f"配额: {quota_info['total']:,} ({quota_info['source']})")
            print(f"今日使用: {used:,}")
    else:
        result = check_and_report()
        print(f"总: {result['total']:,}, 已用: {result['used']:,}, 剩余: {result['remaining']:,} ({result['percent']:.1f}%)")
