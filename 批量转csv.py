import os
import pandas as pd

# 定义输入文件夹和输出文件夹路径
input_folder = r"D:\小论文数据\测试数据整理\测试"
output_folder = r"D:\小论文数据\测试数据整理\CSV2"

# 创建输出文件夹如果不存在
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# 遍历输入文件夹中的所有Excel文件
for filename in os.listdir(input_folder):
    if filename.endswith(".xlsx") or filename.endswith(".xls"):
        # 生成完整的文件路径
        file_path = os.path.join(input_folder, filename)
        # 读取Excel文件
        df = pd.read_excel(file_path)
        # 生成输出CSV文件路径
        output_file_path = os.path.join(output_folder, os.path.splitext(filename)[0] + ".csv")
        # 保存为CSV文件
        df.to_csv(output_file_path, index=False, encoding='utf-8')

print("Excel文件已成功转换为CSV格式！")
