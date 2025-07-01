import arcpy
import os
import sys

# 需要输入的参数
workspace = arcpy.GetParameterAsText(0)
shp_file = arcpy.GetParameterAsText(1)
output_folder = arcpy.GetParameterAsText(2)

try:
    # 设置工作空间
    arcpy.env.workspace = workspace

    # 检查并创建输出文件夹（如果不存在）
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # 列出所有 TIF 栅格文件
    tif_files = arcpy.ListRasters("*", "TIF")

    if not tif_files:
        arcpy.AddError("没有找到TIF文件。")
        sys.exit(1)

    for raster_path in tif_files:
        try:
            filename = os.path.splitext(os.path.basename(raster_path))[0]
            out_raster_path = os.path.join(output_folder, "{}.tif".format(filename))
            arcpy.Clip_management(raster_path, "#", out_raster_path, shp_file, "255",
                                  "ClippingGeometry")  # 255为将背景值或者Nodata设为透明
        except arcpy.ExecuteError as e:
            arcpy.AddError("裁剪栅格数据'{0}'时发生错误: {1}".format(raster_path, e))
        except Exception as e:
            arcpy.AddError("处理栅格数据'{0}'时发生未知错误: {1}".format(raster_path, e))
except Exception as e:
    arcpy.AddError("初始化或执行过程中发生错误: {0}".format(e))
    sys.exit(1)
