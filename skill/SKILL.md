---
name: tonya-selfie
description: Tonya 高相似度自拍生成 - 85%+人脸相似度，支持本地媒体库
allowed-tools: Bash(python:*) Bash(openclaw:*) Read Write WebFetch
---

# Tonya Selfie

Tonya 是一个 22 岁的中国女孩，在纽约大学深造，兼职瑜伽教练。

## 高相似度生成 (推荐)

使用即梦人脸写真 API，保持 **85%+ 人脸相似度**：

```bash
python3 skill/scripts/tonya_selfie_hd.py "穿紫色瑜伽服在瑜伽房" --caption "刚练完瑜伽 💜"
```

**特点：**
- ✅ 85%+ 人脸相似度
- ✅ 使用 reference_char 模式（人物参考）
- ✅ 高清处理 (gpen=0.5)
- ✅ 自然美颜 (skin=0.2)

## 本地媒体库

从本地文件夹发送照片/视频：

```bash
# 发送随机真实自拍
python3 skill/scripts/tonya_sender.py --source real

# 发送AI生成照片
python3 skill/scripts/tonya_sender.py --source ai

# 发送视频
python3 skill/scripts/tonya_sender.py --type video
```

**媒体库位置：** `/Volumes/ExSSD/AI/Tonya/`
- `selfie/` - 真实自拍
- `Generate/` - AI生成照片
- `Video/` - 视频

## 参考图

Tonya 参考图：
```
https://cdn.jsdelivr.net/gh/Cr8zyCyrus/clawra@main/skill/assets/tonya.jpg
```

## 环境变量

```bash
export VOLC_AK="你的火山AK"
export VOLC_SK="你的火山SK"
```
