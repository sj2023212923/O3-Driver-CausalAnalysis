# ==== 1. 加载必要包 ====
library(GGally)
library(ggplot2)
library(scales)

# ==== 2. 读取数据 ====
d1 <- read.csv("D:/lunwen/xiangguanxing.csv")

# ==== 3. 筛选用于分析的连续变量列（排除经纬度、日期等）====
# 你可以根据需要保留或排除部分变量
d1 <- d1[, c("Tm2", "NDVI", "UW", "VW", "BH", "Tor_O3", "NT", "RH", "TP", 
             "TC", "TE", "CO", "NOx", "PM25", "VOC", "MPD", "DEM", "O3")]

# ==== 4. 计算相关性矩阵 ====
corr_matrix <- cor(d1)

# ==== 5. 自定义下三角拟合图 ====
custom_smooth <- function(data, mapping, ...) {
  ggplot(data = data, mapping = mapping) +
    geom_smooth(method = "lm", color = "#5cb3ba", alpha = 0.4, size = 1, ...) +
    geom_point(color = "#ff5e00", alpha = 0.6) +
    theme_minimal()
}

# ==== 6. 绘制初始图（下三角 + 对角线） ====
ggpairs_plot <- ggpairs(
  d1,
  upper = "blank",  # 上三角留空
  lower = list(continuous = wrap(custom_smooth)),  # 下三角拟合图
  diag = list(continuous = wrap("densityDiag", alpha = 0.5, fill = "#5cb3ba"))  # 对角密度
)

# ==== 7. 定义颜色映射函数（蓝 - 白 - 红）====
color_mapping <- function(value) {
  scales::col_numeric(
    palette = c("#5cb3ba", "white", "#ff5e00"),
    domain = c(-1, 1)
  )(value)
}

# ==== 8. 替换上三角为相关系数矩形 ====
for (i in seq_along(d1)) {
  for (j in seq_along(d1)) {
    if (i < j) {
      corr_value <- corr_matrix[i, j]
      corr_color <- color_mapping(corr_value)
      corr_size <- abs(corr_value) * 30
      
      rect_cell <- ggplot() +
        geom_point(aes(x = 0.5, y = 0.5), shape = 22, size = corr_size,
                   fill = corr_color, colour = "black", alpha = 0.8) +
        annotate("text", x = 0.5, y = 0.5, label = sprintf("%.2f", corr_value),
                 size = 4, color = "black") +
        theme_void() +
        theme(aspect.ratio = 1)
      
      ggpairs_plot[i, j] <- rect_cell
    }
  }
}

# ==== 9. 显示图像 ====
print(ggpairs_plot)  # 打开视图窗口显示图像
message("✅ 图像已在视图窗口中显示，请确认是否满意。")

# ==== 10. 暂停并等待用户操作（可选）====
# readline("按回车继续并保存图片...")  # 取消注释可加入人工确认步骤

# ==== 11. 保存为 PDF ====
ggsave("ggpairs_plot.pdf", plot = ggpairs_plot, dpi = 1200, height = 10, width = 12)
message("✅ 图像已成功保存为 ggpairs_plot.pdf")
