# Token监控

配置完成：
- 配额：100万token（估算）
- 阈值：剩余20%预警
- 每天自动汇报使用情况

## 手动命令

```bash
# 查看状态
python3 /root/.openclaw/workspace/scripts/token_monitor.py --status

# 设置准确配额
python3 /root/.openclaw/workspace/scripts/token_monitor.py --set-quota <数量>

# 立即发送日报
python3 /root/.openclaw/workspace/scripts/token_monitor.py --report
```

## 注意

火山引擎没有公开配额查询API，当前是估算值。
如需准确配额，请你去控制台查看后手动设置。
