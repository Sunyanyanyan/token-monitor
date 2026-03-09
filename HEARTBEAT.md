# 心跳检查任务

## 项目进度跟踪
每30分钟检查一次：
```bash
python3 /root/.openclaw/workspace/scripts/heartbeat-project-tracker.py
```
- 查看 GitHub 仓库更新
- 检查 content/ 目录变化
- 更新今日工作日志
- 提醒待办事项

## 记忆维护
每天检查一次：
```bash
python3 /root/.openclaw/workspace/scripts/heartbeat-memory-maintainer.py
```
- 阅读最近3天的 memory/ 文件
- 提取重要事件到 MEMORY.md
- 更新项目状态

## Token监控
每30分钟检查一次：
```bash
python3 /root/.openclaw/workspace/scripts/token_monitor.py
```
