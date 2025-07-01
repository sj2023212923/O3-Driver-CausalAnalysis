library(ggplot2)
library(sf)
library(dplyr)
library(gridExtra)

# 读取华东地区的shapefile
huadong <- st_read("F:/sj/pictures/shp/华东.shp")

# 读取数据
data <- read.csv("D:/lunwen2/ATE_space.csv")

# 将数据转换为空间数据框
points <- st_as_sf(data, coords = c("LG", "LT"), crs = 4326)
points <- st_transform(points, st_crs(huadong))  # 确保点数据与地图坐标系统一致

# 定义变量列表
variables <- c("TM", "UW", "NDVI", "VW", "NT", "TP", "RH", "Tor_O3", "DATE", "TE", "TC", "BH")

# 创建地图绘制函数
plot_maps <- function(var) {
  p <- ggplot() +
    geom_sf(data = huadong, fill = "white", color = "black") +
    geom_sf(data = points, aes(color = get(var)), size = 1) +
    scale_color_viridis_c(option = "C", end = 0.9, name = "ATE") +
    labs(title = var) +
    theme_minimal() +
    theme(plot.title = element_text(hjust = 0.5), legend.position = "bottom") +
    guides(color = guide_colourbar(barwidth = 6, barheight = 0.5))
  
  # 根据变量添加坐标轴标签控制
  if (var == "DATE") {
    # 对于 DATE 变量，不应用任何隐藏标签的设置
    # 保持原样，不修改
  } else if (var %in% c("TE", "TC", "BH")) {
    p <- p + theme(axis.text.y = element_blank())  # 只显示经度
  } else if (var %in% c("TM", "NT")) {
    p <- p + theme(axis.text.x = element_blank())  # 只显示纬度
  } else {
    p <- p + theme(axis.text.x = element_blank(), axis.text.y = element_blank())  # 不显示标签
  }
  
  return(p)
}

# 绘制所有地图
plots <- lapply(variables, plot_maps)

# 组合所有地图为4列3行并显示
combined_plot <- grid.arrange(grobs = plots, ncol = 4)

