import arcpy
import os
import pandas as pd

# 设置输入和输出路径
excel_path = r"D:\小论文数据\训练数据整理\point\point.xls"
workspace = r"D:\小论文数据\训练数据整理\反距离插值\边界层高度\202203"
output_path = r"D:\课程\BH\202203"

# 读取Excel文件中的站点信息
df = pd.read_excel(excel_path)

# 临时保存点数据为CSV
temp_csv = os.path.join(output_path, "points.csv")
df[['监测点编码', '经度', '纬度']].to_csv(temp_csv, index=False)

# 临时保存点数据为shapefile
point_shp = os.path.join(output_path, "points.shp")

# 将CSV文件转换为点shapefile
arcpy.management.XYTableToPoint(temp_csv, point_shp, "经度", "纬度")

# 获取所有栅格文件路径
raster_list = [os.path.join(workspace, f) for f in os.listdir(workspace) if f.endswith(".tif")]

# 将栅格文件路径转换为 arcpy 的栅格对象列表
rasters = [[raster, "VALUE"] for raster in raster_list]

# 输出shapefile的路径
output_file = os.path.join(output_path, "points_MVExtract.shp")

# 执行多值提取至点
arcpy.sa.ExtractMultiValuesToPoints(point_shp, rasters, "NONE")

# 将结果保存到指定输出路径中
arcpy.CopyFeatures_management(point_shp, output_file)

print("多值提取至点操作完成。")
