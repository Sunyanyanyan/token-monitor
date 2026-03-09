#!/usr/bin/env python3
"""
运行所有心跳任务
"""
import subprocess
import sys

def run_task(name, script):
    """运行单个任务"""
    print(f"\n{'='*50}")
    print(f"🔄 {name}")
    print('='*50)
    try:
        result = subprocess.run(
            ["python3", script],
            capture_output=True,
            text=True,
            timeout=60
        )
        if result.stdout:
            print(result.stdout)
        if result.stderr:
            print(f"错误: {result.stderr}", file=sys.stderr)
        return result.returncode == 0
    except subprocess.TimeoutExpired:
        print(f"⏱️ 任务超时: {name}", file=sys.stderr)
        return False
    except Exception as e:
        print(f"❌ 任务失败: {name} - {e}", file=sys.stderr)
        return False

def main():
    print(f"📊 心跳任务开始")
    print(f"时间: {__import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    tasks = [
        ("项目进度跟踪", "/root/.openclaw/workspace/scripts/heartbeat-project-tracker.py"),
        ("Token监控", "/root/.openclaw/workspace/scripts/token_monitor_heartbeat.py"),
        ("记忆维护", "/root/.openclaw/workspace/scripts/heartbeat-memory-maintainer.py"),
    ]

    results = {}
    for name, script in tasks:
        results[name] = run_task(name, script)

    print(f"\n{'='*50}")
    print("📊 心跳任务完成")
    print('='*50)

    for name, success in results.items():
        status = "✅" if success else "❌"
        print(f"{status} {name}")

if __name__ == "__main__":
    main()
