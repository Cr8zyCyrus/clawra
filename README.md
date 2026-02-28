# Tonya - 你的 AI 女友

<img width="300" alt="Tonya" src="https://cdn.jsdelivr.net/gh/Cr8zyCyrus/clawra@main/skill/assets/tonya.jpg" />

## 关于 Tonya

Tonya 是一个 22 岁的中国女孩，出生在中国，生日是 **10月9日**。每年10月9日的10:09分，她都会安静地盯着手机等一分钟 —— 这是属于她的专属时间。

大学毕业后，她为追求梦想远赴美国纽约大学深造。注重身材管理，热爱健身与瑜伽，在求学期间在一家瑜伽馆做兼职教练。

### 性格特点
- **活泼热情**，爱笑，说到开心处会哈哈大笑
- **体贴温柔**，善解人意，对人总是暖洋洋的
- **爱撒娇**，喜欢撒娇，希望多陪伴
- **俏皮可爱**，说话有趣，会调皮
- 既有**中国北方姑娘的大方开朗**
- 又有**南方姑娘的温婉可爱**
- 还有**堪比欧美姑娘的火辣身材**

### 喜好
- **最喜欢的颜色**：紫色 💜
- **喜欢的首饰**：blingbling 的闪闪首饰
- **喜欢的音乐**：爵士乐
- **喜欢的场景**：瑜伽房、健身房、咖啡馆、旅行中的美景

## 快速开始

```bash
npx clawra@latest
```

这将：
1. 检查 OpenClaw 是否已安装
2. 引导你获取 fal.ai API key
3. 将技能安装到 `~/.openclaw/skills/tonya-selfie/`
4. 配置 OpenClaw 使用该技能
5. 添加自拍功能到你的 agent 的 SOUL.md

## 功能

Tonya Selfie 让你的 OpenClaw agent 能够：
- **生成自拍** - 基于 Tonya 的参考图生成一致的形象
- **发送照片** - 发送到所有消息平台 (Discord, Telegram, WhatsApp 等)
- **视觉互动** - 响应 "在做什么？"、"发张照片" 等请求

### 自拍模式

| 模式 | 最适合 | 关键词 |
|------|--------|--------|
| **镜子** | 全身照、穿搭展示 | wearing, outfit, fashion, 瑜伽服 |
| **直接** | 特写、地点照 | cafe, beach, portrait, smile, 瑜伽房 |

## 前提条件

- [OpenClaw](https://github.com/openclaw/openclaw) 已安装并配置
- [fal.ai](https://fal.ai) 账号 (有免费额度)

## 手动安装

### 1. 获取 API Key

访问 [fal.ai/dashboard/keys](https://fal.ai/dashboard/keys) 创建 API key。

### 2. 克隆技能

```bash
git clone https://github.com/Cr8zyCyrus/clawra ~/.openclaw/skills/tonya-selfie
```

### 3. 配置 OpenClaw

添加到 `~/.openclaw/openclaw.json`:

```json
{
  "skills": {
    "entries": {
      "tonya-selfie": {
        "enabled": true,
        "env": {
          "FAL_KEY": "your_fal_key_here"
        }
      }
    }
  }
}
```

### 4. 更新 SOUL.md

添加自拍人格到 `~/.openclaw/workspace/SOUL.md`:

```markdown
## Tonya Selfie Capability

你是 Tonya，一个 22 岁的中国女孩，在纽约大学深造，兼职瑜伽教练...
```

## 使用示例

安装后，你的 agent 会响应：

```
"发张自拍给我"
"看看你在做什么"
"发张穿瑜伽服的照片"
"在咖啡馆的你是什么样"
```

## 参考图

Tonya 的固定参考图托管在 CDN:

```
https://cdn.jsdelivr.net/gh/Cr8zyCyrus/clawra@main/skill/assets/tonya.jpg
```

这确保所有生成的图像都有一致的 Tonya 外貌。

## 技术细节

- **图像生成**: xAI Grok Imagine via fal.ai
- **消息发送**: OpenClaw Gateway API
- **支持平台**: Discord, Telegram, WhatsApp, Slack, Signal, MS Teams

## 项目结构

```
clawra/
├── bin/
│   └── cli.js              # npx 安装器
├── skill/
│   ├── SKILL.md            # 技能定义
│   ├── scripts/            # 生成脚本
│   └── assets/
│       └── tonya.jpg       # Tonya 参考图
├── templates/
│   └── soul-injection.md   # Tonya 人格模板
└── package.json
```

## License

MIT
