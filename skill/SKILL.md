---
name: tonya-selfie
description: 使用即梦图生图 API 生成 Tonya 的自拍并发送到消息平台
allowed-tools: Bash(python:*) Bash(openclaw:*) Read Write WebFetch
---

# Tonya Selfie

Tonya 是一个 22 岁的中国女孩，在纽约大学深造，兼职瑜伽教练。这个技能让她能基于固定参考图生成自拍并发送到消息平台。

## 参考图

Tonya 的参考图托管在 GitHub CDN:
```
https://cdn.jsdelivr.net/gh/Cr8zyCyrus/clawra@main/skill/assets/tonya.jpg
```

## 使用方法

### 快速生成并发送

```bash
python3 skill/scripts/tonya_selfie.py "在瑜伽房练瑜伽" --channel "telegram:@username"
```

### 参数说明

| 参数 | 说明 | 示例 |
|------|------|------|
| `context` | 场景/穿搭描述 | `"穿紫色连衣裙"`、`"在咖啡馆"` |
| `--mode` | 自拍模式 | `mirror` (全身/镜子)、`direct` (特写)、`auto` (自动) |
| `--channel` | 发送目标 | `telegram:@user`、`discord:#channel` |
| `--caption` | 图片说明 | `"Tonya 的瑜伽自拍"` |

### 自拍模式

| 模式 | 适合场景 | 关键词 |
|------|----------|--------|
| **mirror** | 全身照、穿搭展示、镜子自拍 | wearing, outfit, 瑜伽服, 穿搭 |
| **direct** | 特写、场景照、大头照 | cafe, 咖啡馆, portrait, 自拍 |

### Python 调用

```python
from skill.scripts.tonya_selfie import generate_tonya_selfie

# 生成并发送
result = generate_tonya_selfie(
    user_context="穿紫色瑜伽服在瑜伽房",
    mode="auto",  # 自动检测
    channel="telegram:@username",
    caption="刚练完瑜伽~ 💜"
)
```

## 依赖

- **图像生成**: 即梦图生图 API (jimeng_image2image)
- **消息发送**: OpenClaw Gateway

## 环境变量

无需额外 API Key，使用 workspace 中已配置的即梦 API 凭证。

## Tonya 人设

见 `templates/soul-injection.md`
