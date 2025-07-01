def draw_custom_pdp_from_pycaret(model_path, data_path, feature, save_path):
    import pandas as pd
    import matplotlib.pyplot as plt
    from matplotlib import rcParams
    from sklearn.inspection import partial_dependence
    from pycaret.regression import load_model

 # 图形美化
    rcParams['font.family'] = 'Times New Roman'
    rcParams['axes.facecolor'] = '#EAEAF2'
    rcParams['axes.edgecolor'] = 'black'
    rcParams['axes.linewidth'] = 1.2

 # 加载数据与模型
    data = pd.read_csv(data_path)
    X = data.drop(columns=["O3"])
    pycaret_model = load_model(model_path)
    model = pycaret_model.steps[-1][1]  # 提取真实模型 estimator

# PDP 提取
    pdp_result = partial_dependence(model, X, features=[feature], kind='both', grid_resolution=50)
    pdp_x = pdp_result["values"][0]
    pdp_y = pdp_result["average"][0]
    ice_y = pdp_result["individual"][0]

# 绘图
    plt.figure(figsize=(7,5), dpi=120)
    for i in range(min(ice_y.shape[0], 100)):  # 控制最多100条 ICE 曲线避免太密
        plt.plot(pdp_x, ice_y[i], color='lightblue', linewidth=0.6, alpha=0.3)
    plt.plot(pdp_x, pdp_y, color='blue', linewidth=2.2, label="PDP average")

    plt.title(f"Partial Dependence of {feature}", fontsize=14)
    plt.xlabel(f"{feature} (°C)", fontsize=12)
    plt.ylabel("Predicted O₃", fontsize=12)
    plt.legend()
    plt.grid(False)
    plt.tight_layout()
    plt.savefig(save_path, dpi=300)
    plt.show()
draw_custom_pdp_from_pycaret(
    model_path="et_final_model",
    data_path="D:/lunwen/xunlian.csv",
    feature="2TM",
    save_path="D:/lunwen2/PDP_2TM_final.jpg"
)