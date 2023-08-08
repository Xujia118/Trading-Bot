import pandas as pd

df = pd.read_csv('Fundamentals_Nasdaq.csv', index_col='symbol')
filt = (df['trailingEps'] >= 0) & \
        (df['returnOnEquity'] >= 0) & \
        (df['profitMargins'] >= 0)
df = df.loc[filt]

df.to_csv('candidates_Nasdaq.csv')