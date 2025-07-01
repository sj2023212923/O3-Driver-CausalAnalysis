library(ggplot2)
library(cowplot)
library(showtext)
library(readr)

showtext_auto()
font_add("Times", "times.ttf")

# === 数据读取 ===
df_all <- read_csv("D:/lunwen2/variants_final.csv")

# 变量列表（共12个）
vars <- c("2TM", "UW", "NDVI", "VW", "NT", "TP", "RH", "Tor_O3",
          "DATE", "TE", "TC", "BH")

# 初始化图列表
plot_list <- list()

# === 逐变量生成图 ===
for (v in vars) {
  df <- data.frame(
    ATE_CF = df_all[[paste0(v, "_ATE_CF")]],
    ATE_DML = df_all[[paste0(v, "_ATE_DML")]]
  )
  
  model <- lm(ATE_DML ~ ATE_CF, data = df)
  df$resid <- residuals(model)
  eq <- paste0("y = ", round(coef(model)[2], 2), "x + ", round(coef(model)[1], 2))
  
  # 主图
  p_main <- ggplot(df, aes(x = ATE_CF, y = ATE_DML)) +
    geom_point(color = "#1B4F72", alpha = 0.8, size = 1.8) +
    geom_abline(slope = 1, intercept = 0, linetype = "dashed", color = "gray40", linewidth = 0.8) +
    geom_smooth(method = "lm", color = "#B2182B", fill = "#FDBBA4",
                se = TRUE, alpha = 0.5, linewidth = 1.4) +
    annotate("text", x = min(df$ATE_CF, na.rm = TRUE),
             y = max(df$ATE_DML, na.rm = TRUE),
             label = eq, hjust = 0, vjust = 1, size = 4.2, family = "Times") +
    labs(title = v) +
    theme_minimal(base_family = "Times") +
    theme(
      plot.title = element_text(hjust = 0.5, size = 13, face = "bold"),
      axis.title = element_blank(),   # 每张图去除 x/y 轴标题
      axis.text = element_text(size = 9),
      panel.border = element_rect(color = "black", fill = NA, linewidth = 0.5)
    )
  
  p_resid <- ggplot(df, aes(x = resid)) +
    geom_histogram(fill = "#F0B600", color = "black", bins = 20, alpha = 0.75) +
    ggtitle("Residuals") +
    theme_minimal(base_family = "Times") +
    theme(
      plot.title = element_text(size = 7.5, hjust = 0.5),  # ✅ 显示标题、居中、小字号
      axis.title = element_blank(),
      axis.text = element_text(size = 6),
      plot.margin = margin(2, 2, 2, 2)
    )
  

  
  # 合图（残差图位置上移）
  p_combo <- ggdraw() +
    draw_plot(p_main) +
    draw_plot(p_resid, x = 0.6, y = 0.08, width = 0.34, height = 0.3)
  
  plot_list[[v]] <- p_combo
}

# === 拼图 & 添加统一横纵坐标 ===
final_panel <- plot_grid(plotlist = plot_list, ncol = 4)

final_labeled <- ggdraw() +
  draw_plot(final_panel) 

# === 展示图像 ===
print(final_labeled)

# === 可选保存 ===
ggsave("D:/lunwen2/pictures/final_labeled_with_diagonal2.pdf", plot = final_labeled, width = 16, height = 10)


