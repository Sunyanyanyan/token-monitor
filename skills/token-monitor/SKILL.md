---
name: token-monitor
description: Monitor token usage for Volcengine ARK API. Track daily consumption, check remaining quota, send alerts when below threshold.
---

# Token Monitor

Monitor and track Volcengine ARK API token usage.

## Quick Start

Check current status:
```bash
python3 /root/.openclaw/workspace/scripts/token_monitor.py --status
```

Send daily report manually:
```bash
python3 /root/.openclaw/workspace/scripts/token_monitor.py --report
```

Set accurate quota:
```bash
python3 /root/.openclaw/workspace/scripts/token_monitor.py --set-quota <token_count>
```

## Configuration

File: `/root/.openclaw/workspace/config/token_monitor.json`

- `total_quota`: Total token quota (use `--set-quota` to set)
- `threshold_percent`: Alert threshold (default 20%)
- `estimated_quota`: Auto-estimated quota if not set
- `last_daily_report`: Last report date

## Features

- Daily usage tracking
- Automatic daily reports
- Threshold-based alerts
- Feishu notifications

## Note

Volcengine doesn't provide quota query API. Current quota is estimated. Set accurate quota manually for precise monitoring.
