#!/usr/bin/env python3
"""
Tonya Selfie Generator - 高相似度版本
使用即梦人脸写真 API，保持 85%+ 人脸相似度
"""

import os
import sys
import json
import subprocess
import urllib.request
import ssl

# 添加 workspace 到路径以导入 jimeng_portrait
sys.path.insert(0, '/Users/zhaiteng/.openclaw/workspace')

from jimeng_portrait import generate_portrait

# Tonya 参考图路径
TONYA_REFERENCE_PATH = "/Users/zhaiteng/.openclaw/skills/tonya-selfie/skill/assets/tonya.jpg"

def detect_mode(user_context: str) -> str:
    """根据用户描述自动检测自拍模式"""
    mirror_keywords = ['outfit', 'wearing', 'clothes', 'dress', 'suit', 'fashion', 'full-body', 'mirror', '瑜伽服', '穿搭', '服装', '镜子', '全身']
    direct_keywords = ['cafe', 'restaurant', 'beach', 'park', 'city', 'close-up', 'portrait', 'face', 'eyes', 'smile', '咖啡馆', '特写', '自拍', '大头', '近照']
    
    context_lower = user_context.lower()
    
    for kw in direct_keywords:
        if kw in context_lower:
            return 'direct'
    
    for kw in mirror_keywords:
        if kw in context_lower:
            return 'mirror'
    
    return 'direct'  # 默认特写模式，更适合人脸写真

def build_prompt(user_context: str, mode: str) -> str:
    """构建生成提示词 - 针对人脸写真优化"""
    if mode == 'mirror':
        # 镜子自拍模式 - 全身/穿搭
        return f"镜子自拍，{user_context}，全身照，对着镜子拍摄，展示穿搭，高清画质，自然光线，真实感"
    else:
        # 直接自拍模式 - 特写/场景（更适合人脸写真）
        return f"{user_context}，直接看着镜头，眼神明亮，表情自然，手机自拍角度，高清画质，柔和光线"

def send_to_telegram(image_path: str, caption: str = ""):
    """发送图片到 Telegram"""
    bot_token = "8784896214:AAH3ug8O_87Bsx22ur1EMQ1846A2BCT7yhM"
    chat_id = "8608938384"
    
    url = f"https://api.telegram.org/bot{bot_token}/sendPhoto"
    cmd = [
        "curl", "-s", "-X", "POST", url,
        "-F", f"chat_id={chat_id}",
        "-F", f"photo=@{image_path}"
    ]
    
    if caption:
        cmd.extend(["-F", f"caption={caption}"])
    
    print(f"Sending to Telegram...")
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode == 0 and '"ok":true' in result.stdout:
        print(f"✅ 发送成功!")
        return True
    else:
        print(f"❌ 发送失败: {result.stderr}")
        return False

def generate_tonya_selfie(user_context: str, mode: str = "auto", send: bool = True, caption: str = None):
    """
    生成 Tonya 高相似度自拍
    
    使用即梦人脸写真 API (i2i_portrait_photo)，保持 85%+ 人脸相似度
    
    Args:
        user_context: 用户描述 (如 "在瑜伽房"、"穿紫色连衣裙")
        mode: 'mirror' | 'direct' | 'auto'
        send: 是否发送到 Telegram
        caption: 图片说明文字
    
    Returns:
        生成的图片路径
    """
    # 自动检测模式
    if mode == 'auto':
        mode = detect_mode(user_context)
        print(f"Auto-detected mode: {mode}")
    
    # 构建提示词
    prompt = build_prompt(user_context, mode)
    print(f"Prompt: {prompt}")
    
    # 使用即梦人脸写真生成（85%+相似度）
    print("Generating Tonya selfie with portrait mode (85%+ face similarity)...")
    print("⏳ 这可能需要 20-40 秒...")
    
    result = generate_portrait(
        image_source=TONYA_REFERENCE_PATH,
        prompt=prompt,
        width=1328,
        height=1328,
        gen_mode='reference_char',  # 人物参考模式 - 保持人脸特征
        gpen=0.5,   # 高清处理（0-1，越高越清晰）
        skin=0.2,   # 美颜效果（0-1，越低越自然）
        skin_unifi=0,  # 匀肤效果
        seed=-1,    # 随机种子
        use_base64=True,
        download=True
    )
    
    if not result:
        raise Exception("Failed to generate portrait")
    
    # 处理返回结果
    if isinstance(result, list):
        generated_path = result[0]
    else:
        generated_path = result
    
    print(f"✅ 生成成功: {generated_path}")
    
    # 发送到 Telegram
    if send:
        default_caption = caption or "我的自拍 💜 像不像我~"
        send_to_telegram(generated_path, default_caption)
    
    return generated_path

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Generate Tonya selfie with high face similarity (85%+)")
    parser.add_argument("context", help="Description of the scene/outfit (e.g., '在瑜伽房练瑜伽')")
    parser.add_argument("--mode", choices=['mirror', 'direct', 'auto'], default='auto', help="Selfie mode")
    parser.add_argument("--no-send", action='store_true', help="Don't send to Telegram, just save locally")
    parser.add_argument("--caption", help="Image caption")
    
    args = parser.parse_args()
    
    try:
        result = generate_tonya_selfie(
            user_context=args.context,
            mode=args.mode,
            send=not args.no_send,
            caption=args.caption
        )
        print(f"✅ Done! Saved to: {result}")
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)
