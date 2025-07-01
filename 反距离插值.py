import arcpy
import os

# 输入文件夹和输出文件夹路径
input_folder = r"D:\小论文数据\训练数据整理\栅格转点-type\11132\2TM\202203"
output_folder = r"D:\小论文数据\训练数据整理\反距离插值\2TM\202203"

# 掩膜文件路径和输出坐标系
mask = r"D:\小论文数据\区划图\shp\华东.shp"
output_coordinate_system = arcpy.SpatialReference(4326)  # WGS 1984

# 确保输出文件夹存在，如果不存在则创建
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# 设置环境参数
arcpy.env.mask = mask
arcpy.env.outputCoordinateSystem = output_coordinate_system
arcpy.env.extent = mask
arcpy.env.cellSize = 0.05
arcpy.env.workspace = output_folder  # 设置工作空间为输出文件夹

# 遍历输入文件夹下的所有点文件
for filename in os.listdir(input_folder):
    if filename.endswith('.shp'):  # 假设输入数据为shapefile
        input_path = os.path.join(input_folder, filename)

        # 设置输出文件路径
        output_filename = os.path.splitext(filename)[0] + "_IDW.tif"
        output_path = os.path.join(output_folder, output_filename)

        # 反距离插值参数设置
        power = 2  # 根据需要设置

        # 执行反距离插值
        arcpy.sa.Idw(input_path, "grid_code", arcpy.env.cellSize, power).save(output_path)

print("反距离插值操作完成")
