import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from matplotlib.gridspec import GridSpec  # 精细布局控制

# ============== 1. 修复字体问题 ==============
# 优先使用系统已安装的中文字体（如 "SimHei" 或 "Microsoft YaHei"）
plt.rcParams["font.family"] = ["SimHei", "Microsoft YaHei", "Arial"]
plt.rcParams["axes.unicode_minus"] = False  # 解决负号显示问题

# ============== 2. 定义数据 ==============
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

# 颜色映射（季节）
season_palette = {
    "春季": "#8BC34A", "夏季": "#FFC107",
    "秋季": "#FF9800", "冬季": "#2196F3"
}

# ============== 3. 初始化画布 ==============
fig = plt.figure(figsize=(20, 22))
gs = GridSpec(4, 4,  # 4行4列布局
              width_ratios=[1, 1, 1, 1],
              height_ratios=[1, 1, 1, 0.8])

# ============== 4. 子图1：月份-平均高温（修复 Seaborn 警告） ==============
ax1 = plt.subplot(gs[0, 0])
# 通过 hue 参数传递分组依据，避免 palette 警告
sns.barplot(
    x="月份", y="平均高温 (℃)", hue="季节",  # 添加 hue 参数
    data=df, palette=season_palette,
    dodge=False,  # 关闭分组偏移（保持单柱子）
    ax=ax1
)
# 更健壮的图例移除方式
if ax1.get_legend():
    ax1.get_legend().remove()
# 添加数值标注
for x, y in enumerate(df["平均高温 (℃)"]):
    ax1.text(x, y+0.5, f"{y}℃", ha="center", fontsize=9)
ax1.set_title("各月平均高温分布", fontsize=12)

# ============== 5. 子图2：月份-降水量（气泡图） ==============
ax2 = plt.subplot(gs[0, 1])
sns.scatterplot(
    x="月份", y="降水量 (mm)",
    size=df["平均低温 (℃)"].abs(),  # 气泡大小用低温绝对值
    sizes=(30, 200),  # 气泡尺寸范围
    color="#2196F3", alpha=0.7,
    data=df, ax=ax2
)
ax2.legend(title="平均低温绝对值", bbox_to_anchor=(1, 1), fontsize=9)
ax2.set_title("降水量与低温关系", fontsize=12)

# ============== 6. 子图3：季节-降水量分布（修复 Seaborn 警告） ==============
ax3 = plt.subplot(gs[0, 2])
# 通过 hue 参数传递分组依据，避免 palette 警告
sns.violinplot(
    x="季节", y="降水量 (mm)", hue="季节",  # 添加 hue 参数
    palette=season_palette,
    inner="quartile",  # 显示四分位数
    dodge=False,  # 关闭分组偏移
    data=df, ax=ax3
)
# 更健壮的图例移除方式
if ax3.get_legend():
    ax3.get_legend().remove()
ax3.set_title("季节降水量分布", fontsize=12)

# ============== 7. 子图4：平均高温-降水量（分类散点图） ==============
ax4 = plt.subplot(gs[0, 3])
sns.scatterplot(
    x="平均高温 (℃)", y="降水量 (mm)",
    hue="季节", palette=season_palette,
    s=80, alpha=0.8,
    data=df, ax=ax4
)
ax4.legend(bbox_to_anchor=(1, 1), fontsize=9)
ax4.set_title("高温与降水量关系", fontsize=12)

# ============== 8. 子图5：月份-平均低温（带趋势线的点图） ==============
ax5 = plt.subplot(gs[1, 0])
sns.pointplot(
    x="月份", y="平均低温 (℃)",
    color="#FF5722",
    markers="o", linestyles="--",
    data=df, ax=ax5
)
ax5.set_title("各月平均低温趋势", fontsize=12)

# ============== 9. 子图6：季节-温度分布（箱线图） ==============
# 重塑数据为长格式
df_melt = pd.melt(
    df,
    id_vars=["月份", "季节"],
    value_vars=["平均高温 (℃)", "平均低温 (℃)"],
    var_name="温度类型",
    value_name="温度值"
)
ax6 = plt.subplot(gs[1, 1])
sns.boxplot(
    x="季节", y="温度值", hue="温度类型",
    palette={"平均高温 (℃)": "#FF9800", "平均低温 (℃)": "#2196F3"},
    data=df_melt, ax=ax6
)
ax6.legend(title="", bbox_to_anchor=(1, 1), fontsize=9)
ax6.set_title("季节温度分布对比", fontsize=12)

# ============== 10. 子图7：平均高温分布（直方图+KDE曲线） ==============
ax7 = plt.subplot(gs[1, 2])
sns.histplot(
    df["平均高温 (℃)"],
    bins=8, kde=True,
    color="#8BC34A",
    ax=ax7
)
ax7.set_title("平均高温分布特征", fontsize=12)

# ============== 11. 子图8：降水量分布（KDE+ rugs 原始点） ==============
ax8 = plt.subplot(gs[1, 3])
sns.kdeplot(
    df["降水量 (mm)"],
    fill=True, color="#E91E63",
    ax=ax8
)
sns.rugplot(
    df["降水量 (mm)"],
    color="#E91E63", height=0.1,
    ax=ax8
)
ax8.set_title("降水量分布密度", fontsize=12)

# ============== 12. 子图9：数据相关性（热力图+数值标注） ==============
ax9 = plt.subplot(gs[2, :2])  # 跨两列
corr = df[["平均高温 (℃)", "平均低温 (℃)", "降水量 (mm)"]].corr()
sns.heatmap(
    corr, annot=True, fmt=".2f",
    cmap="RdBu_r", vmin=-1, vmax=1,
    ax=ax9
)
ax9.set_title("指标相关性热力图", fontsize=12)

# ============== 13. 子图10：季节占比（饼图） ==============
ax10 = plt.subplot(gs[2, 2:])  # 跨两列
season_counts = df["季节"].value_counts()
ax10.pie(
    season_counts,
    labels=season_counts.index,
    autopct='%1.1f%%',
    colors=[season_palette[k] for k in season_counts.index],
    startangle=90,
    wedgeprops={'edgecolor': 'w', 'linewidth': 1}
)
ax10.set_title("季节分布占比", fontsize=12)

# ============== 14. 子图11：年度气候雷达图（修复维度不匹配） ==============
ax11 = plt.subplot(gs[3, 1:3], polar=True)  # 极坐标（雷达图）
# 选 3月（春）、6月（夏）、9月（秋）、12月（冬）
radar_data = df.query("月份 in ['3月','6月','9月','12月']")
# 指标归一化（0-1）
radar_vars = ["平均高温 (℃)", "平均低温 (℃)", "降水量 (mm)"]
radar_norm = (radar_data[radar_vars] - radar_data[radar_vars].min()) / (radar_data[radar_vars].max() - radar_data[radar_vars].min())

# 修复 append 方法：用 concat 替代
radar_norm = pd.concat([radar_norm, radar_norm.iloc[[0]]], ignore_index=True)  # 闭合图形

# 重新计算角度（与数据列数匹配）
angles = np.linspace(0, 2*np.pi, len(radar_vars), endpoint=False).tolist()
angles += angles[:1]  # 闭合角度

# 绘制雷达图（转置数据以匹配角度）
for i, month in enumerate(radar_data["月份"]):
    values = radar_norm.iloc[i].tolist() + radar_norm.iloc[i].tolist()[:1]  # 闭合数据点
    ax11.plot(angles, values,
              label=month, color=season_palette[radar_data["季节"].iloc[i]])
    ax11.fill(angles, values, alpha=0.25)

# 配置雷达图
ax11.set_yticklabels([])  # 隐藏径向刻度
ax11.set_xticks(angles[:-1])
ax11.set_xticklabels(radar_vars, fontsize=10)
ax11.legend(bbox_to_anchor=(1.2, 1), fontsize=9)
ax11.set_title("四季气候特征雷达图", fontsize=12)

# ============== 15. 整体布局调整 ==============
plt.tight_layout(h_pad=3, w_pad=2)  # 增大子图间距
plt.show()