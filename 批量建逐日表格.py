import os
import pandas as pd
from datetime import datetime, timedelta

# 指定目标文件夹
target_folder = r"D:\小论文数据\测试数据整理\逐日数据"

# 确保目标文件夹存在，如果不存在则创建
if not os.path.exists(target_folder):
    os.makedirs(target_folder)

# 开始日期和结束日期
start_date = datetime(2022, 12, 1)
end_date = datetime(2023, 2, 28)

# 当前处理的日期
current_date = start_date

# 创建日期范围内的Excel文件
while current_date <= end_date:
    # 生成文件名，格式为"YYYYMMDD.xlsx"
    file_name = current_date.strftime("%Y%m%d") + ".xlsx"
    file_path = os.path.join(target_folder, file_name)

    # 创建一个空的DataFrame
    df = pd.DataFrame()

    # 保存为Excel文件
    df.to_excel(file_path, index=False)

    print(f"Created: {file_path}")

    # 增加一天
    current_date += timedelta(days=1)
