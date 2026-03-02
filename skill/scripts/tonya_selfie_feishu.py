#!/usr/bin/env python3
"""
Tonya Selfie Generator v1.1 - 飞书版
使用即梦AI图片生成4.0 API (jimeng_t2i_v40)
支持飞书 Bot 发送

更新日期: 2026-03-02
"""

import os
import sys
import shutil
import subprocess
import time

sys.path.insert(0, '/Users/zhaiteng/.openclaw/workspace')
from jimeng_image import generate_image

# Tonya 参考图路径 (本地)
TONYA_REFERENCE_PATH = "/Volumes/ExSSD/AI/Tonya/tonya-smile.jpg"

def generate_and_send_to_feishu(scene_description: str, caption: str = "Tonya 的自拍 💜"):
    """
    生成 Tonya 自拍并发送到飞书
    
    Args:
        scene_description: 场景描述，如 "在海边散步"、"穿紫色瑜伽服"
        caption: 图片说明文字
    
    Returns:
        生成的图片路径
    """
    # 检查参考图
    if not os.path.exists(TONYA_REFERENCE_PATH):
        raise Exception(f"参考图不存在: {TONYA_REFERENCE_PATH}")
    
    print(f"✅ 参考图: {TONYA_REFERENCE_PATH}")
    
    # 使用 v40 专用提示词模板
    prompt = f"以图片人物相貌为基准，生成她{scene_description}，只参考她的相貌，不要参考着装及背景"
    print(f"📝 提示词: {prompt}")
    
    # 使用 jimeng_t2i_v40 接口生成
    print("🎨 使用即梦AI图片生成4.0...")
    output_paths = generate_image(
        prompt=prompt,
        image_source=TONYA_REFERENCE_PATH,
        req_key="jimeng_t2i_v40",
        scale=0.5,
        width=1328,
        height=1328,
        seed=-1,
        use_base64=True,
        download=True
    )
    
    if not output_paths:
        raise Exception("图片生成失败")
    
    generated_path = output_paths[0]
    print(f"✅ 生成成功: {generated_path}")
    
    # 发送到飞书
    send_to_feishu(generated_path, caption)
    
    return generated_path

def send_to_feishu(image_path: str, caption: str = ""):
    """发送图片到飞书"""
    # 复制到临时目录
    tmp_id = f"{int(time.time())}_{os.urandom(2).hex()}"
    temp_name = f"tonya_selfie_{tmp_id}.jpg"
    temp_path = f"/Users/zhaiteng/.openclaw/workspace/.send-temp/{temp_name}"
    
    os.makedirs("/Users/zhaiteng/.openclaw/workspace/.send-temp", exist_ok=True)
    shutil.copy(image_path, temp_path)
    
    # 使用 openclaw 发送
    cmd = [
        'openclaw', 'message', 'send',
        '--channel', 'feishu',
        '--path', f"./.send-temp/{temp_name}"
    ]
    
    if caption:
        cmd.extend(['--message', caption])
    
    print(f"📤 发送到飞书...")
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode == 0:
        print(f"✅ 发送成功!")
    else:
        print(f"❌ 发送失败: {result.stderr}")
        raise Exception(f"发送失败: {result.stderr}")
    
    return True

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="生成 Tonya 自拍并发送到飞书")
    parser.add_argument("scene", help="场景描述 (如 '在海边'、'穿紫色连衣裙')")
    parser.add_argument("--caption", default="Tonya 的自拍 💜", help="图片说明")
    
    args = parser.parse_args()
    
    try:
        result = generate_and_send_to_feishu(args.scene, args.caption)
        print(f"\n✅ 完成! 图片: {result}")
    except Exception as e:
        print(f"\n❌ 错误: {e}")
        sys.exit(1)
