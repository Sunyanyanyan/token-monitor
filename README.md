# Token Monitor

Monitor Volcengine ARK API token usage.

## Setup

```bash
# Set quota
python3 /root/.openclaw/workspace/scripts/token_monitor.py --set-quota <amount>

# Check status
python3 /root/.openclaw/workspace/scripts/token_monitor.py --status
```

## Features

- Daily usage tracking
- Auto alerts at 20% threshold
- Feishu notifications
