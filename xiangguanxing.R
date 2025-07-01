library(ggplot2)
library(ggExtra)
library(cowplot)
library(showtext)

showtext_auto()
font_add("Times", "times.ttf")

# 数据 & 模型
df <- TE_merge
model <- lm(TE_ATE_CF ~ TE_ATE_DML, data = df)
df$resid <- residuals(model)
df$yhat <- predict(model)
df$group <- ifelse(abs(df$resid) > 1, "Significant", "Not significant")

# R 与 p 值
r_val <- cor(df$TE_ATE_CF, df$TE_ATE_DML)
pval <- summary(model)$coefficients[2,4]
eq <- paste0("y = ", round(coef(model)[2], 3), "x + ", round(coef(model)[1], 3),
             "\nR = ", round(r_val, 3), ", p = ", format.pval(pval, digits = 3))

# ==== 主图 ====
p <- ggplot(df, aes(x = TE_ATE_CF, y = TE_ATE_DML)) +
  geom_point(aes(color = group), alpha = 0.8, size = 2.2) +
  geom_smooth(method = "lm",
              color = "#D73027", fill = "#FEE090",
              se = TRUE, alpha = 0.4, linewidth = 1.5) +
  annotate("text",
           x = min(df$TE_ATE_CF) + 0.08,
           y = max(df$TE_ATE_DML) + 0.95,
           label = eq,
           hjust = 0, vjust = 1,
           size = 5.4,
           family = "Times") +
  scale_color_manual(values = c("Significant" = "#D55E00", "Not significant" = "#0072B2")) +
  scale_x_continuous(breaks = seq(-0.2, 1.2, 0.2)) +  # ✅ 更密集刻度
  scale_y_continuous(breaks = seq(-2, 5, 1)) +
  labs(x = "TE_ATE_CF", y = "TE_ATE_DML", color = "Residual Group") +
  theme_minimal(base_family = "Times") +
  theme(
    legend.position = "top",
    panel.border = element_rect(color = "black", fill = NA, linewidth = 0.8),
    plot.margin = margin(12, 12, 12, 12),
    axis.title = element_text(size = 15),  # ✅ 更大XY轴标题
    axis.text = element_text(size = 13)    # ✅ 更大刻度字体
  ) +
  coord_cartesian(xlim = c(-0.3, 1.3), ylim = c(-2, 5))

# ==== 边缘直方图 ====
p_marginal <- ggMarginal(
  p,
  type = "histogram",
  bins = 30,
  margins = "both",
  xparams = list(fill = "#E69F00", alpha = 0.4, color = "#E69F00"),
  yparams = list(fill = "#56B4E9", alpha = 0.4, color = "#56B4E9")
)

# ==== 残差直方图 ====
resid_hist <- ggplot(df, aes(x = resid)) +
  geom_histogram(fill = "#E69F00", color = "black", bins = 30, alpha = 0.6) +
  labs(title = "Residual Histogram", x = NULL, y = "Count") +
  theme_minimal(base_family = "Times") +
  theme(
    plot.title = element_text(size = 11, face = "bold", hjust = 0.5),
    axis.title = element_text(size = 13),
    axis.text = element_text(size = 11)
  )

# ==== 合图 ====
final_plot <- ggdraw() +
  draw_plot(p_marginal) +
  draw_plot(resid_hist, x = 0.53, y = 0.065, width = 0.3, height = 0.28)

# 展示
print(final_plot)

ggsave("D:/lunwen2/Date/ot_output.pdf", plot = final_plot, width = 8, height = 6)
