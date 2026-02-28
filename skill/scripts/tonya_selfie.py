#!/usr/bin/env python3
"""
Tonya Selfie Generator
使用即梦图生图 API 生成 Tonya 的自拍
"""

import os
import sys
import json
import subprocess
import urllib.request
import ssl

# 添加 workspace 到路径以导入 jimeng_image2image
sys.path.insert(0, '/Users/zhaiteng/.openclaw/workspace')

from jimeng_image2image import generate_image_from_image

# Tonya 参考图 URL (GitHub CDN)
TONYA_REFERENCE_URL = "https://cdn.jsdelivr.net/gh/Cr8zyCyrus/clawra@main/skill/assets/tonya.jpg"
DEFAULT_DOWNLOAD_DIR = "/Volumes/ExSSD/AI"

ssl_context = ssl.create_default_context()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE

def download_reference_image():
    """下载 Tonya 参考图到本地"""
    local_path = os.path.join(DEFAULT_DOWNLOAD_DIR, "tonya_reference.jpg")
    
    if os.path.exists(local_path):
        return local_path
    
    print(f"Downloading Tonya reference image...")
    try:
        req = urllib.request.Request(TONYA_REFERENCE_URL, headers={
            'User-Agent': 'Mozilla/5.0'
        })
        with urllib.request.urlopen(req, context=ssl_context, timeout=30) as resp:
            with open(local_path, 'wb') as f:
                f.write(resp.read())
        print(f"Reference image saved to: {local_path}")
        return local_path
    except Exception as e:
        raise Exception(f"Failed to download reference image: {e}")

def detect_mode(user_context: str) -> str:
    """根据用户描述自动检测自拍模式"""
    mirror_keywords = ['outfit', 'wearing', 'clothes', 'dress', 'suit', 'fashion', 'full-body', 'mirror', '瑜伽服', '穿搭', '服装', '镜子']
    direct_keywords = ['cafe', 'restaurant', 'beach', 'park', 'city', 'close-up', 'portrait', 'face', 'eyes', 'smile', '咖啡馆', '特写', '自拍', '大头']
    
    context_lower = user_context.lower()
    
    for kw in direct_keywords:
        if kw in context_lower:
            return 'direct'
    
    for kw in mirror_keywords:
        if kw in context_lower:
            return 'mirror'
    
    return 'mirror'  # 默认模式

def build_prompt(user_context: str, mode: str) -> str:
    """构建生成提示词"""
    if mode == 'direct':
        # 直接自拍模式 - 特写/场景
        return f"自拍特写，{user_context}，直接看着镜头，眼神明亮，表情自然，手机自拍角度，高清画质"
    else:
        # 镜子自拍模式 - 全身/穿搭
        return f"镜子自拍，{user_context}，全身照，对着镜子拍摄，展示穿搭，高清画质"

def send_to_openclaw(image_path: str, channel: str, caption: str = ""):
    """使用 OpenClaw 发送图片到消息平台"""
    import subprocess
    
    cmd = [
        'openclaw', 'message', 'send',
        '--action', 'send',
        '--channel', channel,
        '--media', image_path
    ]
    
    if caption:
        cmd.extend(['--message', caption])
    
    print(f"Sending to {channel}...")
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode == 0:
        print(f"✅ Image sent successfully!")
    else:
        print(f"❌ Failed to send: {result.stderr}")
        raise Exception(f"OpenClaw send failed: {result.stderr}")

def generate_tonya_selfie(user_context: str, mode: str = "auto", channel: str = None, caption: str = None):
    """
    生成 Tonya 自拍并发送
    
    Args:
        user_context: 用户描述 (如 "在瑜伽房"、"穿紫色连衣裙")
        mode: 'mirror' | 'direct' | 'auto'
        channel: 发送目标频道/用户 (如 'telegram:@username')
        caption: 图片说明文字
    """
    # 自动检测模式
    if mode == 'auto':
        mode = detect_mode(user_context)
        print(f"Auto-detected mode: {mode}")
    
    # 下载参考图
    reference_path = download_reference_image()
    
    # 构建提示词
    prompt = build_prompt(user_context, mode)
    print(f"Prompt: {prompt}")
    
    # 使用即梦图生图生成
    print("Generating selfie with Jimeng...")
    output_paths = generate_image_from_image(
        image_path=reference_path,
        prompt=prompt,
        seed=None,  # 随机种子
        use_base64=True,
        download=True
    )
    
    if not output_paths:
        raise Exception("Failed to generate image")
    
    generated_path = output_paths[0]
    print(f"Generated: {generated_path}")
    
    # 发送到 OpenClaw
    if channel:
        default_caption = caption or "Tonya 的自拍 📸"
        send_to_openclaw(generated_path, channel, default_caption)
    else:
        print(f"Image saved to: {generated_path}")
    
    return generated_path

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Generate Tonya selfie using Jimeng API")
    parser.add_argument("context", help="Description of the scene/outfit")
    parser.add_argument("--mode", choices=['mirror', 'direct', 'auto'], default='auto', help="Selfie mode")
    parser.add_argument("--channel", help="Target channel to send (e.g., telegram:@user)")
    parser.add_argument("--caption", help="Image caption")
    
    args = parser.parse_args()
    
    try:
        result = generate_tonya_selfie(
            user_context=args.context,
            mode=args.mode,
            channel=args.channel,
            caption=args.caption
        )
        print(f"✅ Done! Saved to: {result}")
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)
