import arcpy
import os
import pandas as pd

# 设置工作空间为包含SHP文件的文件夹路径
workspace = r"D:\小论文数据\测试数据整理\栅格转点-测试\VOC"
output_folder = r"D:\小论文数据\测试数据整理\表转excel-测试\VOC"

# 创建输出文件夹（如果不存在）
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# 设置工作空间环境
arcpy.env.workspace = workspace

# 获取工作空间中的所有SHP文件
shp_files = arcpy.ListFeatureClasses()

# 遍历所有SHP文件
for shp_file in shp_files:
    # 获取SHP文件的基本信息
    desc = arcpy.Describe(shp_file)
    shp_name = os.path.splitext(desc.name)[0]

    # 创建DataFrame以保存属性表数据
    fields = [field.name for field in arcpy.ListFields(shp_file) if field.type != 'Geometry']
    data = []

    with arcpy.da.SearchCursor(shp_file, fields) as cursor:
        for row in cursor:
            data.append(row)

    df = pd.DataFrame(data, columns=fields)

    # 将DataFrame保存为Excel文件
    excel_file = os.path.join(output_folder, f"{shp_name}.xlsx")
    df.to_excel(excel_file, index=False)

    print(f"{shp_file} 已成功转换为 {excel_file}")

print("所有SHP文件已成功转换为Excel文件。")