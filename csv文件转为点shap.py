import arcpy
import os

# 设置输入和输出文件夹路径
input_folder = r"D:\小论文数据\预测结果\结果csv\202302"
output_folder = r"D:\小论文数据\预测结果\栅格SHAP"

# 设置环境
arcpy.env.workspace = input_folder
arcpy.env.overwriteOutput = True

# 获取文件夹中的所有CSV文件
csv_files = [f for f in os.listdir(input_folder) if f.endswith('.csv')]

# 设置坐标系
spatial_reference = arcpy.SpatialReference(4326)  # GCS_WGS_1984

# 遍历每个CSV文件
for csv_file in csv_files:
    # 定义输入文件路径
    input_csv = os.path.join(input_folder, csv_file)

    # 定义输出文件路径
    output_shp = os.path.join(output_folder, os.path.splitext(csv_file)[0] + '.shp')

    # 设置XY字段
    x_field = "LG"
    y_field = "LT"

    # 执行XY表到点的转换
    arcpy.management.XYTableToPoint(input_csv, output_shp, x_field, y_field, "", spatial_reference)

    print(f"{csv_file} 已转换为 {output_shp}")

print("所有CSV文件转换完成")
