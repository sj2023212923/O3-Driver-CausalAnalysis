import os
import glob

# 指定根目录
root_dir = r"D:\小论文数据\测试数据整理\表转excel-测试\总云量"

# 遍历根目录下的所有子文件夹
for subdir in os.listdir(root_dir):
    subdir_path = os.path.join(root_dir, subdir)
    if os.path.isdir(subdir_path):
        # 查找子文件夹中的所有Excel文件
        excel_files = glob.glob(os.path.join(subdir_path, "*.xlsx"))

        for excel_file in excel_files:
            # 获取文件名和扩展名
            file_path, file_name = os.path.split(excel_file)
            new_file_name = f"TC{file_name}"
            new_file_path = os.path.join(file_path, new_file_name)

            # 重命名文件
            os.rename(excel_file, new_file_path)
            print(f"Renamed: {excel_file} to {new_file_path}")
