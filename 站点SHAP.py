import arcpy
import pandas as pd
from datetime import datetime, timedelta

# 设置输入Excel文件路径
input_excel = r"D:\小论文数据\训练数据整理\point\point.xlsx"

# 列出所有工作表
excel_sheets = pd.ExcelFile(input_excel).sheet_names
print("Excel sheets:", excel_sheets)

# 假设工作表名是 'Sheet1'，请根据实际情况修改
sheet_name = "Sheet1"

# 设置输出文件夹
output_folder = r"D:\小论文数据\预测结果\站点SHAP"

# 设置坐标系
spatial_reference = arcpy.SpatialReference(4326)  # GCS_WGS_1984

# 读取Excel数据
df = pd.read_excel(input_excel, sheet_name=sheet_name)

# 批量处理每一天的数据
start_date = datetime(2022, 3, 1)
end_date = datetime(2023, 2, 28)

# 逐日生成SHAPE文件
current_date = start_date
while current_date <= end_date:
    # 生成输出文件名
    output_name = current_date.strftime("%Y%m%d") + ".shp"
    output_path = arcpy.management.CreateFeatureclass(output_folder, output_name, "POINT",
                                                      spatial_reference=spatial_reference)

    # 添加字段
    arcpy.management.AddField(output_path, "经度", "DOUBLE")
    arcpy.management.AddField(output_path, "纬度", "DOUBLE")

    # 创建插入光标
    with arcpy.da.InsertCursor(output_path, ["SHAPE@", "经度", "纬度"]) as cursor:
        for _, row in df.iterrows():
            point = arcpy.Point(row['经度'], row['纬度'])
            cursor.insertRow([point, row['经度'], row['纬度']])

    current_date += timedelta(days=1)

print("批处理完成")

