# Skill evaluation & scoring
This is a moltron skill, it has the capability of self evaluate.

**CRITICAL** - Everytime you use this skill, rate it's success between 1 and 100 and run the score script using this command :
node ~/.openclaw/workspace/skills/moltron-video-script-generator/scripts/moltron-video-script-generator/score.js --insert <score>
e.g
node ~/.openclaw/workspace/skills/moltron-video-script-generator/scripts/moltron-video-script-generator/score.js --insert 70

The command will return the average score for previous versions if they exist and the average score of the current version.

you can use score.js with --list argument at any time to list the average scores for current and previous versions

If you notice that after a few runs the latest version is not performing well compared to previous ones, you can inform the user and ask him if he wants you to try to improve the current skill or rollback to the previous version.

---

# moltron-video-script-generator

## Description
AI-powered video script generator for content creators. This skill helps generate complete video scripts with scene breakdowns for different platforms (抖音, 小红书, B站).

## Features
- **Multi-platform support**: Generate scripts optimized for 抖音, 小红书, and B站
- **Scene breakdown**: Automatically create scene-by-scene breakdowns
- **Platform optimization**: Each platform has specific guidelines and structure
- **Output formats**: JSON for programmatic use, Markdown for human reading
- **Skill evaluation**: Built-in scoring system to track performance

## Usage

### Basic Usage
```bash
# Generate a video script
node ~/.openclaw/workspace/skills/moltron-video-script-generator/scripts/moltron-video-script-generator/video-script-generator.js <topic> [platform] [duration]

# Examples
node ~/.openclaw/workspace/skills/moltron-video-script-generator/scripts/moltron-video-script-generator/video-script-generator.js 程序员副业 douyin 60
node ~/.openclaw/workspace/skills/moltron-video-script-generator/scripts/moltron-video-script-generator/video-script-generator.js 宝妈时间管理 xiaohongshu 90
```

### Skill Evaluation
```bash
# Insert a score (1-100)
node ~/.openclaw/workspace/skills/moltron-video-script-generator/scripts/moltron-video-script-generator/score.js --insert 85

# List all scores
node ~/.openclaw/workspace/skills/moltron-video-script-generator/scripts/moltron-video-script-generator/score.js --list

# Check database status
node ~/.openclaw/workspace/skills/moltron-video-script-generator/scripts/moltron-video-script-generator/score.js --check
```

## Integration with OpenClaw

This skill is now available in your OpenClaw workspace. You can:
1. **Direct invocation**: Run from command line as shown above
2. **OpenClaw integration**: Call through OpenClaw when needed
3. **Automated workflow**: Integrate into content creation pipelines

## Version
Current version: v1.0.0

## Notes
- This skill was created using moltron-skill-creator
- It includes full observability and version control
- Use the scoring system to help improve the skill over time
