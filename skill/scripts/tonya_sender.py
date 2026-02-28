#!/usr/bin/env python3
"""
Tonya 多媒体发送器
支持从本地文件夹选取照片/视频，或生成新图片
"""

import os
import sys
import random
import glob
import subprocess
from pathlib import Path

# Tonya 媒体文件夹
TONYA_BASE_DIR = "/Volumes/ExSSD/AI/Tonya"
SELFIE_DIR = os.path.join(TONYA_BASE_DIR, "selfie")      # 真实自拍
GENERATE_DIR = os.path.join(TONYA_BASE_DIR, "Generate")  # AI生成
VIDEO_DIR = os.path.join(TONYA_BASE_DIR, "Video")        # 视频

# 图片和视频扩展名
IMAGE_EXTENSIONS = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp', '.heic']
VIDEO_EXTENSIONS = ['.mp4', '.mov', '.avi', '.mpg', '.mpeg', '.m4v', '.3gp']

def get_files_from_dir(directory, extensions):
    """从目录获取指定扩展名的文件"""
    files = []
    for ext in extensions:
        files.extend(glob.glob(os.path.join(directory, f"**/*{ext}"), recursive=True))
        files.extend(glob.glob(os.path.join(directory, f"**/*{ext.upper()}"), recursive=True))
    return sorted(list(set(files)))

def get_all_selfies():
    """获取所有自拍照片（真实 + AI生成）"""
    real_selfies = get_files_from_dir(SELFIE_DIR, IMAGE_EXTENSIONS)
    ai_generated = get_files_from_dir(GENERATE_DIR, IMAGE_EXTENSIONS)
    return real_selfies, ai_generated

def get_all_videos():
    """获取所有视频"""
    return get_files_from_dir(VIDEO_DIR, VIDEO_EXTENSIONS)

def search_by_keyword(files, keyword):
    """根据关键词筛选文件"""
    keyword_lower = keyword.lower()
    matches = []
    for f in files:
        filename = os.path.basename(f).lower()
        if keyword_lower in filename:
            matches.append(f)
    return matches

def get_random_selfie(source="any", keyword=None):
    """
    随机获取一张自拍照片
    
    Args:
        source: "real"(真实) | "ai"(AI生成) | "any"(任意)
        keyword: 文件名关键词筛选
    
    Returns:
        文件路径或 None
    """
    real_selfies, ai_generated = get_all_selfies()
    
    if source == "real":
        candidates = real_selfies
    elif source == "ai":
        candidates = ai_generated
    else:  # any
        # 优先真实照片，如果没有则用AI生成
        candidates = real_selfies if real_selfies else ai_generated
    
    if keyword:
        candidates = search_by_keyword(candidates, keyword)
    
    if not candidates:
        return None
    
    return random.choice(candidates)

def get_random_video(keyword=None):
    """随机获取一个视频"""
    videos = get_all_videos()
    
    if keyword:
        videos = search_by_keyword(videos, keyword)
    
    if not videos:
        return None
    
    return random.choice(videos)

def send_media_to_telegram(file_path, caption="", chat_id="8608938384"):
    """发送媒体文件到 Telegram"""
    bot_token = "8784896214:AAH3ug8O_87Bsx22ur1EMQ1846A2BCT7yhM"
    
    ext = os.path.splitext(file_path)[1].lower()
    
    if ext in VIDEO_EXTENSIONS:
        # 发送视频
        url = f"https://api.telegram.org/bot{bot_token}/sendVideo"
        cmd = [
            "curl", "-s", "-X", "POST", url,
            "-F", f"chat_id={chat_id}",
            "-F", f"video=@{file_path}"
        ]
    else:
        # 发送图片
        url = f"https://api.telegram.org/bot{bot_token}/sendPhoto"
        cmd = [
            "curl", "-s", "-X", "POST", url,
            "-F", f"chat_id={chat_id}",
            "-F", f"photo=@{file_path}"
        ]
    
    if caption:
        cmd.extend(["-F", f"caption={caption}"])
    
    print(f"Sending: {os.path.basename(file_path)}")
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode == 0 and '"ok":true' in result.stdout:
        print(f"✅ 发送成功!")
        return True
    else:
        print(f"❌ 发送失败: {result.stderr}")
        return False

def send_tonya_selfie(source="any", keyword=None, caption=None, generate_if_none=True):
    """
    发送 Tonya 自拍
    
    Args:
        source: "real" | "ai" | "any"
        keyword: 文件名关键词
        caption: 图片说明
        generate_if_none: 如果没有本地照片，是否AI生成
    """
    # 尝试获取本地照片
    selfie_path = get_random_selfie(source=source, keyword=keyword)
    
    if selfie_path:
        # 有本地照片，直接发送
        source_type = "真实自拍" if "selfie" in selfie_path else "AI生成"
        default_caption = caption or f"给你看看我的{source_type} 💜"
        return send_media_to_telegram(selfie_path, default_caption)
    
    # 没有本地照片，尝试生成
    if generate_if_none:
        print("没有找到本地照片，尝试生成...")
        sys.path.insert(0, '/Users/zhaiteng/.openclaw/workspace')
        sys.path.insert(0, '/Users/zhaiteng/.openclaw/skills/tonya-selfie/skill/scripts')
        
        from tonya_selfie import generate_tonya_selfie
        
        prompt = keyword or "日常自拍"
        result = generate_tonya_selfie(
            user_context=prompt,
            mode="auto",
            channel=None,  # 不通过 OpenClaw，我们自己发送
            caption=caption
        )
        
        if result and isinstance(result, list):
            return send_media_to_telegram(result[0], caption or "刚生成的自拍 💜")
    
    print("❌ 无法获取或生成照片")
    return False

def send_tonya_video(keyword=None, caption=None):
    """发送 Tonya 视频"""
    video_path = get_random_video(keyword=keyword)
    
    if not video_path:
        print("❌ 没有找到视频")
        return False
    
    default_caption = caption or "给你看看我的视频 💜"
    return send_media_to_telegram(video_path, default_caption)

def show_stats():
    """显示媒体库统计"""
    real_selfies, ai_generated = get_all_selfies()
    videos = get_all_videos()
    
    print("=" * 50)
    print("💜 Tonya 媒体库统计")
    print("=" * 50)
    print(f"📸 真实自拍: {len(real_selfies)} 张")
    print(f"🎨 AI生成:   {len(ai_generated)} 张")
    print(f"🎬 视频:     {len(videos)} 个")
    print("=" * 50)

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Tonya 多媒体发送器")
    parser.add_argument("--type", choices=['selfie', 'video', 'stats'], default='selfie',
                       help="发送类型")
    parser.add_argument("--source", choices=['real', 'ai', 'any'], default='any',
                       help="照片来源 (真实/AI/任意)")
    parser.add_argument("--keyword", help="文件名关键词筛选")
    parser.add_argument("--caption", help="图片/视频说明")
    parser.add_argument("--no-generate", action='store_true',
                       help="无本地照片时不生成")
    
    args = parser.parse_args()
    
    if args.type == 'stats':
        show_stats()
    elif args.type == 'video':
        send_tonya_video(keyword=args.keyword, caption=args.caption)
    else:  # selfie
        send_tonya_selfie(
            source=args.source,
            keyword=args.keyword,
            caption=args.caption,
            generate_if_none=not args.no_generate
        )
