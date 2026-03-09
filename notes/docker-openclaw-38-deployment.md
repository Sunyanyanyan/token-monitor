# Docker部署OpenClaw 3.8方案

> **核心原则**：确保始终有可用的OpenClaw
> **执行策略**：先测试，后迁移，每步可回滚

---

## 🎯 方案概述

### 目标
- 部署最新版OpenClaw 3.8（Docker）
- 保留现有版本3.2（npm全局安装）
- 确保迁移过程中始终有可用助手

---

## 📋 三阶段执行流程

### 阶段1：Docker独立测试（最安全）

**目标**：验证Docker能否运行OpenClaw

**操作**：
```bash
# 1. 创建临时Docker容器（不挂载任何配置）
docker run -d \
  --name openclaw-test \
  -p 18791:18790 \
  openclaw:latest

# 2. 测试是否启动
docker ps | grep openclaw-test

# 3. 测试基本功能
# - 启动网关
# - 连接频道
# - 运行agent

# 4. 结果处理
# 成功：进入阶段2
# 失败：删除容器，继续用旧版（不受影响）
```

**安全保障**：
- ✅ 完全不影响现有OpenClaw
- ✅ 失败就删除容器
- ✅ 旧版本持续可用

---

### 阶段2：配置挂载测试

**目标**：验证Docker能否加载现有配置

**操作**：
```bash
# 1. 停止临时容器
docker stop openclaw-test
docker rm openclaw-test

# 2. 创建带配置的容器（旧版仍在运行！）
docker run -d \
  --name openclaw-config-test \
  -p 18791:18790 \
  -v ~/.openclaw:/root/.openclaw \
  -v ~/.openclaw/workspace:/root/.openclaw/workspace \
  openclaw:latest

# 3. 测试配置加载
# - 验证频道连接
# - 验证技能加载
# - 验证所有功能

# 4. 结果处理
# 成功：进入阶段3
# 失败：删除容器，继续用旧版（不受影响）
```

**安全保障**：
- ✅ 旧版OpenClaw仍在运行
- ✅ 失败就删除容器，旧版立即可用
- ✅ 配置数据安全

---

### 阶段3：切换使用（最后一步）

**目标**：从旧版切换到Docker版

**操作**：
```bash
# 1. 备份现有数据
cp -r ~/.openclaw ~/.openclaw.backup
echo "✅ 备份完成"

# 2. 停止旧版OpenClaw网关
openclaw gateway stop
echo "⚠️ 旧版网关已停止（但数据保留）"

# 3. 启动Docker版
docker start openclaw-config-test
echo "✅ Docker版启动"

# 4. 完整功能测试
# - 频道连接
# - agent响应
# - 所有技能
# - 插件功能

# 5. 结果处理
# 成功：迁移完成！可以卸载旧版
# 失败：立即回滚到旧版
```

**安全保障**：
- ✅ 完整备份（~/.openclaw.backup）
- ✅ 失败立即回滚
- ✅ 旧版随时可恢复

---

## 🛡️ 安全保障机制

### 1. 三重保障
- **先测试**：Docker独立运行，不依赖现有环境
- **后迁移**：确认可用才考虑迁移配置
- **每步回滚**：任何步骤失败都可立即回滚

### 2. 回滚方案
```bash
# 阶段1失败
docker rm openclaw-test
# → 旧版OpenClaw继续运行

# 阶段2失败
docker stop openclaw-config-test
docker rm openclaw-config-test
# → 旧版OpenClaw继续运行

# 阶段3失败
docker stop openclaw-config-test
openclaw gateway start
# → 立即回滚到旧版
```

### 3. 端口隔离
```
旧版：端口18790（默认）
Docker：端口18791（测试期间）
```

### 4. 数据安全
```
阶段3开始前：完整备份 ~/.openclaw.backup
迁移失败：立即恢复备份
```

---

## 📊 时间估算

| 阶段 | 时间 | 说明 |
|--------|------|------|
| 阶段1：独立测试 | 10-15分钟 | 创建容器+功能测试 |
| 阶段2：配置测试 | 5-10分钟 | 挂载配置+验证 |
| 阶段3：切换使用 | 5-8分钟 | 停旧版+启动Docker+测试 |
| **总计** | **20-33分钟** | |

---

## ✅ 执行原则

### 1. 始终保留旧版本
- 直到Docker完全可用
- 任何时间都可以切回

### 2. 分步骤确认
```
我：准备执行步骤X
这会影响：XXX
确认吗？(y/n)
你：y
我：执行...
```

### 3. 阶段汇报
```
我：阶段1完成 ✅
你：继续
我：阶段2开始...
```

### 4. 失败立即回滚
```
任何步骤失败
→ 立即回滚
→ 告诉你原因
→ 确保旧版可用
```

---

## 🎯 当前状态

### 保存信息
- ✅ 方案已记录
- ✅ 准备好执行
- ⏸ 等待你的指令

### 执行时机
当你需要时，告诉我：
```
"开始Docker部署"
```

我会按上述方案执行，确保安全。

---

## 💡 备注

### OpenClaw版本
- 当前版本：2026.3.2（npm全局安装）
- 目标版本：2026.3.8（Docker部署）

### 已知配置
- 工作目录：/root/.openclaw/workspace
- 飞书token：I3U2wdQmXiOJLFkd9X4cbUtYngg
- Git仓库：https://github.com/Sunyanyanyan/token-monitor
- Moltron项目：~/moltron/projects/moltron-video-script-generator

---

*方案保存时间：2026-03-09 19:50*
*状态：已保存，等待执行*
