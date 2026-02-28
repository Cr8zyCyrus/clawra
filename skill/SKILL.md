---
name: tonya-selfie
description: Tonya 多媒体发送 - 本地照片/视频库 + AI生成，发送到消息平台
allowed-tools: Bash(python:*) Bash(openclaw:*) Read Write WebFetch
---

# Tonya Selfie

Tonya 是一个 22 岁的中国女孩，在纽约大学深造，兼职瑜伽教练。这个技能让她能：
- 从本地媒体库发送自拍/视频
- 基于参考图 AI 生成新自拍
- 发送到消息平台 (Telegram)

## 参考图

Tonya 的参考图托管在 GitHub CDN:
```
https://cdn.jsdelivr.net/gh/Cr8zyCyrus/clawra@main/skill/assets/tonya.jpg
```

## 本地媒体库

Tonya 有三个媒体文件夹：

| 文件夹 | 路径 | 内容 |
|--------|------|------|
| **selfie** | `/Volumes/ExSSD/AI/Tonya/selfie/` | 真实自拍及生活照 |
| **Generate** | `/Volumes/ExSSD/AI/Tonya/Generate/` | AI生成的照片 |
| **Video** | `/Volumes/ExSSD/AI/Tonya/Video/` | 视频录像 |

## 使用方法

### 1. 从本地媒体库发送

**发送随机自拍：**
```bash
python3 skill/scripts/tonya_sender.py --type selfie --source any
```

**发送真实照片：**
```bash
python3 skill/scripts/tonya_sender.py --source real --caption "给你看看我之前的样子 💜"
```

**发送AI生成照片：**
```bash
python3 skill/scripts/tonya_sender.py --source ai --caption "这张是AI生成的~"
```

**发送视频：**
```bash
python3 skill/scripts/tonya_sender.py --type video --caption "给你看个视频 💜"
```

**按关键词筛选：**
```bash
python3 skill/scripts/tonya_sender.py --keyword "瑜伽" --caption "瑜伽时光 💜"
```

### 2. AI 生成并发送

```bash
python3 skill/scripts/tonya_selfie.py "在瑜伽房练瑜伽"
```

### 3. 查看媒体库统计

```bash
python3 skill/scripts/tonya_sender.py --type stats
```

## Tonya 人设

见 `templates/soul-injection.md`

## 依赖

- **图像生成**: 即梦图生图 API (jimeng_image2image)
- **本地媒体**: 从 `/Volumes/ExSSD/AI/Tonya/` 读取
- **消息发送**: Telegram Bot API

## 环境变量

```bash
export VOLC_AK="你的火山AK"
export VOLC_SK="你的火山SK"
```
