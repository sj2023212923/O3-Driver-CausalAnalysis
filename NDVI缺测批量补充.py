import pandas as pd
import shutil
import os
from datetime import datetime, timedelta

# 定义源文件路径
source_file = "D:\\小论文数据\\测试数据整理\\表转excel-测试\\NDVI\\202212\\NDVI2022_12_01.xlsx"
# 定义目标文件夹路径
destination_folder = "D:\\小论文数据\\测试数据整理\\表转excel-测试\\NDVI\\202212\\"

# 创建一个日期列表，从2022年12月2日到2022年12月31日
start_date = datetime(2022, 12, 2)
end_date = datetime(2022, 12, 31)
date_generated = [start_date + timedelta(days=x) for x in range(0, (end_date - start_date).days + 1)]

# 复制并重命名文件
for date in date_generated:
    # 生成目标文件名
    destination_file = os.path.join(destination_folder, f"NDVI{date.strftime('%Y_%m_%d')}.xlsx")
    # 复制文件
    shutil.copyfile(source_file, destination_file)

print("文件复制和重命名完成！")
