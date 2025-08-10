import pandas as pd

money = pd.read_parquet('money.parquet')
cash = pd.read_parquet('cash.parquet')
abgroup = pd.read_parquet('abgroup.parquet')
platforms = pd.read_parquet('platforms.parquet')

money_agg = money.groupby('user_id').agg(
    money_sum=('money', 'sum'),
    money_count=('money', 'size'),
    money_unique_days=('date', 'nunique')
).reset_index()

cash_agg = cash.groupby('user_id').agg(
    cash_sum=('cash', 'sum'),
    cash_count=('cash', 'size'),
    cash_unique_days=('date', 'nunique')
).reset_index()

agg = pd.merge(money_agg, cash_agg, on='user_id', how='outer').fillna(0)

agg['total_count'] = agg['money_count'] + agg['cash_count']
agg['total_unique_days'] = agg['money_unique_days'] + agg['cash_unique_days']

agg['norm_total_count'] = (agg['total_count'] - agg['total_count'].mean()) / agg['total_count'].std(ddof=0)
agg['norm_total_unique_days'] = (agg['total_unique_days'] - agg['total_unique_days'].mean()) / agg['total_unique_days'].std(ddof=0)

def iqr(series):
    q75, q25 = series.quantile(q=0.75), series.quantile(q=0.25)
    return q75 - q25

cash_sum_iqr = iqr(agg['cash_sum'])
money_sum_iqr = iqr(agg['money_sum'])
norm_total_count_iqr = iqr(agg['norm_total_count'])
norm_total_unique_days_iqr = iqr(agg['norm_total_unique_days'])

agg['f1'] = agg['cash_sum'] > (agg['cash_sum'].median() + 1.5 * cash_sum_iqr)
agg['f2'] = agg['money_sum'] > (agg['money_sum'].median() + 1.5 * money_sum_iqr)
agg['f3'] = agg['norm_total_count'] > (agg['norm_total_count'].median() + 1.5 * norm_total_count_iqr)
agg['f4'] = agg['norm_total_unique_days'] > (agg['norm_total_unique_days'].median() + 1.5 * norm_total_unique_days_iqr)

agg['cheater'] = (agg[['f1', 'f2', 'f3', 'f4']].sum(axis=1) >= 2)

cheaters = set(agg.loc[agg['cheater'], 'user_id'])

df = (abgroup
      .merge(money_agg[['user_id', 'money_sum']], on='user_id', how='left')
      .merge(cash_agg[['user_id', 'cash_sum']], on='user_id', how='left')
      .merge(platforms, on='user_id', how='left'))
df = df[~df['user_id'].isin(cheaters)]

df['money_sum'] = df['money_sum'].fillna(0)
df['cash_sum'] = df['cash_sum'].fillna(0)

metrics = []

for group_name, group_df in df.groupby('group'):
    total_users = group_df['user_id'].nunique()
    total_revenue = group_df['money_sum'].sum()
    paying_users = group_df.loc[group_df['money_sum'] > 0, 'user_id'].nunique()
    total_cash = group_df['cash_sum'].sum()

    arpu = total_revenue / total_users
    arppu = total_revenue / paying_users if paying_users > 0 else 0
    avg_cash = total_cash / total_users

    metrics.append({
        'group': group_name,
        'users': total_users,
        'paying_users': paying_users,
        'ARPU': arpu,
        'ARPPU': arppu,
        'AVGCash': avg_cash,
    })

metrics_df = pd.DataFrame(metrics)
print(metrics_df)

df.to_csv('cleaned_data.csv', index=False)
