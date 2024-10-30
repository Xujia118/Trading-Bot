'''
1. make a csv file to avoid connecting internet every time
2. preprocess data
3. apply random forest

The key is timing. 

'''

import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

class Model:
    def __init__(self, ticker) -> None:
        self.ticker = ticker
        self.df = None

    def create_csv(self):
        df = yf.download(self.ticker)
        df.to_csv(f"./models/{self.ticker}_data.csv")

    def read_csv(self):
        self.df = pd.read_csv(f"./models/{self.ticker}_data.csv")
        print(self.df.head())

    # Preprocess data frame, remove NA
    def build_features(self):
        self.df.na()
    # Build more features

    # 

stock = "AAPL"
model = Model(stock)
# model.create_csv()
# model.read_csv()
model.build_features()