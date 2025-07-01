import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os

# === 1. 读取数据 ===
df = pd.read_csv(r'D:\lunwen\xiangguanxing.csv')

# === 2. 设置样式 ===
plt.rcParams['font.family'] = 'Times New Roman'
sns.set(style="whitegrid")

# === 3. 设置保存目录 ===
save_dir = r'D:\lunwen2\pictures\xiangxiantu2'
os.makedirs(save_dir, exist_ok=True)

# === 4. 对 TP 进行 log(x + 1e-4) 变换，避免 log(0) ===
df['TP_log'] = np.log10(df['TP'] + 1e-4)

# === 5. 绘图 ===
fig, axes = plt.subplots(2, 1, figsize=(6, 4.5),
                         gridspec_kw={'height_ratios': [0.8, 4]},
                         sharex=True)

# 上方：箱线图
sns.boxplot(x=df['TP_log'], ax=axes[0],
            color='#E69F00',
            boxprops=dict(edgecolor='black'),
            medianprops=dict(color='black'),
            whiskerprops=dict(color='black'),
            capprops=dict(color='black'),
            flierprops=dict(markeredgecolor='black'))
axes[0].set(xlabel='', yticks=[])
for spine in axes[0].spines.values():
    spine.set_visible(True)
    spine.set_color('black')

# 下方：直方图 + KDE
sns.histplot(df['TP_log'], kde=True, ax=axes[1],
             color='#E69F00', edgecolor='black')
axes[1].set(xlabel='log₁₀(TP + 1e-4)', ylabel='Count')
for spine in axes[1].spines.values():
    spine.set_visible(True)
    spine.set_color('black')

# === 6. 保存图像 ===
plt.tight_layout()
save_path = os.path.join(save_dir, 'TP_log_distribution.png')
plt.savefig(save_path, dpi=300, bbox_inches='tight')
plt.show()
