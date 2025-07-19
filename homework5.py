import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv('D:/edgedownloads/专利文献/global_freelancers_raw.csv')

df['gender_clean'] = df['gender'].str.lower().str.extract(r'(f|m)', expand=False)
df['gender_clean'] = df['gender_clean'].map({'f': 'Female', 'm': 'Male'})

df['hourly_rate_clean'] = df['hourly_rate (USD)'].replace('[^\d.]', '', regex=True).astype(float)
df['is_active_clean'] = df['is_active'].astype(str).str.upper().map({'1': 1, '0': 0, 'Y': 1, 'N': 0})

df['client_satisfaction_clean'] = df['client_satisfaction'].str.replace('%', '', regex=False)
df['client_satisfaction_clean'] = pd.to_numeric(df['client_satisfaction_clean'], errors='coerce')

sns.set(style="whitegrid")
plt.rcParams.update({'font.size': 8})

fig, axes = plt.subplots(3, 3, figsize=(15, 12))
axes = axes.flatten()

# 1. 性别分布
sns.countplot(x='gender_clean', data=df, ax=axes[0])
axes[0].set_title("Gender Distribution")

# 2. 国家前10分布
top_countries = df['country'].value_counts().nlargest(10)
sns.barplot(x=top_countries.values, y=top_countries.index, ax=axes[1])
axes[1].set_title("Top 10 Countries")

# 3. 技能分布
top_skills = df['primary_skill'].value_counts()
sns.barplot(x=top_skills.values, y=top_skills.index, ax=axes[2])
axes[2].set_title("Primary Skill Distribution")

# 4. 年龄分布
sns.histplot(df['age'], bins=20, kde=True, ax=axes[3], color="skyblue")
axes[3].set_title("Age Distribution")

# 5. 从业年限分布
sns.histplot(df['years_of_experience'], bins=20, kde=True, ax=axes[4], color="lightgreen")
axes[4].set_title("Years of Experience")

# 6. 客户满意度
sns.histplot(df['client_satisfaction_clean'], bins=20, kde=True, ax=axes[5], color="coral")
axes[5].set_title("Client Satisfaction (%)")

# 7. 评分分布
sns.histplot(df['rating'], bins=10, kde=True, ax=axes[6], color="mediumpurple")
axes[6].set_title("Rating Distribution")

# 8. 时薪分布
sns.histplot(df['hourly_rate_clean'], bins=20, kde=True, ax=axes[7], color="orange")
axes[7].set_title("Hourly Rate (USD)")

# 9. 是否活跃分布
sns.countplot(x='is_active_clean', data=df, ax=axes[8])
axes[8].set_title("Is Active (0/1)")
plt.tight_layout(pad=3.0, h_pad=3.0, w_pad=3.0)
plt.show()
