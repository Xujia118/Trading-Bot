import numpy as np
import pandas as pd
import parameters

class TechnicalAnalysis:
    def __init__(self, df) -> None:
        self.df = df
        self.boll_tolerance = parameters.boll_tolerance
        self.small_candle_tolerance = parameters.small_candle_tolerance
        self.consolidation_tolerance = parameters.consolidation_tolerance
        self.SMA_tolerance = parameters.SMA_tolerance

    def SMA60(self): 
        # forbid buying if price is above SMA60
        self.df['SMA60'] = self.df['Close'].rolling(window=60).mean()
        self.df['below_SMA60'] = np.where(self.df['Close'] < self.df['SMA60'], True, False)
        return self.df

    def SMA120(self):   
        # forbig buying if a large portion of close is under SMA120
        self.df['SMA120'] = self.df['Close'].rolling(window=120).mean()
        self.df['above_SMA120'] = np.where(self.df['Close'] > self.df['SMA120'], True, False)      
        self.df['check_SMA120'] = self.df['above_SMA120'].rolling(window=120).sum() / 120
        return self.df  
        
    def Bollinger(self):  
        self.df['SMA20'] = self.df['Close'].rolling(window=20).mean() 
        self.df['Upper'] = self.df['SMA20'] + 2 * self.df['Close'].rolling(window=20).std()
        self.df['Lower'] = self.df['SMA20'] - 2 * self.df['Close'].rolling(window=20).std()

        self.df['Boll_buy'] = np.where(self.df['Low'] * (1 - self.boll_tolerance) <= self.df['Lower'], True, False)
        self.df['Boll_sell'] = np.where(self.df['High'] * (1 + self.boll_tolerance) >= self.df['Upper'], True, False)
        
        return self.df
    
    def sell_consolidation(self):
        yesterday_df = self.df.shift(1, fill_value=0)    

        today_small_bearish_candle = (abs(self.df['Open'] - self.df['Close']) <= self.small_candle_tolerance * self.df['Open']) & \
                                    self.df['Close'] <= self.df['Open']

        # Bearish engulf
        bearish_engulf = (self.df['Open'] * (1 + self.consolidation_tolerance) >= np.maximum(yesterday_df['Open'], yesterday_df['Close'])) & \
                        (self.df['Close'] * (1 - self.consolidation_tolerance) <= np.minimum(yesterday_df['Open'], yesterday_df['Close']))

        # Flag
        flag = (yesterday_df['High'] * (1 + self.consolidation_tolerance) >= np.maximum(self.df['Open'], self.df['Close'])) & \
                    (yesterday_df['Low'] * (1 - self.consolidation_tolerance) <= np.minimum(self.df['Open'], self.df['Close']))
        
        self.df['sell_consolidation'] = bearish_engulf | (flag & today_small_bearish_candle)                                  

        return self.df
    
    def buy_consolidation(self):
        yesterday_df = self.df.shift(1, fill_value=0)
        
        today_small_candle = (abs(self.df['Open'] - self.df['Close']) <= self.small_candle_tolerance * self.df['Open']) #& \
                                    #self.df['Close'] > self.df['Open']
        
        # Bullish engulf
        bullish_engulf = (self.df['Close'] * (1 + self.consolidation_tolerance) >= np.maximum(yesterday_df['Open'], yesterday_df['Close'])) & \
                        (self.df['Open'] * (1 - self.consolidation_tolerance) <= np.minimum(yesterday_df['Open'], yesterday_df['Close']))
        
        # Flag
        flag = (yesterday_df['High'] * (1 + self.consolidation_tolerance) >= np.maximum(self.df['Open'], self.df['Close'])) & \
                    (yesterday_df['Low'] * (1 - self.consolidation_tolerance) <= np.minimum(self.df['Open'], self.df['Close'])) 
    

        self.df['buy_consolidation'] = bullish_engulf | (flag & today_small_candle)

        return self.df

    def good_to_buy(self, consolidation_days=3):  
        self.df = self.SMA60()  
        self.df = self.SMA120() 
        self.df = self.Bollinger()         
        self.df = self.buy_consolidation()

        boll_buy_dates = self.df.index[(self.df['Boll_buy']) & 
                                       (self.df['check_SMA120'] >= self.SMA_tolerance) & 
                                       (self.df['below_SMA60'])
                                       ].tolist()       
        buy_status = {date: False for date in self.df.index}
        
        for boll_buy_date in boll_buy_dates:
            start_date = boll_buy_date
            end_date = start_date + pd.Timedelta(consolidation_days, 'd')  

            consolidation_dates = self.df.loc[start_date:end_date, 'buy_consolidation'].index
            for date in consolidation_dates:
                if self.df.loc[date, 'buy_consolidation']:
                    buy_status[date] = True
        
        self.df['good_to_buy'] = self.df.index.map(buy_status)
        
        return self.df

    def good_to_sell(self, consolidation_days=0):
        self.df = self.Bollinger()
        self.df = self.sell_consolidation()

        # Consolidation signal remains valid for three days
        boll_sell_dates = self.df.index[self.df['Boll_sell']].to_list()
        sell_status = {date: False for date in self.df.index}

        for boll_sell_date in boll_sell_dates:
            start_date = boll_sell_date
            end_date = start_date + pd.Timedelta(consolidation_days, 'd')

            consolidation_dates = self.df.loc[start_date:end_date, 'sell_consolidation'].index
            for date in consolidation_dates:
                if self.df.loc[date, 'sell_consolidation']:
                    sell_status[date] = True
            
        self.df['good_to_sell'] = self.df.index.map(sell_status)

        return self.df