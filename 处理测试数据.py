import pandas as pd
import numpy as np

# 读取CSV文件
file_path = r"D:\小论文数据\测试数据整理\csv\202205\20220531.csv"  # 替换为你的CSV文件路径
data_pre = pd.read_csv(file_path)

# 替换无穷大值为NaN
data_pre = data_pre.replace([np.inf, -np.inf], np.nan)

# 检查并处理NaN值
if data_pre.isnull().sum().sum() > 0:
    print("Data contains NaN values. Handling NaNs...")
    data_pre = data_pre.dropna()  # 或者使用其他填补策略，例如 data_pre.fillna(0)

# 检查是否有超过 float32 范围的值
if (data_pre > np.finfo(np.float32).max).sum().sum() > 0 or (data_pre < np.finfo(np.float32).min).sum().sum() > 0:
    print("Data contains values out of float32 range. Handling such values...")
    data_pre = data_pre[(data_pre < np.finfo(np.float32).max) & (data_pre > np.finfo(np.float32).min)]

# 确保数据类型
data_pre = data_pre.astype(np.float32)

# 保存处理后的数据到新的CSV文件
processed_data_path = r"D:\小论文数据\预测结果\结果csv\202205-1\20220531.csv"  # 替换为你希望保存处理后数据的路径
data_pre.to_csv(processed_data_path, index=False)

print(f"Processed data saved to: {processed_data_path}")

