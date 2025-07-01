from statistics import mean
import math
import matplotlib.pyplot as plt
from sklearn.metrics import explained_variance_score,r2_score,median_absolute_error,mean_squared_error,mean_absolute_error
from scipy import stats
import numpy as np
from matplotlib import rcParams
config = {"font.family":'Times New Roman',"font.size": 16,"mathtext.fontset":'stix'}
rcParams.update(config)
# 读取数据
import pandas as pd
import warnings
warnings.filterwarnings("ignore")


def scatter_out_1(x, y):
    # ==========计算评价指标==========
    MSE = mean_squared_error(x, y)
    RMSE = np.sqrt(MSE)
    R2 = r2_score(x, y)
    MAE = mean_absolute_error(x, y)
    EV = explained_variance_score(x, y)

    if R2 < 0:
        print("R2 值为负数:", R2)
        R = float('nan')  # 设置为 NaN 以避免进一步错误
    else:
        R = math.sqrt(R2)

    print('==========算法评价指标==========')
    print('Explained Variance(EV):', '%.3f' % EV)
    print('Mean Absolute Error(MAE):', '%.3f' % MAE)
    print('Mean squared error(MSE):', '%.3f' % MSE)
    print('Root Mean Squared Error(RMSE):', '%.3f' % RMSE)
    print('R_squared:', '%.3f' % R2)
    print('R:', '%.3f' % R)
    # 其余代码...

    # ===========Calculate the point density==========
    # ===========计算点密度==========
    xy = np.vstack([x, y])
    z = stats.gaussian_kde(xy)(xy)
    # ===========Sort the points by density, so that the densest points are plotted last===========
    # ===========按密度对点进行排序，使最密集的点最后被绘制出来===========
    idx = z.argsort()
    x, y, z = x[idx], y[idx], z[idx]
    def best_fit_slope_and_intercept(xs, ys):
        m = (((mean(xs) * mean(ys)) - mean(xs * ys)) / ((mean(xs) * mean(xs)) - mean(xs * xs)))
        b = mean(ys) - m * mean(xs)
        return m, b

    m, b = best_fit_slope_and_intercept(x, y)
    print('k:', '%.3f' % (m))
    print('b:', '%.3f' % (b))
    t = "y = 0.912x + 2.707"

    regression_line = []
    for a in x:
        regression_line.append((m * a) + b)

    fig,ax=plt.subplots(figsize=(12,9),dpi=600)
    # scatter = ax.scatter(x, y, marker='o', c=z * 100, edgecolors='', s=15, label='LST', cmap='Spectral_r')
    scatter=ax.scatter(x,y,marker='o',c=z,edgecolors='none',s=15,label='LST',cmap='jet')
    # bb = ax.text(0.05, 0.87,'$R^2=%.3f$' % R2, transform=ax.transAxes, fontsize=15, verticalalignment='top', bbox = dict(edgecolor='w',facecolor='w', alpha=1))
    cbar=plt.colorbar(scatter,shrink=1,orientation='vertical',extend='both',pad=0.015,aspect=30,label='frequency')
    font3 = {'family': 'SimHei', 'size': 16, 'color': 'k'}
    # cbar = plt.colorbar(scatter, shrink=1, orientation='vertical', extend='both', pad=0.015, aspect=30,label = '频率',fontdict=font3)

    plt.plot([0,2],[0,2],'black',lw=1.5,linestyle = '--')  # 画的1:1线，线的颜色为black，线宽为0.8
    #当使用48行时，56行可以删除（49行与56行搭配使用）
    plt.scatter(x, y, c=z, s=7, edgecolor='none', cmap='jet')

    plt.plot(x,regression_line,'red',lw=1.5,linestyle = '--')      # 预测与实测数据之间的回归线
    plt.axis([0,2,0,2])  # 设置线的范围

    plt.xlabel('预测值',fontdict=font3)
    plt.ylabel('实测值',fontdict=font3)
    plt.xticks(fontproperties='Times New Roman')
    plt.yticks(fontproperties='Times New Roman')
    # plt.legend(loc='upper right', frameon=False)  # 去掉图例边框
    # plt.legend(loc='upper left', edgecolor='k')  # 设置图例边框颜色
    # plt.legend(loc='upper left', facecolor='w')  # 设置图例背景颜色,若无边框,参数无效


    plt.text(0.1,1.9,t,family = 'Times New Roman')
    plt.text(0.1,1.8, '$N=%.f$' % len(y), family = 'Times New Roman') # text的位置需要根据x,y的大小范围进行调整。
    plt.text(0.1,1.7, '$R=%.3f$' %R2, family = 'Times New Roman')
    # plt.text(1,220, '$BIAS=%.4f$' % BIAS, family = 'Times New Roman')
    plt.text(0.1,1.6, '$RMSE=%.3f$' % RMSE, family = 'Times New Roman')
    plt.text(0.1, 1.5, '$MAE=%.3f$' % MAE, family='Times New Roman')
    plt.xlim(0,2)                                  # 设置x坐标轴的显示范围
    plt.ylim(0,2)                                  # 设置y坐标轴的显示范围
    plt.savefig(r'D:\lunwen\pictures\nihe.png',dpi=800,bbox_inches='tight',pad_inches=0)
    plt.show()

if __name__ == '__main__':
    filename = r'D:\lunwen\nihe.xlsx'
    df2 = pd.read_excel(filename)  # 读取文件
    x = df2['yuce'].values
    y = df2['guance'].values
    scatter_out_1(x,y)