from alpaca.data.historical import StockHistoricalDataClient
from alpaca.data.requests import StockBarsRequest
from alpaca.data.timeframe import TimeFrame
import pandas as pd
import config

def GetTickcerData(ticker, start):
    client = StockHistoricalDataClient(config.API_KEY, config.SECRET_KEY)

    request_params = StockBarsRequest(
        symbol_or_symbols=[ticker],
        timeframe=TimeFrame.Day,
        start=f"{start} 00:00:00",
    )

    bars = client.get_stock_bars(request_params)
    df = bars.df

    # Convert the df into a workable form
    df.index = df.index.set_levels(pd.to_datetime(df.index.get_level_values('timestamp')), level='timestamp')
    df['date'] = df.index.get_level_values('timestamp').strftime('%Y-%m-%d')
    df = df[['open', 'high', 'low', 'close', 'date']]
    df = df.rename(columns=lambda x:x.capitalize())
    df['Date'] = pd.to_datetime(df['Date'])
    df.set_index('Date', inplace=True)

    return df

