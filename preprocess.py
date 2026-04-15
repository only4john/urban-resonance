"""
转换CSV为JSON供可视化使用
"""

import pandas as pd
import json

print("转换数据...")

# 读取CSV
df = pd.read_csv('noise_clusters_17classes.csv')

# 18类矿物色谱
MINERAL_COLORS = {
    "工地施工": { "r": 45, "g": 90, "b": 90 },
    "道路出行": { "r": 90, "g": 95, "b": 105 },
    "小区管理": { "r": 30, "g": 35, "b": 40 },
    "商业噪音": { "r": 155, "g": 74, "b": 74 },
    "公共设施": { "r": 90, "g": 74, "b": 106 },
    "交通噪音": { "r": 75, "g": 78, "b": 88 },
    "夜间施工": { "r": 139, "g": 58, "b": 58 },
    "设备噪音": { "r": 55, "g": 95, "b": 105 },
    "广场活动": { "r": 171, "g": 90, "b": 90 },
    "渣土车": { "r": 110, "g": 115, "b": 120 },
    "高架铁路": { "r": 74, "g": 58, "b": 90 },
    "夜间扰民": { "r": 139, "g": 107, "b": 74 },
    "底商餐饮": { "r": 123, "g": 91, "b": 58 },
    "道路施工": { "r": 35, "g": 85, "b": 75 },
    "综合噪音": { "r": 107, "g": 75, "b": 42 },
    "公园噪音": { "r": 106, "g": 90, "b": 122 },
    "垃圾问题": { "r": 139, "g": 107, "b": 74 },
    "其他": { "r": 80, "g": 80, "b": 80 }
}

# 转换为JSON格式
data = []
for _, row in df.iterrows():
    label = row['语义标签']
    color = MINERAL_COLORS.get(label, MINERAL_COLORS["其他"])
    
    # 转换时间戳（秒级）
    dt = pd.to_datetime(row['时间'])
    timestamp = int(dt.timestamp()) if pd.notna(dt) else 0
    
    data.append({
        "lon": float(row['经度']) if pd.notna(row['经度']) else 0,
        "lat": float(row['纬度']) if pd.notna(row['纬度']) else 0,
        "category_id": int(row['ClusterID']) if pd.notna(row['ClusterID']) else 0,
        "category_name": label,
        "timestamp": timestamp,
        "weight": 1.0
    })

# 保存JSON
with open('urban-resonance/noise_data.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False)

print(f"已转换 {len(data)} 条数据")
print("已保存: urban-resonance/noise_data.json")

# 生成标签配置
labels = []
for label, color in MINERAL_COLORS.items():
    rgb = f"#{color['r']:02x}{color['g']:02x}{color['b']:02x}"
    labels.append({"name": label, "color": rgb})

with open('urban-resonance/noise_labels.json', 'w', encoding='utf-8') as f:
    json.dump(labels, f, ensure_ascii=False)

print("已保存: urban-resonance/noise_labels.json")
