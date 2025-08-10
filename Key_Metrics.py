import pandas as pd
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt

data = pd.read_csv('cleaned_data.csv')

metrics = data.groupby(['group', 'platform']).agg(
    users=('user_id', 'nunique'),
    paying_users=('money_sum', lambda x: (x > 0).sum()),
    revenue=('money_sum', 'sum')
).reset_index()

metrics['ARPU'] = metrics['revenue'] / metrics['users']
metrics['ARPPU'] = metrics['revenue'] / metrics['paying_users'].replace(0, np.nan)
metrics['AvgCash'] = metrics['revenue'] / metrics['paying_users'].replace(0, np.nan)
metrics['conversion'] = metrics['paying_users'] / metrics['users']

def welch_ttest(group1, group2):
    t_stat, p_val = stats.ttest_ind(group1, group2, equal_var=False, nan_policy='omit')
    return p_val

def z_test_conversion(success_a, size_a, success_b, size_b):
    p1 = success_a / size_a
    p2 = success_b / size_b
    p = (success_a + success_b) / (size_a + size_b)
    se = np.sqrt(p * (1 - p) * (1/size_a + 1/size_b))
    if se == 0:
        return 1.0
    z = (p1 - p2) / se
    p_val = 2 * (1 - stats.norm.cdf(abs(z)))
    return p_val

alpha = 0.05

groups = data['group'].unique()
platforms = data['platform'].unique()

for platform in platforms:
    print(f'\nPlatform: {platform}')
    group_data = data[data['platform'] == platform]
    if len(groups) < 2:
        print("Недостаточно групп для сравнения.")
        continue
    g1 = groups[0]
    g2 = groups[1]

    arpu_g1 = group_data[group_data['group'] == g1].groupby('user_id')['money_sum'].sum()
    arpu_g2 = group_data[group_data['group'] == g2].groupby('user_id')['money_sum'].sum()
    p_arpu = welch_ttest(arpu_g1, arpu_g2)
    print(f'ARPU Welch t-test p-value: {p_arpu:.4f} - {"Significant" if p_arpu < alpha else "Not significant"}')

    payers_g1 = group_data[(group_data['group'] == g1) & (group_data['money_sum'] > 0)].groupby('user_id')['money_sum'].sum()
    payers_g2 = group_data[(group_data['group'] == g2) & (group_data['money_sum'] > 0)].groupby('user_id')['money_sum'].sum()
    if len(payers_g1) > 0 and len(payers_g2) > 0:
        p_arppu = welch_ttest(payers_g1, payers_g2)
        print(f'ARPPU Welch t-test p-value: {p_arppu:.4f} - {"Significant" if p_arppu < alpha else "Not significant"}')
    else:
        print('ARPPU Welch t-test: Not enough paying users for comparison.')

    success_g1 = (group_data[group_data['group'] == g1].groupby('user_id')['money_sum'].sum() > 0).sum()
    size_g1 = group_data[group_data['group'] == g1]['user_id'].nunique()
    success_g2 = (group_data[group_data['group'] == g2].groupby('user_id')['money_sum'].sum() > 0).sum()
    size_g2 = group_data[group_data['group'] == g2]['user_id'].nunique()
    p_conv = z_test_conversion(success_g1, size_g1, success_g2, size_g2)
    print(f'Conversion z-test p-value: {p_conv:.4f} - {"Significant" if p_conv < alpha else "Not significant"}')

fig, axs = plt.subplots(1, 3, figsize=(18, 5))

arpu_plot = metrics.pivot(index='group', columns='platform', values='ARPU')
arpu_plot.plot(kind='bar', ax=axs[0])
axs[0].set_title('ARPU by Group and Platform')
axs[0].set_ylabel('ARPU')
axs[0].set_xlabel('Group')

arppu_plot = metrics.pivot(index='group', columns='platform', values='ARPPU')
arppu_plot.plot(kind='bar', ax=axs[1])
axs[1].set_title('ARPPU by Group and Platform')
axs[1].set_ylabel('ARPPU')
axs[1].set_xlabel('Group')

conv_plot = metrics.pivot(index='group', columns='platform', values='conversion')
conv_plot.plot(kind='bar', ax=axs[2])
axs[2].set_title('Conversion by Group and Platform')
axs[2].set_ylabel('Conversion Rate')
axs[2].set_xlabel('Group')

plt.tight_layout()
plt.show()
