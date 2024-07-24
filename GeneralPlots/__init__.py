import yfinance as yf
import matplotlib.pyplot as plt
import datetime as dt
import os
from pathlib import Path

def plot_returns_from_ticker(ticker):
    n_years_lookback = 10
    start = dt.date.today() - dt.timedelta(days = 365*n_years_lookback)
    end = dt.date.today()


    # Read data 
    df = yf.download(ticker,start,end)

    # View Columns
    df.head()
    plt.figure(figsize=(15,10))
    plt.plot(df['Adj Close'])
    plt.title(ticker + ' Closing Price Chart')
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.grid(True)
    # check current path and create MLFundamentalAnalysis/GeneralPlots/plots/{ticker}_closing_price.png pathname
    if not os.path.exists(os.path.join(os.getcwd(), 'plots')):
        os.makedirs(os.path.join(os.getcwd(), 'plots'))
    pathname = os.path.join(os.getcwd(), 'plots') + '/'
    
    plt.savefig(pathname + ticker + '_closing_price.png')
    
    
if __name__ == "__main__":
    plot_returns_from_ticker('PETR4.SA')