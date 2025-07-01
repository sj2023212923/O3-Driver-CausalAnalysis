import pandas as pd
import numpy as np
import joblib
from sklearn.ensemble import ExtraTreesRegressor
from sklearn.inspection import PartialDependenceDisplay
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings("ignore")

# ✅ 加载训练数据
data = pd.read_csv(r"D:\lunwen2\xunlian_cf_ate_with_zscore.csv")
data['point_id'] = data['LG'].astype(str) + "_" + data['LT'].astype(str)

# ✅ 加载你保存的 PyCaret 模型
final_model = joblib.load(r"C:\Users\shila\Desktop\jupyter\et_final_model.pkl")
raw_model = final_model.named_steps["actual_estimator"]
model_params = raw_model.get_params()

# ✅ 设置参数
target = 'O3'
treatment = 'DATE'
top6_vars = ['2TM', 'NT', 'DATE', 'TE', 'NDVI', 'LT']  # 替换为你 SHAP 提取出的特征

# ✅ 存储结果
results = []

# ✅ 遍历每个点位，训练并计算 PDP ATE
for pid, df_point in data.groupby('point_id'):
    if len(df_point) < 30:
        continue  # 样本过少跳过

    X = df_point[top6_vars]
    y = df_point[target]

    try:
        # ✅ 使用原始模型结构重新训练每个点位模型
        model = ExtraTreesRegressor(**model_params)
        model.fit(X, y)

        # ✅ 计算 PDP
        display = PartialDependenceDisplay.from_estimator(model, X, features=[treatment])
        line = display.lines_[0][0]  # 提取曲线
        x_vals, y_vals = line.get_data()

        # ✅ PDP ATE = 斜率（首末值差）
        pdp_slope = (y_vals[-1] - y_vals[0]) / (x_vals[-1] - x_vals[0])

        results.append({
            'point_id': pid,
            'LG': df_point['LG'].iloc[0],
            'LT': df_point['LT'].iloc[0],
            'ATE_PDP': pdp_slope
        })

    except Exception as e:
        print(f"❌ 跳过 {pid}，因为 PDP 计算报错：{e}")

# ✅ 保存结果
df_pdp = pd.DataFrame(results)
df_pdp.to_csv("D:/lunwen2/DATE/pdp_ate_result_with_model.csv", index=False)
print("✅ PDP ATE 计算完成，已保存为 pdp_ate_result_with_model.csv")
