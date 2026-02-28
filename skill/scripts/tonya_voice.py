#!/usr/bin/env python3
"""
Tonya TTS - 使用 FishAudio 生成 Tonya 的语音

默认使用 Tonya 的声音模型 (ID: 4d044bba21e34fad821cf856e8e24cba)
"""

import os
import sys
import argparse
import subprocess

# 添加 workspace 到路径
sys.path.insert(0, '/Users/zhaiteng/.openclaw/workspace')

from fish_audio_tool import tts, quick_tts

# Tonya 默认声音模型 ID
TONYA_VOICE_ID = "4d044bba21e34fad821cf856e8e24cba"

def generate_tonya_voice(text: str, output_path: str = None, send_to_channel: str = None):
    """
    生成 Tonya 的语音
    
    Args:
        text: 要合成的文本
        output_path: 输出路径 (默认保存到 AI 文件夹)
        send_to_channel: 如果提供，发送到指定频道
    
    Returns:
        生成的音频文件路径
    """
    if output_path is None:
        import time
        timestamp = int(time.time())
        output_path = f"/Volumes/ExSSD/AI/tonya_voice_{timestamp}.mp3"
    
    print(f"Generating Tonya's voice for: \"{text[:50]}...\"")
    
    # 使用 Tonya 的声音模型
    result_path = tts(text, output_path, reference_id=TONYA_VOICE_ID)
    
    print(f"Voice saved to: {result_path}")
    
    # 发送到消息平台
    if send_to_channel:
        cmd = [
            'openclaw', 'message', 'send',
            '--action', 'send',
            '--channel', send_to_channel,
            '--media', result_path
        ]
        print(f"Sending voice to {send_to_channel}...")
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"✅ Voice sent successfully!")
        else:
            print(f"❌ Failed to send: {result.stderr}")
    
    return result_path

def generate_with_caption(text: str, image_path: str = None, channel: str = None):
    """
    为自拍生成配套语音
    
    例如：图片发一张瑜伽房自拍，语音配一段"刚练完瑜伽，好累但好开心~"
    """
    output_path = generate_tonya_voice(text, send_to_channel=channel)
    return output_path

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate Tonya's voice using FishAudio")
    parser.add_argument("text", help="Text to synthesize")
    parser.add_argument("--output", "-o", help="Output file path")
    parser.add_argument("--channel", "-c", help="Send to channel (e.g., telegram:@user)")
    
    args = parser.parse_args()
    
    try:
        result = generate_tonya_voice(
            text=args.text,
            output_path=args.output,
            send_to_channel=args.channel
        )
        print(f"✅ Done! Saved to: {result}")
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)
