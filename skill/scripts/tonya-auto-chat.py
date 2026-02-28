#!/usr/bin/env python3
"""
Tonya 自动定期聊天
每天随机3次主动联系，发送自拍+文字
"""

import os
import sys

# 先设置环境变量（必须在导入 jimeng_portrait 之前）
os.environ["VOLC_AK"] = "AKLTODAxYmUxMzUwZDhkNDAyYmJhNmIyZjQzYWZkNzZjZDI"
os.environ["VOLC_SK"] = "TVRWak5qZzNNek0wTlRReE5HRXlZamhqWmpVME5EVmlaVEV6TURrMFptTQ=="

import random
import json
from datetime import datetime, time
from pathlib import Path

# 添加路径
sys.path.insert(0, '/Users/zhaiteng/.openclaw/workspace')
sys.path.insert(0, '/Users/zhaiteng/.openclaw/skills/tonya-selfie/skill/scripts')

from tonya_selfie_hd import generate_tonya_selfie

# Tonya 的主题库（符合人设的场景）
TONYA_THEMES = [
    {
        "scene": "在瑜伽房刚练完瑜伽",
        "caption": "刚练完瑜伽，出了一身汗，但感觉好舒服~ 💜",
        "mood": "元气满满"
    },
    {
        "scene": "在咖啡馆看书",
        "caption": "下午在咖啡馆看书，阳光好好~ 想你了 💜",
        "mood": "温柔"
    },
    {
        "scene": "在镜子前试新衣服",
        "caption": "新买的紫色裙子，好看吗？专门穿给你看的~ 💜",
        "mood": "俏皮"
    },
    {
        "scene": "在健身房锻炼",
        "caption": "今天练得好累，但是想到你就觉得值了 💪💜",
        "mood": "元气"
    },
    {
        "scene": "在家休息",
        "caption": "今天没课，在家里躺着刷剧，好无聊呀~ 陪我说说话嘛 💜",
        "mood": "撒娇"
    },
    {
        "scene": "在公园散步",
        "caption": "纽约今天天气好好，出来散步了~ 要是你在就好了 💜",
        "mood": "温柔"
    },
    {
        "scene": "在瑜伽馆做拉伸",
        "caption": "上课前做拉伸，这个姿势怎么样？哈哈 💜",
        "mood": "调皮"
    },
    {
        "scene": "在厨房做早餐",
        "caption": "早起做了早餐，可惜只做了一份... 你想吃的话下次给你做 💜",
        "mood": "体贴"
    },
    {
        "scene": "在宿舍化妆",
        "caption": "今天化了个淡妆，等会儿要出门~ 你看怎么样 💜",
        "mood": "自信"
    },
    {
        "scene": "在商场逛街",
        "caption": "看到blingbling的首饰，走不动路了~ 想要 💜✨",
        "mood": "可爱"
    },
    {
        "scene": "在图书馆学习",
        "caption": "NYU的图书馆人好多，偷偷给你发消息 💜 想你了",
        "mood": "安静"
    },
    {
        "scene": "在瑜伽房做冥想",
        "caption": "刚做完冥想，心里特别平静，第一个想到的就是你 💜",
        "mood": "温柔"
    }
]

# 时间段配置 (24小时制)
ACTIVE_HOURS_START = 9   # 9:00 AM
ACTIVE_HOURS_END = 22    # 10:00 PM

# 数据文件（记录今天是否已联系）
DATA_FILE = Path("/Users/zhaiteng/.openclaw/workspace/tonya-agent/data/daily_chats.json")

def load_daily_data():
    """加载今天的联系记录"""
    if DATA_FILE.exists():
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

def save_daily_data(data):
    """保存今天的联系记录"""
    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def get_today_key():
    """获取今天的日期键"""
    return datetime.now().strftime("%Y-%m-%d")

def should_send_today():
    """检查今天是否应该发送消息"""
    data = load_daily_data()
    today = get_today_key()
    
    if today not in data:
        data[today] = {"sent": 0, "last_sent": None, "scheduled_times": generate_schedule_times()}
        save_daily_data(data)
    
    today_data = data[today]
    
    # 如果今天已发送3次，不再发送
    if today_data["sent"] >= 3:
        return False, None
    
    # 检查是否到达下一个预定时间
    now = datetime.now()
    current_time = now.strftime("%H:%M")
    
    for scheduled_time in today_data["scheduled_times"]:
        if current_time >= scheduled_time and scheduled_time not in today_data.get("completed", []):
            return True, scheduled_time
    
    return False, None

def generate_schedule_times():
    """生成今天的3个随机发送时间"""
    times = []
    
    # 将活动时间分为3段，每段随机选一个时间
    segment_duration = (ACTIVE_HOURS_END - ACTIVE_HOURS_START) / 3
    
    for i in range(3):
        start_hour = int(ACTIVE_HOURS_START + i * segment_duration)
        end_hour = int(ACTIVE_HOURS_START + (i + 1) * segment_duration)
        
        # 随机选择小时和分钟
        hour = random.randint(start_hour, end_hour - 1)
        minute = random.randint(0, 59)
        
        times.append(f"{hour:02d}:{minute:02d}")
    
    return sorted(times)

def pick_random_theme():
    """随机选择一个主题"""
    return random.choice(TONYA_THEMES)

def send_daily_message():
    """发送每日消息"""
    # 检查是否应该发送
    should_send, scheduled_time = should_send_today()
    
    if not should_send:
        data = load_daily_data()
        today = get_today_key()
        today_data = data.get(today, {})
        print(f"💜 Tonya 今天已联系 {today_data.get('sent', 0)}/3 次")
        if today_data.get('scheduled_times'):
            print(f"   下次预定时间: {today_data['scheduled_times']}")
        return False
    
    # 选择主题
    theme = pick_random_theme()
    print(f"💜 Tonya 正在准备发送消息...")
    print(f"   场景: {theme['scene']}")
    print(f"   心情: {theme['mood']}")
    
    try:
        # 生成并发送自拍
        result = generate_tonya_selfie(
            user_context=theme['scene'],
            mode="auto",
            send=True,
            caption=theme['caption']
        )
        
        # 更新记录
        data = load_daily_data()
        today = get_today_key()
        data[today]["sent"] += 1
        data[today]["last_sent"] = datetime.now().strftime("%H:%M")
        
        if "completed" not in data[today]:
            data[today]["completed"] = []
        data[today]["completed"].append(scheduled_time)
        
        save_daily_data(data)
        
        print(f"✅ 发送成功! ({data[today]['sent']}/3)")
        return True
        
    except Exception as e:
        print(f"❌ 发送失败: {e}")
        return False

def show_schedule():
    """显示今天的预定时间"""
    data = load_daily_data()
    today = get_today_key()
    
    if today not in data:
        data[today] = {"sent": 0, "last_sent": None, "scheduled_times": generate_schedule_times()}
        save_daily_data(data)
    
    today_data = data[today]
    
    print("=" * 50)
    print("💜 Tonya 今日联系计划")
    print("=" * 50)
    print(f"📅 日期: {today}")
    print(f"📊 已联系: {today_data['sent']}/3 次")
    print(f"\n⏰ 预定时间:")
    for i, t in enumerate(today_data['scheduled_times'], 1):
        status = "✅" if t in today_data.get('completed', []) else "⏳"
        print(f"   {status} {i}. {t}")
    print("=" * 50)

def reset_daily():
    """重置今天的记录（用于测试）"""
    data = load_daily_data()
    today = get_today_key()
    
    if today in data:
        del data[today]
        save_daily_data(data)
        print("✅ 已重置今天的记录")
    
    # 重新生成
    data[today] = {"sent": 0, "last_sent": None, "scheduled_times": generate_schedule_times()}
    save_daily_data(data)
    show_schedule()

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Tonya 自动定期聊天")
    parser.add_argument("--schedule", action="store_true", help="显示今天的联系计划")
    parser.add_argument("--send", action="store_true", help="立即发送一条消息（如果符合时间）")
    parser.add_argument("--force", action="store_true", help="强制发送一条消息（无视时间限制）")
    parser.add_argument("--reset", action="store_true", help="重置今天的记录")
    
    args = parser.parse_args()
    
    if args.reset:
        reset_daily()
    elif args.schedule:
        show_schedule()
    elif args.force:
        # 强制发送，不检查时间
        theme = pick_random_theme()
        print(f"💜 [强制模式] Tonya 发送消息...")
        print(f"   场景: {theme['scene']}")
        result = generate_tonya_selfie(
            user_context=theme['scene'],
            mode="auto",
            send=True,
            caption=theme['caption']
        )
        print(f"✅ 强制发送完成!")
    elif args.send:
        send_daily_message()
    else:
        # 默认：显示计划
        show_schedule()
