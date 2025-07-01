# ==== 加载必要包 ====
library(ranger)
library(dplyr)
library(ggplot2)
library(reshape2)

# ==== 读取数据 ====
df <- read.csv("D:/lunwen2/xunlian2.csv")  # ← 修改为你的实际路径
df <- df %>%
  select(O3, TM, NDVI, NT, TE, Tor_O3, TP, TC, BH) %>%
  na.omit()

# ==== Extra Trees 模型训练 ====
set.seed(123)
et_model <- ranger(O3 ~ ., data = df, num.trees = 500, splitrule = "extratrees")

# ==== 自定义 PDP + ICE + CI 函数 ====
get_pdp_ice <- function(model, data, varname, grid_size = 20) {
  grid_vals <- seq(min(data[[varname]], na.rm = TRUE), max(data[[varname]], na.rm = TRUE), length.out = grid_size)
  ice_list <- lapply(grid_vals, function(val) {
    newdata <- data
    newdata[[varname]] <- val
    preds <- predict(model, data = newdata)$predictions
    return(preds)
  })
  ice_df <- do.call(cbind, ice_list)
  colnames(ice_df) <- grid_vals
  ice_long <- reshape2::melt(ice_df)
  colnames(ice_long) <- c("id", "x", "y")
  
  pdp_summary <- ice_long %>%
    group_by(x) %>%
    summarise(
      ymean = mean(y),
      ymin = quantile(y, 0.025),
      ymax = quantile(y, 0.975)
    )
  
  list(ice = ice_long, pdp = pdp_summary)
}

# ==== 计算 TM 的 PDP + ICE ====
result <- get_pdp_ice(et_model, df, "TM")

# ==== 绘图，赋值给变量 ====
pdp_ice_plot <- ggplot() +
  geom_line(data = result$ice, aes(x = x, y = y, group = id), alpha = 0.2, color = "grey") +
  geom_ribbon(data = result$pdp, aes(x = x, ymin = ymin, ymax = ymax), alpha = 0.3, fill = "blue") +
  geom_line(data = result$pdp, aes(x = x, y = ymean), size = 1.2, color = "blue") +
  labs(
    title = "PDP + ICE with 95% CI (ET Model)",
    x = "TM (2-meter Temperature)",
    y = "Predicted O₃"
  ) +
  theme_minimal() +
  theme(text = element_text(family = "Times New Roman", size = 12))

# ==== Step 1：在 RStudio 中展示图像 ====
print(pdp_ice_plot)

# ==== Step 2：保存图像 ====
ggsave("PDP_ICE_TM.pdf", plot = pdp_ice_plot, width = 6, height = 4, dpi = 300)
ggsave("PDP_ICE_TM.jpg", plot = pdp_ice_plot, width = 6, height = 4, dpi = 300)
