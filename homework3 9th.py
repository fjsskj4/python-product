import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from matplotlib.gridspec import GridSpec

plt.rcParams["font.family"] = ["SimHei", "Microsoft YaHei", "Arial"]
plt.rcParams["axes.unicode_minus"] = False

data = {
    "月份": ["1月", "2月", "3月", "4月", "5月", "6月",
            "7月", "8月", "9月", "10月", "11月", "12月"],
    "平均高温 (℃)": [2, 7, 16, 17, 23, 28, 30, 29, 24, 17, 11, 6],
    "平均低温 (℃)": [-13, -7, 0, 2, 8, 11, 14, 14, 10, 3, -5, -12],
    "降水量 (mm)": [0, 1.9, 2.2, 27.2, 5.5, 40.8, 27.1, 26.6, 34.5, 5.5, 0, 3.6],
    "季节": ["冬季", "冬季", "春季", "春季", "春季", "夏季",
            "夏季", "夏季", "秋季", "秋季", "秋季", "冬季"]
}
df = pd.DataFrame(data)
season_palette = {"春季": "#8BC34A", "夏季": "#FFC107", "秋季": "#FF9800", "冬季": "#2196F3"}


fig = plt.figure(figsize=(22, 20))
gs = GridSpec(3, 3, width_ratios=[1, 1, 1], height_ratios=[1, 1, 1])

ax1 = plt.subplot(gs[0, 0])
sns.barplot(x="月份", y="平均高温 (℃)", hue="季节", data=df, palette=season_palette, dodge=False, ax=ax1)
if ax1.get_legend():
    ax1.get_legend().remove()
for x, y in enumerate(df["平均高温 (℃)"]):
    ax1.text(x, y+0.5, f"{y}℃", ha="center", fontsize=9)
ax1.set_title("各月平均高温分布", fontsize=12)

ax2 = plt.subplot(gs[0, 1])
sns.scatterplot(x="月份", y="降水量 (mm)", size=df["平均低温 (℃)"].abs(), sizes=(30, 200), color="#2196F3", alpha=0.7, data=df, ax=ax2)
ax2.legend(title="平均低温绝对值", bbox_to_anchor=(1.15, 1), fontsize=9)
ax2.set_title("降水量与低温关系", fontsize=12)

ax3 = plt.subplot(gs[0, 2])
sns.violinplot(x="季节", y="降水量 (mm)", hue="季节", data=df, palette=season_palette, inner="quartile", dodge=False, ax=ax3)
if ax3.get_legend():
    ax3.get_legend().remove()
ax3.set_title("季节降水量分布", fontsize=12)
ax4 = plt.subplot(gs[1, 0])
sns.scatterplot(x="平均高温 (℃)", y="降水量 (mm)", hue="季节", palette=season_palette, s=80, alpha=0.8, data=df, ax=ax4)

ax4.legend(
    title="季节",
    bbox_to_anchor=(1.0, 1.0),
    loc='upper left',
    fontsize=9,
    title_fontsize=10
)
ax4.set_title("高温与降水量关系", fontsize=12)


ax5 = plt.subplot(gs[1, 1])
sns.pointplot(x="月份", y="平均低温 (℃)", color="#FF5722", markers="o", linestyles="--", data=df, ax=ax5)
ax5.set_title("各月平均低温趋势", fontsize=12)

ax6 = plt.subplot(gs[1, 2])
df_melt = pd.melt(df, id_vars=["季节"], value_vars=["平均高温 (℃)", "平均低温 (℃)"], var_name="温度类型", value_name="温度值")
sns.boxplot(x="季节", y="温度值", hue="温度类型", data=df_melt, palette={"平均高温 (℃)": "#FF9800", "平均低温 (℃)": "#2196F3"}, ax=ax6)
ax6.legend(title="温度类型", bbox_to_anchor=(1.15, 1), fontsize=9)
ax6.set_title("季节温度分布对比", fontsize=12)


ax7 = plt.subplot(gs[2, 0])
sns.histplot(df["平均高温 (℃)"], bins=8, kde=True, color="#8BC34A", ax=ax7)
ax7.set_title("平均高温分布特征", fontsize=12)

ax8 = plt.subplot(gs[2, 1])
sns.kdeplot(df["降水量 (mm)"], fill=True, color="#E91E63", ax=ax8)
sns.rugplot(df["降水量 (mm)"], color="#E91E63", height=0.1, ax=ax8)
ax8.set_title("降水量分布密度", fontsize=12)


ax9 = plt.subplot(gs[2, 2])
corr = df[["平均高温 (℃)", "平均低温 (℃)", "降水量 (mm)"]].corr()
sns.heatmap(corr, annot=True, fmt=".2f", cmap="RdBu_r", vmin=-1, vmax=1, ax=ax9)
ax9.set_title("指标相关性热力图", fontsize=12)

plt.tight_layout(
    h_pad=7,
    w_pad=3,
    rect=[0.02, 0.03, 1, 0.98]
)
plt.show()#'D:/edgedownloads/专利文献/global_freelancers_raw.csv'