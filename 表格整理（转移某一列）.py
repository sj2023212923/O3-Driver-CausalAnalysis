import pandas as pd

# 源文件路径
source_file = r"D:\Download\表转excel\臭氧\202302.xlsx"
# 目标文件路径
target_file = r"D:\站点实测\实测\202302-1.xlsx"

# 读取源文件中的数据，跳过列名，直接从第一行开始读取
source_df = pd.read_excel(source_file, header=None)

# 读取目标文件
target_df = pd.read_excel(target_file)

# 确保目标 DataFrame 至少具有和 source_df 相同数量的行数
if len(target_df) < len(source_df):
    # 添加足够的空行使目标 DataFrame 的行数和 source_df 相同
    extra_rows = len(source_df) - len(target_df)
    target_df = target_df.append(pd.DataFrame(index=range(extra_rows), columns=target_df.columns))

# 直接将源数据复制到目标文件的第三列，从第一行开始
target_df.loc[:len(source_df)-1, 'ColumnP'] = source_df.iloc[:, 1].values  # 选择第二列数据

# 保存修改后的目标文件
target_df.to_excel(target_file, index=False)

print("数据已经成功粘贴到目标文件的第三列，从第二行开始。")












