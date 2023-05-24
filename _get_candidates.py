import pandas as pd

df = pd.read_csv('Fundamentals_Nasdaq.csv', index_col='symbol')
filt = (df['trailingEps'] >= df['trailingEps'].median()) & \
        (df['returnOnEquity'] >= df['returnOnEquity'].median()) & \
        (df['profitMargins'] >= df['profitMargins'].median())
df = df.loc[filt]

df.to_csv('candidates_Nasdaq.csv')