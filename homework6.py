import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
df = pd.read_csv('D:/edgedownloads/专利文献/global_freelancers_raw.csv')
df['gender_clean'] = df['gender'].str.lower().str.extract(r'(f|m)', expand=False).map({'f': 'Female', 'm': 'Male'})
df['hourly_rate_clean'] = df['hourly_rate (USD)'].replace('[^\d.]', '', regex=True).astype(float)
df['is_active_clean'] = df['is_active'].astype(str).str.upper().map({'1': 1, '0': 0, 'Y': 1, 'N': 0})
df['client_satisfaction_clean'] = pd.to_numeric(df['client_satisfaction'].str.replace('%', '', regex=False), errors='coerce')

sns.set(style="whitegrid")
plt.rcParams.update({'font.size': 10})

fig, axes = plt.subplots(2, 2, figsize=(14, 10))
axes = axes.flatten()

sns.scatterplot(data=df, x='age', y='rating', ax=axes[0], alpha=0.6)
axes[0].set_title("Age vs Rating")

sns.scatterplot(data=df, x='years_of_experience', y='hourly_rate_clean', ax=axes[1], alpha=0.6)
axes[1].set_title("Experience vs Hourly Rate")

sns.scatterplot(data=df, x='hourly_rate_clean', y='client_satisfaction_clean', ax=axes[2], alpha=0.6)
axes[2].set_title("Hourly Rate vs Client Satisfaction")

sns.scatterplot(data=df, x='rating', y='client_satisfaction_clean', ax=axes[3], alpha=0.6)
axes[3].set_title("Rating vs Client Satisfaction")

plt.tight_layout()
plt.show()
