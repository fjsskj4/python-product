import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# 设置中文字体
plt.rcParams["font.family"] = ["SimHei", "Microsoft YaHei", "Arial"]
plt.rcParams["axes.unicode_minus"] = False

# 定义数据
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

# 颜色映射
season_palette = {
    "春季": "#8BC34A", "夏季": "#FFC107",
    "秋季": "#FF9800", "冬季": "#2196F3"
}

# 图表1：各月平均高温分布（柱状图）
plt.figure(figsize=(12, 6))
sns.barplot(
    x="月份", y="平均高温 (℃)", hue="季节",
    data=df, palette=season_palette, dodge=False
)
for x, y in enumerate(df["平均高温 (℃)"]):
    plt.text(x, y+0.5, f"{y}℃", ha="center", fontsize=10)
plt.title("各月平均高温分布", fontsize=14)
plt.legend(loc="upper left")
plt.tight_layout()
plt.show()

# 图表2：降水量与低温关系（气泡图）
plt.figure(figsize=(12, 6))
sns.scatterplot(
    x="月份", y="降水量 (mm)",
    size=df["平均低温 (℃)"].abs(),
    sizes=(30, 200),
    color="#2196F3", alpha=0.7,
    data=df
)
plt.title("降水量与低温关系", fontsize=14)
plt.legend(title="平均低温绝对值", bbox_to_anchor=(1, 1))
plt.tight_layout()
plt.show()

# 图表3：季节降水量分布（小提琴图）
plt.figure(figsize=(12, 6))
sns.violinplot(
    x="季节", y="降水量 (mm)", hue="季节",
    palette=season_palette,
    inner="quartile",
    dodge=False,
    data=df
)
plt.title("季节降水量分布", fontsize=14)
plt.legend().remove()
plt.tight_layout()
plt.show()

# 图表4：高温与降水量关系（分类散点图）
plt.figure(figsize=(12, 6))
sns.scatterplot(
    x="平均高温 (℃)", y="降水量 (mm)",
    hue="季节", palette=season_palette,
    s=80, alpha=0.8,
    data=df
)
plt.title("高温与降水量关系", fontsize=14)
plt.legend(bbox_to_anchor=(1, 1))
plt.tight_layout()
plt.show()

# 图表5：各月平均低温趋势（点图）
plt.figure(figsize=(12, 6))
sns.pointplot(
    x="月份", y="平均低温 (℃)",
    color="#FF5722",
    markers="o", linestyles="--",
    data=df
)
plt.title("各月平均低温趋势", fontsize=14)
plt.tight_layout()
plt.show()

# 图表6：季节温度分布对比（箱线图）
plt.figure(figsize=(12, 6))
df_melt = pd.melt(
    df,
    id_vars=["月份", "季节"],
    value_vars=["平均高温 (℃)", "平均低温 (℃)"],
    var_name="温度类型",
    value_name="温度值"
)
sns.boxplot(
    x="季节", y="温度值", hue="温度类型",
    palette={"平均高温 (℃)": "#FF9800", "平均低温 (℃)": "#2196F3"},
    data=df_melt
)
plt.title("季节温度分布对比", fontsize=14)
plt.legend(title="", bbox_to_anchor=(1, 1))
plt.tight_layout()
plt.show()

# 图表7：平均高温分布特征（直方图+KDE曲线）
plt.figure(figsize=(12, 6))
sns.histplot(
    df["平均高温 (℃)"],
    bins=8, kde=True,
    color="#8BC34A"
)
plt.title("平均高温分布特征", fontsize=14)
plt.tight_layout()
plt.show()

# 图表8：降水量分布密度（KDE+ rugs 原始点）
plt.figure(figsize=(12, 6))
sns.kdeplot(
    df["降水量 (mm)"],
    fill=True, color="#E91E63"
)
sns.rugplot(
    df["降水量 (mm)"],
    color="#E91E63", height=0.1
)
plt.title("降水量分布密度", fontsize=14)
plt.tight_layout()
plt.show()

# 图表9：指标相关性热力图
plt.figure(figsize=(10, 8))
corr = df[["平均高温 (℃)", "平均低温 (℃)", "降水量 (mm)"]].corr()
sns.heatmap(
    corr, annot=True, fmt=".2f",
    cmap="RdBu_r", vmin=-1, vmax=1
)
plt.title("指标相关性热力图", fontsize=14)
plt.tight_layout()
plt.show()

# 图表10：季节分布占比（饼图）
plt.figure(figsize=(10, 8))
season_counts = df["季节"].value_counts()
plt.pie(
    season_counts,
    labels=season_counts.index,
    autopct='%1.1f%%',
    colors=[season_palette[k] for k in season_counts.index],
    startangle=90,
    wedgeprops={'edgecolor': 'w', 'linewidth': 1}
)
plt.title("季节分布占比", fontsize=14)
plt.tight_layout()
plt.show()

# 图表11：四季气候特征雷达图
plt.figure(figsize=(10, 8))
ax = plt.subplot(111, polar=True)

# 选 3月（春）、6月（夏）、9月（秋）、12月（冬）
radar_data = df.query("月份 in ['3月','6月','9月','12月']")
# 指标归一化（0-1）
radar_vars = ["平均高温 (℃)", "平均低温 (℃)", "降水量 (mm)"]
radar_norm = (radar_data[radar_vars] - radar_data[radar_vars].min()) / (radar_data[radar_vars].max() - radar_data[radar_vars].min())
radar_norm = pd.concat([radar_norm, radar_norm.iloc[[0]]], ignore_index=True)  # 闭合图形

# 计算角度
angles = np.linspace(0, 2*np.pi, len(radar_vars), endpoint=False).tolist()
angles += angles[:1]  # 闭合角度

# 绘制雷达图
for i, month in enumerate(radar_data["月份"]):
    values = radar_norm.iloc[i].tolist() + radar_norm.iloc[i].tolist()[:1]  # 闭合数据点
    ax.plot(angles, values,
              label=month, color=season_palette[radar_data["季节"].iloc[i]])
    ax.fill(angles, values, alpha=0.25)

# 配置雷达图
ax.set_yticklabels([])  # 隐藏径向刻度
ax.set_xticks(angles[:-1])
ax.set_xticklabels(radar_vars, fontsize=10)
ax.legend(bbox_to_anchor=(1.2, 1), fontsize=9)
ax.set_title("四季气候特征雷达图", fontsize=12)
plt.tight_layout()
plt.show()