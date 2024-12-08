import yfinance as yf
import pandas as pd


class StocksData:
    def __init__(self):
        self.nasdaq_stocks = []
        self.sp500_stocks = []

    def update_stocks_data(self):
        self._get_financials()
        self._get_candidates()

    def _get_financials(self):
        '''
        Get all stocks from sp500 and nasdaq;
        Retrieve their key financial metrics
        Output to a csv file
        '''

        self._get_nasdaq_stocks()
        self._get_sp500_stocks()
        # all_tickers = self.nasdaq_stocks + self.sp500_stocks # yf doesn't take sp500; too many requests
        all_tickers = self.nasdaq_stocks

        infos = [yf.Ticker(i).info for i in all_tickers]

        df = pd.DataFrame(infos)
        df = df.set_index('symbol')

        fundamentals = ['trailingPE',
                        'trailingEps',
                        'returnOnEquity',
                        'profitMargins',
                        'dividendYield'
                        ]

        df = df[fundamentals]
        df.to_csv('Fundamentals_Nasdaq.csv')
        print('Fundamentals updated successfully.')

    def _get_candidates(self):
        df = pd.read_csv('Fundamentals_Nasdaq.csv', index_col='symbol')

        filter = (df['trailingEps'] >= 0) & \
            (df['returnOnEquity'] >= 0) & \
            (df['profitMargins'] >= 0)
        df = df.loc[filter]

        df.to_csv('candidates_Nasdaq.csv')
        print('Candidates updated. Go to go for the next quater.')

    def _get_nasdaq_stocks(self):
        nasdaq_url = 'https://en.wikipedia.org/wiki/NASDAQ-100'
        nasdaq_table = pd.read_html(nasdaq_url)
        self.nasdaq_stocks = nasdaq_table[4]['Symbol'].tolist()

    def _get_sp500_stocks(self):
        sp500_url = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
        sp500_table = pd.read_html(sp500_url)
        self.sp500_stocks = sp500_table[0]['Symbol'].tolist()


if __name__ == "__main__":
    sd = StocksData()
    sd.update_stocks_data()
