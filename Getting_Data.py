import pandas as pd

money = pd.read_csv('Money.csv', usecols=['user_id', 'date', 'money'], dtype={'user_id': str, 'money': 'float32'})
cheaters = pd.read_csv('Cheaters.csv', usecols=['user_id', 'cheaters'], dtype={'user_id': str, 'cheaters': 'int8'})
abgroup = pd.read_csv('ABgroup.csv', usecols=['user_id', 'group'], dtype={'user_id': str, 'group': 'category'})
platforms = pd.read_csv('Platforms.csv', usecols=['user_id', 'platform'], dtype= {'user_id': str, 'platform': 'category'})
cash = pd.read_csv('Cash.csv', usecols=['user_id', 'date', 'cash'], dtype={'user_id': str, 'cash': 'float32'})

cheater_ids = set(cheaters.loc[cheaters['cheaters'] == 1, 'user_id'])

money = money[~money['user_id'].isin(cheater_ids)]
abgroup = abgroup[~abgroup['user_id'].isin(cheater_ids)]
platforms = platforms[~platforms['user_id'].isin(cheater_ids)]
cash = cash[~cash['user_id'].isin(cheater_ids)]

money = money.drop_duplicates()
abgroup = abgroup.drop_duplicates()
platforms = platforms.drop_duplicates()
cash = cash.drop_duplicates()
cheaters = cheaters.drop_duplicates()

money['date'] = pd.to_datetime(money['date'], format = '%d.%m.%Y')
cash['date'] = pd.to_datetime(cash['date'], format = '%d.%m.%Y')

money = money[money['money'] >= 0]
cash = cash[cash['cash'] >= 0]

def three_sigmas(df, col):
    mean = df[col].mean()
    std = df[col].std()
    return df[(df[col] >= mean - 3*std) & (df[col] <= mean + 3*std)]

money = three_sigmas(money, 'money')
cash = three_sigmas(cash, 'cash')

money.to_parquet('money.parquet', index=False)
cash.to_parquet('cash.parquet', index=False)
platforms.to_parquet('platforms.parquet', index=False)
abgroup.to_parquet('abgroup.parquet', index=False)
cheaters.to_parquet('cheaters.parquet', index=False)

