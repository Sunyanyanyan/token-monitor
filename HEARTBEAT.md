# 心跳检查任务

## 统一入口
所有心跳任务（每30分钟）：
```bash
python3 /root/.openclaw/workspace/scripts/run_heartbeat.py
```

## 包含的任务

### 1. 项目进度跟踪
- 查看 GitHub 仓库更新
- 检查 content/ 目录变化
- 更新今日工作日志
- 提醒待办事项

### 2. Token监控
- 检查今日token使用量
- 剩余低于20%时预警
- 发送使用统计报告

### 3. 记忆维护
- 阅读最近3天的 memory/ 文件
- 提取重要事件到 MEMORY.md
- 更新项目状态
