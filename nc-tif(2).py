import os
import numpy as np
import xarray as xr
from osgeo import gdal, osr

# 定义输入和输出路径
nc_path = r"D:\Download\date\2023-03\2023-03.nc"
output_path = r"D:\Download\date\变量\tif数据\10mV\2023"

# 读取 NetCDF 文件
data = xr.open_dataset(nc_path, engine="netcdf4")

# 打印数据结构确认变量
print(data)

# 获取坐标与分辨率
lat = data["latitude"].values
lon = data["longitude"].values
resolution = abs(lon[1] - lon[0])

# 创建输出文件夹（如果不存在）
os.makedirs(output_path, exist_ok=True)

# 遍历每个时间片，将 ssrd 输出为 GeoTIFF
for i in range(len(data.valid_time)):
    # 提取当前时间片数据（二维）
    dpt = data["v10"].isel(valid_time=i).values

    # 获取当前时间
    current_time = data.valid_time.values[i]
    date_str = np.datetime_as_string(current_time, unit='D')   # '2023-01-01'
    hour_str = np.datetime_as_string(current_time, unit='h')[-2:]  # '00', '01', ...

    # 创建对应日期的子文件夹
    daily_folder = os.path.join(output_path, date_str)
    os.makedirs(daily_folder, exist_ok=True)

    # 拼接输出文件路径
    tiff_path = os.path.join(daily_folder, f"hour_{hour_str}.tif")

    # 创建 GeoTIFF 文件
    driver = gdal.GetDriverByName("GTiff")
    ds = driver.Create(tiff_path, len(lon), len(lat), 1, gdal.GDT_Float32)

    # 设置空间参考（仿射变换：左上角经度、分辨率、旋转、左上角纬度、旋转、负的纬度分辨率）
    ds.SetGeoTransform((np.min(lon), resolution, 0, np.max(lat), 0, -resolution))

    # 设置投影为 WGS84
    srs = osr.SpatialReference()
    srs.ImportFromEPSG(4326)
    ds.SetProjection(srs.ExportToWkt())

    # 写入数据
    band = ds.GetRasterBand(1)
    band.WriteArray(dpt)
    band.SetNoDataValue(-32767)
    band.ComputeStatistics(False)

    # 创建金字塔以加快加载
    ds.BuildOverviews("NEAREST", [1])
    ds.FlushCache()
    ds = None  # 完成写入，关闭文件

print("✅ 所有 ssrd 时序数据已成功转换为 TIFF 文件。")
