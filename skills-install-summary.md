# OpenClaw 技能安装总结

**安装时间**: 2026-03-06 17:18-17:30

## 已安装的工具

### 1. ClawHub CLI
- **安装命令**: `npm i -g clawhub`
- **功能**: 从 clawhub.com 搜索、安装、更新和发布代理技能
- **状态**: ✅ 已安装

### 2. Summarize
- **安装命令**: `npm install -g summarize`
- **功能**: 总结或提取 URL、播客和本地文件的文本/转录
- **状态**: ✅ 已安装
- **用途**:
  - 总结网页文章
  - 提取 YouTube 视频转录（最佳尝试）
  - 总结 PDF 文件
  - 支持多种模型（OpenAI, Anthropic, xAI, Google）

### 3. GitHub CLI (gh)
- **安装命令**: `apt install -y gh`
- **版本**: 2.4.0+dfsg1
- **功能**: GitHub 操作（issues, PRs, CI runs, 代码审查）
- **状态**: ✅ 已安装
- **注意**: 需要运行 `gh auth login` 进行认证

## 可用的技能

### 已启用技能（通过内置）
- ✅ feishu-doc - 飞书文档读写
- ✅ feishu-drive - 飞书云存储
- ✅ feishu-perm - 飞书权限管理
- ✅ feishu-wiki - 飞书知识库
- ✅ healthcheck - 系统安全检查
- ✅ tmux - 远程控制 tmux
- ✅ weather - 天气查询
- ✅ skill-creator - 技能创建

### 新增可用技能（需要配置）
- 🆕 **summarize** - 网页/视频/文件总结
- 🆕 **github** - GitHub 操作（需认证）
- 🆕 **coding-agent** - 代码代理（（需安装 codex/claude/pi）
- 🆕 **slack** - Slack 控制（需配置）

## 下一步建议

### 1. 配置 GitHub CLI
```bash
gh auth login
```

### 2. 配置 Summarize
```bash
# 设置 API Key（选择一个）
export OPENAI_API_KEY="your-key"
# 或
export ANTHROPIC_API_KEY="your-key"
# 或
export GEMINI_API_KEY="your-key"
```

### 3. 测试新技能
- 让我总结一个 URL
- 让我检查 GitHub 仓库状态
- 让我创建新的技能

## 权限状态

已启用的工具：
- ✅ read - 读取文件
- ✅ exec - 执行命令
- ✅ write - 写入文件
- ✅ edit - 编辑文件
- ✅ process - 进程管理
- ✅ web_search - 网络搜索（需配置 API Key）
- ✅ web_fetch - 网络获取
