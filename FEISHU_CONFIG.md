# Tonya 飞书 Bot 配置 v1.1.0

**更新日期**: 2026-03-02

## 新增功能

### 1. 飞书 Bot 集成 ✅
- **账号**: `tonya-feishu`
- **App ID**: `cli_a92f9f59b6e21bd2`
- **状态**: 已验证成功
- **功能**: 支持发送语音、图片、文件

### 2. 即梦AI图片生成4.0 接口 ✅
- **接口**: `jimeng_t2i_v40`（比 v30 效果更好）
- **参考图**: `/Volumes/ExSSD/AI/Tonya/tonya-smile.jpg`
- **scale**: `0.5`
- **提示词模板**: "以图片人物相貌为基准，生成她[场景]，只参考她的相貌，不要参考着装及背景"

### 3. 飞书发送配置
```bash
# 复制到临时目录
TMP_ID=$(date +%s)_$RANDOM
cp "/path/to/file" ~/.openclaw/workspace/.send-temp/"file.tmp.$TMP_ID"

# 发送
openclaw message send --channel feishu --path "./.send-temp/file.tmp.$TMP_ID"

# 清理
rm ~/.openclaw/workspace/.send-temp/*.tmp.*
```

## 使用方法

### 生成自拍并发送到飞书
```bash
python3 skill/scripts/tonya_selfie_feishu.py "穿紫色瑜伽服" --caption "刚练完瑜伽 💜"
```

## 验证记录
- ✅ 2026-03-02 成功发送语音文件
- ✅ 2026-03-02 成功发送图片
- ✅ 2026-03-02 成功生成自拍（jimeng_t2i_v40）

---
**注意**: 此配置包含敏感信息，请保持仓库私有。
